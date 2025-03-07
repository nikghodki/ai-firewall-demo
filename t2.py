import openai
import gradio as gr
import os, json
import constants
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='firewall_rules')

os.environ["OPENAI_API_KEY"] = constants.APIKEY
openai.api_key = constants.APIKEY

def verify_reply(reply):
    if reply:
        try:
            json_reply = json.loads(reply)
        except ValueError as err:
            return False
    return json_reply


def call_api(api_input):
    channel.basic_publish(exchange='',
                          routing_key='firewall_rules',
                          body=str(api_input))
    print(f" [x] Sent {api_input} to be added to firewall rule")

with open('schemas.json') as file:
    firewall_data = json.load(file)
    print(firewall_data)
    firewall_data_str =json.dumps(firewall_data)


def chatbot(input):
    if input:
        messages = [{"role": "system",
                     "content": "You are a firewall Management center assistant, check if user wants to add or edit or delete the firewall rule, check the parameters in the input given by user and create a JSON  body with the parameters for firewall rule. Generate output in json format."},
                    {"role": "user", "content": input}, {"role": "assistant",
                                                         "content": "You are firewall management assistant who adds , deletes and edits policies and rules"}]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=[" Human:", " AI:"]
        )
        reply= completion.choices[0]["message"]["content"]
        print(reply)
        messages = [{"role": "system",
                     "content": "You are a firewall Management center assistant,check if input from user has details to create rule for firewall, if yes, check the sample json object strictly and fill the details in sample object provided by user strictly ,add 'todo':'create' strictly if rule needs to be added, or add 'todo':'edit' if rule needs to be edited strictly.And generate output json based on the sample input strictly.If there are no details for firewall, output the user input as it is. "},
                    {"role": "user", "content": f"{reply}\n Sample json object:\n{firewall_data_str}"}, {"role": "assistant",
                                                                                   "content": "You are firewall management assistant who adds , deletes and edits policies and rules"}]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=[" Human:", " AI:"]
        )
        reply = completion.choices[0]["message"]["content"]
        print(reply)
        # input_2 = f"if below data: "+reply+" has json body, in it, please use the fetch the values from json body and create a json object by replacing parameters in create_check from context"
        # loader = JSONLoader(file_path='./schemas.json', jq_schema='.', text_content=False)
        # index = VectorstoreIndexCreator().from_loaders([loader])
        # reply = index.query(input, llm=ChatOpenAI())
        # input = "If user is asking to add a rule with below details: " + reply + " fetch json body from context and add values from user to the body and output in json format similar to context and generate output as json object."
        # loader = JSONLoader(file_path='./schemas.json', jq_schema='.', text_content=False)
        # index = VectorstoreIndexCreator().from_loaders([loader])
        # reply = index.query(input, llm=ChatOpenAI())
        # index_directory = './.chroma'
        #
        # # Delete the index by removing its files
        # shutil.rmtree(index_directory)
        api_input = verify_reply(reply)
        if api_input != False:
            call_api(api_input)
        return reply






inputs = gr.inputs.Textbox(lines=7, label="Chat with FirewallBot")
outputs = gr.outputs.Textbox(label="Reply")

gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs, title="Firewall Chatbot",
             description="Add firewall rules",
             theme="compact").launch(share=True)

#connection.close()
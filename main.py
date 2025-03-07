import openai
import gradio as gr
import os, json
import constants
from langchain.document_loaders import JSONLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
import pika
import get_screenshot
import bot_helper

config_file_path = './pfsense_config_APIFirewallRuleCreate.json'
rules_file_path = './rules.json'
new_rule_config_file = './new_rule.json'
json_separator = "FIREWALL_RULE"
rules_list = ""
config_file_path = 'pfsense_config_APIFirewallRuleCreate.json'
json_schema = ''


with open(config_file_path) as config_file:
    json_schema = config_file.read()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0,
                                                               blocked_connection_timeout=None,))
channel = connection.channel()
channel.queue_declare(queue='firewall_rules')

os.environ["OPENAI_API_KEY"] = constants.APIKEY
openai.api_key = constants.APIKEY


def call_api(api_input):
    channel.basic_publish(exchange='',
                      routing_key='firewall_rules',
                      body=str(api_input))
    print(f" [x] Sent {api_input} to be added to firewall rule")

context = [
    {
        "role": "system",
        "content":
            f"""
                        You are FireBot, an automated firewall management assistant.
                        You respond in a short, conversational and friendly style.
                        First check if user wants to add or edit or delete the firewall rule.

                        Get Rules:
                            If user wants to get rules, to get rules generate output as a strict json which includes a
                            key named 'todo' and value for this key as 'get' and key named 'confirm' with value 'yes'.

                        Show rules:
                            If user asks to show firewall rules, check if there is data in {rules_list}, fetch each rule
                            and output each rule, do not create json object.

                        Delete rules:
                            Based on the Description of rule that user provides that needs to be deleted, fetch
                            tracker ID of the rule from {rules_list} and create a strict json body with key 'todo'
                            having value 'delete' and key 'tracker' with value of tracker fetched from {rules_list}.

                        Create Rule:
                            If user wants to create firewall rule, check the parameters in the input given by user.
                            The required parameters are as given by the config in {json_schema}.
                            Determine which of the  input parameters should be matched to the required parameters, and
                            accordingly create a strict json for the new firewall rule.
                            If any of the required parameters are missing then -
                                1. Use default value from the config in {json_schema}.
                                2. Highlight the ones that were missing in user input, and let the user know that defaults
                                   will be used instead.

                            Value for parameter 'todo' should be 'create' if firewall rule needs to be created or added.
                            Value for parameter protocol should be in lowercase always strictly.
                            Once the user provides all the required parameters, create a json specification for firewall 
                            rule as specified by the config in {json_schema}.
                    
                            The output should also include a brief description and explanation about the created JSON
                            firewall rule specification.

                        The generated json should be enclosed by the separator {json_separator} before and after it.
                        After creating the output, ask the user for confirmation.
                        If the user confirms that they would like to perform the given action with this json,
                        then create a new output with just the generated strict json, and add new key 'confirm' with value as 'yes'. 

                        """
    },
    {
        "role": "assistant",
        "content": """I'm a firewall management assistant. I can help you add, delete or edits policies and
                   rules for pfsense firewall. How can I be of assistance?"""
    }

]

def chatbot(input):
    if input:
        if len(input) > 4:
            input = bot_helper.curtail_memory(input)
        audio=''
        try:
            rules_list = bot_helper.get_rules()
            rules_message = {"role":"system","content": "Rules Present in firewall latest are: "+str(rules_list)}
            input.append(rules_message)
        except Exception as err:
            print(err)
        try:
            get_screenshot.get_screenshot()
        except Exception as err:
            print(err)

        if ("hello") in input:
            audio = bot_helper.text_to_speech_2(bot_helper.welcome_message)
        reply = bot_helper.get_completion_from_messages(input)
        print(f'===== reply =====\n{reply}')

        input = f"""If there is data in json format in following data in double quotes "{reply}", output only the json body strictly no text"""
        loader = JSONLoader(file_path=config_file_path, jq_schema='.', text_content=False)
        index = VectorstoreIndexCreator().from_loaders([loader])
        reply_internal = index.query(input, llm=ChatOpenAI())

        print(f"===== reply_internal =====\n{reply_internal}")

        api_input = bot_helper.verify_reply(reply_internal)
        print(f"===== api_input =====\n{api_input}")

        if api_input:
            if "todo" in api_input.keys() and "confirm" in api_input:
                confirm = api_input["confirm"]
                message_call = api_input["todo"]
                if message_call == "create":
                    audio_out = "The given firewall rule has been created. Kindly verify the rule in pfsense Management Center, Thank you for working with me."
                elif message_call == "edit":
                    audio_out = "The given firewall rule has been edited. Kindly verify the rule in pfsense Management Center, Thank you for working with me."
                elif message_call == "delete":
                    audio_out = "The given firewall rule has been deleted. Kindly verify the rule in pfsense Management Center, Thank you for working with me."
                elif message_call == "get":
                    audio_out = "Kindly wait till I fetch the rules from firewall configuration."
                else:
                    audio_out =''
                if audio_out:
                    audio = bot_helper.text_to_speech_2(audio_out)

                if confirm == "yes":
                    call_api(api_input)

        images = get_screenshot.get_latestscreenshots()

        return reply, images[0], images[1], audio


with gr.Blocks(theme='freddyaboulton/dracula_revamped') as demo:
    images = get_screenshot.get_latestscreenshots()
    gr.Markdown("""<h1><center>Firewall management Assistant</center></h1>""")
    html = gr.HTML()
    html.visible = False
    chatbots = gr.Chatbot()
    input = gr.Textbox(label="Ask assistant a question")

    def respond(message, ui_chat_history):
        user_msg = {
            "role": "user",
            "content": message}
        context.append(user_msg)
        bot_message, latest_image, previous_image, audio = chatbot(context)
        assistant_message = {
            "role": "assistant",
            "content": bot_message
        }
        context.append(assistant_message)
        ui_chat_history.append((message, bot_message))
        return "", ui_chat_history, latest_image, previous_image, audio
    examples = gr.Examples(examples=["Hello","Get Firewall Rules.", "Show Firewall Rules", "Create a firewall rule to allow access to ip 192.168.1.10 from 10.64.10.1 with source port as 8081 and destination port as 8081, on wan interface, protocol tcp, Description: Allow access to Arjun for pfsense","Delete rule with description test"],
                           inputs=[input])
    with gr.Row():
        with gr.Column():
            gr.Markdown("""<h2><left>Previous Screenshot</left></h2>""")
            previous_image = gr.Pil(images[1], height=350, width=350)
        with gr.Column():
            gr.Markdown("""<h2><left>Latest Screenshot</left></h2>""")
            latest_image = gr.Pil(images[0], height=350, width=350)
    input.submit(fn=respond, inputs=[input,chatbots], outputs=[input,chatbots,latest_image, previous_image, html])
demo.launch(share=True)

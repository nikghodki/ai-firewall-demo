import pika, sys, os, json
import agent
import logging

create_schema = {
  "dst": "string",
  "dstport": "string",
  "interface": [
    "string"
  ],
  "ipprotocol": "inet",
  "protocol": "any",
  "src": "string",
  "srcport": "string",
  "type": "pass"
}

firewall_host_ip="35.185.19.16"
token='61646d696e'
key='fc9de5ea51838a087ca31974d43d1f7a'
authtoken = f"{token} {key}"
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='firewall_rules')

    def callback(ch, method, properties, body):
        print(f"Received message {body}")
        out = body.decode("utf8").replace("'","\"")
        input_schema = json.loads(out)
        uri = f"/api/v1/firewall/rule"
        endpoint = f"https://{firewall_host_ip}"
        header = {'Authorization': authtoken}
        input_schema, action = agent.fetch_action_rebuild_schema(input_schema)
        try:
            if action == "create":
                #if agent.verify_json(input_schema,create_schema) == True:
                if agent.create_fw_rule(input_schema, uri, endpoint, header) == True:
                    return True
            if action == "edit":
                if agent.verify_json(input_schema, edit_schema):
                    if agent.edit_fw_rule(input_schema, uri, endpoint, header):
                        return True
            if action == "delete":
                if agent.delete_fw_rule(str(input_schema["tracker"]), uri, endpoint, header):
                    return True
            if action == "get":
                rules = agent.get_fw_rule(uri, endpoint, header)
                try:
                    with open('../botservice/rules.json', 'w') as rules_file:
                        json.dump(json.loads(rules)['data'],rules_file)
                except Exception as err:
                    print(err)
                return True
        except Exception as err:
            logging.exception(err)
            return False


    channel.basic_consume(queue='firewall_rules', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
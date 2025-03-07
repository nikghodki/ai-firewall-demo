import pika

create_schema = {
  "todo": "create",
  "ackqueue": "string",
  "apply": "false",
  "defaultqueue": "string",
  "descr": "",
  "direction": "any",
  "disabled": "false",
  "dnpipe": "string",
  "dst": "string",
  "dstport": "string",
  "floating": "false",
  "gateway": "string",
  "icmptype": [
    "althost"
  ],
  "interface": [
    "string"
  ],
  "ipprotocol": "inet",
  "log": "false",
  "pdnpipe": "string",
  "protocol": "any",
  "quick": "false",
  "sched": "string",
  "src": "string",
  "srcport": "string",
  "statetype": "keep state",
  "tcpflags_any": "false",
  "tcpflags1": [
    "fin"
  ],
  "tcpflags2": [
    "fin"
  ],
  "top": "false",
  "type": ""
}

edit_schema = {
  "todo":"edit",
  "ackqueue": "string",
  "apply": "false",
  "defaultqueue": "string",
  "descr": "string",
  "direction": "in",
  "disabled": "true",
  "dnpipe": "string",
  "dst": "string",
  "dstport": "string",
  "floating": "true",
  "gateway": "string",
  "icmptype": [
    "althost"
  ],
  "interface": [
    "string"
  ],
  "ipprotocol": "inet",
  "log": "true",
  "pdnpipe": "string",
  "protocol": "any",
  "quick": "true",
  "sched": "string",
  "src": "string",
  "srcport": "string",
  "statetype": "keep state",
  "tcpflags_any": "true",
  "tcpflags1": [
    "fin"
  ],
  "tcpflags2": [
    "fin"
  ],
  "top": "false",
  "tracker": 0,
  "type": "pass"
}

get_schema = {"todo": "get"}

message =str(create_schema)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='firewall_rules')

channel.basic_publish(exchange='',
                      routing_key='firewall_rules',
                      body=message)
print(" [x] Sent data")
connection.close()


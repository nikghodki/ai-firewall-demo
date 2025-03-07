import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='firewall_rules')
channel.basic_publish(exchange='',
                      routing_key='firewall_rules',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

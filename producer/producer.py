import pika 
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel() 
channel.exchange_declare(exchange='exchange', exchange_type='direct')

channel.queue_declare(queue='health check')
channel.queue_declare(queue='stock')
channel.queue_declare(queue='order_processing')
channel.queue_declare(queue='item_creation')

binding_keys = ['health check', 'stock', 'order_processing', 'item_creation']
for binding_key in binding_keys:
    channel.queue_bind(exchange='exchange', queue=binding_key, routing_key=binding_key)

type = sys.argv[1]

if(type not in binding_keys):
    print("Invalid type")
    sys.exit(0)

if(type == 'health check'):
    message = ''.join(sys.argv[2:])
    channel.basic_publish(exchange='exchange', routing_key=type, body=message)
    print(f"Sent message: {type}:{message}")

elif(type == 'stock'):
    item_id = sys.argv[2]
    item_name = sys.argv[3]
    item_price = sys.argv[4]
    item_quantity = sys.argv[5]
    message = f"{item_id}:{item_name}:{item_price}:{item_quantity}"
    channel.basic_publish(exchange='exchange', routing_key=type, body=message)
    print("Sent message:",type,":",message)
    connection.close()
    

elif(type == 'order_processing'):
    type = sys.argv[1]
    item_id = sys.argv[2]
    item_name = sys.argv[3]
    item_price = sys.argv[4]
    item_quantity = sys.argv[5]

    message = f"{item_id}:{item_name}:{item_price}:{item_quantity}"
    channel.basic_publish(exchange='exchange', routing_key=type, body=message)
    print("Sent message:",type,":",message)
    connection.close() 



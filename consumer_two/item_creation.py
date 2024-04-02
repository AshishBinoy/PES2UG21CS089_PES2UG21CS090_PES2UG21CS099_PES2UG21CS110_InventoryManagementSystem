import mysql.connector 
import pika 

# DOES NOT WORK NEED TO FIX

#Creating MySQL Connection 
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "123456789")
cursor = mydb.cursor() 
cursor.execute("CREATE DATABASE IF NOT EXISTS Inventory")
cursor.execute("Use Inventory")
cursor.execute("CREATE TABLE IF NOT EXISTS Items (item_id INT AUTO_INCREMENT PRIMARY KEY, item_name VARCHAR(255), item_price FLOAT, item_quantity INT)")


#Creating RabbitMQ Connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='exchange', exchange_type='direct')
channel.queue_declare(queue='item_creation')
channel.queue_bind(exchange='exchange', queue='item_creation', routing_key='item_creation')

#Callback function
def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    item_id,item_name, item_price, item_quantity = body.decode('utf-8').split(":")
    cursor.execute("INSERT INTO Items (item_id,item_name, item_price, item_quantity) VALUES (%s, %s, %s, %s)", (item_id,item_name, item_price, item_quantity))
    mydb.commit()
    print(f"Item {item_name} added to the inventory")

print("Waiting for messages... press CTRL+C to exit")
channel.basic_consume(queue='item_creation', on_message_callback=callback, auto_ack=True)
channel.start_consuming() 
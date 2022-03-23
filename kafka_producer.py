import kafka
import config_loader

bootstrap_servers = config_loader.read('''data['kafka']['bootstrap_servers']''')
topicName = config_loader.read('''data['kafka']['topic']''')

producer = kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)
producer.send(topicName, b'start')
producer.flush()

with open("../Sender Data/stg.png", 'rb') as file:
    for line in file.readlines():
        producer.send(topicName, line)
        producer.flush()

producer.send(topicName, b'stop')
producer.flush()

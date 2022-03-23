import os.path
from datetime import datetime
import yaml
from kafka import KafkaConsumer,TopicPartition
import config_loader
import offset_manager

bootstrap_servers = config_loader.read('''data['kafka']['bootstrap_servers']''')
topicName = config_loader.read('''data['kafka']['topic']''')

consumer = KafkaConsumer(topicName, bootstrap_servers=bootstrap_servers, auto_offset_reset="earliest", auto_commit_interval_ms=1)

dir_path = config_loader.read('''data['environment']['receive_path']''')

try:
    offset = offset_manager.read('''data[''' +"'"+topicName+"'"+"]")
    print("Last offset that was read",offset)

except KeyError:
    offset=0
    print("new line added")
    with open("offset.yaml") as offset_file:
        data = yaml.safe_load(offset_file)
        datadict = dict(data)
        datadict[topicName] = 0

    with open("offset.yaml",'w') as offset_file:
        yaml.dump(datadict,offset_file)

except TypeError:
    offset = 0
    with open("offset.yaml") as offset_file:
        data = yaml.safe_load(offset_file)
        datadict = {topicName: 0}

    with open("offset.yaml", 'w') as offset_file:
        yaml.dump(datadict, offset_file)

# date = datetime.now().strftime("%Y_%m_%d-%I-%M_%S")

# if not os.path.isdir(config_loader.read('''data['environment']['receive_path']''')):
#     os.mkdir(config_loader.read('''data['environment']['receive_path']'''))

# ///////////////////////// Kafka topic offset retriever
PARTITIONS = []
for partition in consumer.partitions_for_topic(topicName):
    PARTITIONS.append(TopicPartition(topicName, partition))

topic_end_offsets = consumer.end_offsets(PARTITIONS)
topic_end_offsets = topic_end_offsets[TopicPartition(topic=topicName, partition=0)]
print("the last offset of the topic",topic_end_offsets)

#////////////////////////end of topic offset retriever

if topic_end_offsets-1 != offset:
    print('1')
    with open(dir_path, 'wb') as file:  # receiving messages from the consumer and writing
        inprogress = False  # to an image file with current timestamp
        for message in consumer:
            if message.offset > offset:

                if message.value == b'start' and inprogress is False:
                    # print('start offset')
                    # print(message)
                    inprogress = True
                    continue

                # if message.value == b'start' and inprogress is True:
                #     # print(message)
                #     # file.truncate(0)
                #
                #     with open("offset.yaml") as offset_file:
                #         data = yaml.safe_load(offset_file)
                #         data[topicName] = message.offset
                #
                #     with open("offset.yaml", 'w') as offset_file:
                #         yaml.dump(data, offset_file)
                #     exit(0)

                elif message.value == b'stop':  # saves the last offset read by the consumer
                    # print("end offset")
                    # print(message)

                    with open("offset.yaml") as offset_file:
                        data = yaml.safe_load(offset_file)
                        data[topicName] = message.offset

                    with open("offset.yaml", 'w') as offset_file:
                        yaml.dump(data, offset_file)
                    exit(0)

                else:
                    file.write(message.value)
                    # print(message)
else:
    print('0')


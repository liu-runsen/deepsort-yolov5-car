#_*_coding:UTF-8_*_

'''
@Author：Runsen
'''
import json

import pika
import time

auth = pika.PlainCredentials(
    username='guest',
    password='guest',
) # 用户名 / 密码



connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        '127.0.0.1', # RabbitMQ 地址
        5672, # 端口号
        '/', # 虚拟主机
        auth, # 验证
    )
) # 链接RabbitMQ
channel = connection.channel() # 创建RabbitMQ通道

channel.queue_declare(
    queue='hzairport', # 消费对列名
    durable=True, # 持久化
)


def callback(ch, method, properties, body):
    result =  json.loads(body)
    print(" [x] Received %r" % result["alert"])


channel.basic_consume(
    queue='hzairport', # 对列名
    auto_ack=True, # 自动回应
    on_message_callback=callback, # 回调消息
)


time.sleep(5) # 模拟消费时间
print("消费者")
channel.start_consuming()


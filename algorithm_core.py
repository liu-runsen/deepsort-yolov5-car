#_*_coding:UTF-8_*_
'''
@Author：Runsen
'''
import json

'''
@Author：Runsen


思路：初始长方形
计算：长方形的平均速度
判断第三个长方形的平均速度是不是小于平均速度，如果大于了，就进行报警处理

205  455  295 455
224  480  342 480
253  490  351 490
277  516  391 516
304  546  440 546
351  595  506 595
402  650  590 650
482  727  712 727


'''
import pika
import base64
import cv2
import tracker
from detector import Detector
from utils.utils import Point
# 导入点的位置
from utils import *

# 连接MQ
credentials = pika.PlainCredentials(
    username='guest',
    password='guest',
)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='127.0.0.1',  # MQ地址(本机)
        port=5672,  # 端口号,注意是5672,不是15672
        virtual_host='/',  # 虚拟主机
        credentials=credentials,  # 用户名/密码
    )
)


channel = connection.channel()
channel.queue_declare(
    queue='hzairport',  # 队列名
    durable=True,  # 使队列持久化
)




def Judge_overspeed(distance, first_time, second_time, third_time, fouth_time, fith_time, final_time):

    # if first_time and start_time:
    #     fisrt_speed = distance / (first_time - start_time)
    # else:
    #     fisrt_speed = 0

    if second_time and first_time:
        fisrt_speed = distance / (second_time - first_time)
    else:
        fisrt_speed = 0

    if third_time and second_time:
        second_speed = distance / (third_time - second_time)
    else:
        second_speed = 0

    if fouth_time and third_time:
        third_speed = distance / (fouth_time - third_time)
    else:
        third_speed = 0

    if fith_time and fouth_time:
        fouth_speed = distance / (fith_time - fouth_time)
    else:
        fouth_speed = 0

    if final_time and fith_time:
        last_speed = distance / (final_time - fith_time)
    else:
        print("什么辣鸡模型，这都检测不到")
        last_speed = 3

    print(fisrt_speed, second_speed, third_speed, fouth_speed, last_speed)
    # 计算平均速度

    # avg_speed = (fisrt_speed + second_speed + third_speed + fouth_speed  + last_speed) / 6
    #
    # speeds = [fisrt_speed, second_speed, third_speed, fouth_speed, last_speed]

    if last_speed > THRESHOLD_SPEED:
        alert =  True
    else:
        alert = False

    message = {
        "alert": alert,
    }
    return message





def alarm(video=None):
    # 初始化 yolov5
    detector = Detector()
    # 打开视频
    # video_path = r'rtsp://admin:nianguo2020@192.168.31.64:554/Streaming/Channels/101?transportmode=unicast'

    if video:
        capture = cv2.VideoCapture(video)
    else:
        # 显示摄像头
        capture = cv2.VideoCapture(0)
    # capture.set(5,capture.get(5))

    idx = 0
    fps = capture.get(5)
    divided = 0
    time = 0

    while True:
        # 读取每帧图片
        _, im = capture.read()

        if im is None:
            break
        # 缩小尺寸，1920x1080->960x540
        im = cv2.resize(im, (960, 540))

        list_bboxs = []

        # bboxes ： yolov5检测的点
        # eg: (93, 192, 116, 218, 'truck', tensor(0.61563, device='cuda:0')
        # x1, y1, x2, y2, lbl, conf
        bboxes = detector.detect(im)

        # 如果画面中 有bbox
        if len(bboxes) > 0:
            list_bboxs = tracker.update(bboxes, im)

        idx += 1
        divided = idx % fps

        if divided == 0: time += 1

        if len(list_bboxs) > 0:
            # ----------------------判断撞线----------------------
            for item_bbox in list_bboxs:
                x1, y1, x2, y2, label, track_id = item_bbox
                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                x = int((x1 + x2) / 2)
                y = y2

                # if poly1.contains(Point(2 * x, 2 * y)) and line1_value[y, x] == 1:
                #     start_time = time + (divided / fps)
                #     print(f'进入第一块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : start_time: {start_time}')

                # 同一车同一track_id

                if poly2.contains(Point(2 * x, 2 * y)) and line2_value[y, x] == 1 :
                    first_time = time + (divided / fps)
                    # spend_time_1 = first_time - start_time
                    print(f'进入第一块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {first_time}')

                    # try:
                    #     print(f'第一次进入时间： {start_time}')
                    # except:
                    #     start_time = 0
                    #     print(f'不存在：start_time 类别: {label} | id: {track_id} | 在进入第一块矩形没有检测到')
                    #


                if poly3.contains(Point(2 * x, 2 * y)) and line3_value[ y, x] == 1 and track_id == track_id and label == label:
                    second_time = time + (divided / fps)
                    # spend_time_2 = second_time - first_time
                    print(f'进入第二块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {second_time}')

                    try:
                        print(f'第一块花费的时间： {second_time - first_time }')
                    except:
                        print(f'不存在：first_time 类别: {label} | id: {track_id} | 在进入第一块矩形没有检测到')
                        first_time = 0


                if poly4.contains(Point(2 * x, 2 * y)) and line4_value[ y, x] == 1 and track_id == track_id and label == label:
                    third_time = time + (divided / fps)
                    print(f'进入第三块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {third_time}')

                    try:
                        print(f'第二块花费的时间： {third_time  - second_time}')
                    except:
                        print(f'不存在：second_time 类别: {label} | id: {track_id} | 在进入第二块矩形前没有检测到')
                        first_time = second_time = 0


                if poly5.contains(Point(2 * x, 2 * y)) and line5_value[
                    y, x] == 1 and track_id == track_id and label == label:
                    fouth_time = time + (divided / fps)
                    print(f'进入第五块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {fouth_time}')

                    try:
                        print(f'第四块花费的时间： {third_time - second_time}')
                    except:
                        print(f'不存在：third_time 类别: {label} | id: {track_id} | 在进入第三块矩形前没有检测到')
                        first_time = second_time = third_time = 0



                if poly6.contains(Point(2 * x, 2 * y)) and line6_value[
                    y, x] == 1 and track_id == track_id and label == label:
                    fith_time = time + (divided / fps)
                    print(f'进入第五块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {fith_time}')
                    try:
                        print(f'第五块花费的时间： {fouth_time - third_time}')
                    except:
                        print(f'不存在：fouth_time 类别: {label} | id: {track_id} | 在进入第四块矩形前没有检测到')

                        first_time = second_time = third_time = fouth_time = 0


                if poly7.contains(Point(2 * x, 2 * y)) and line7_value[ y, x] == 1 and track_id == track_id and label == label:
                    final_time = time + (divided / fps)
                    print(f'离开的时间:: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {final_time}')
                    message = Judge_overspeed(DISTANCE,first_time, second_time, third_time, fouth_time,fith_time, final_time)

                    # 二进制变成字符串
                    img_data = base64.b64encode(im).decode('utf-8')

                    print(message["alert"])
                    message["img"] = img_data
                    # 发消息队列
                    message = json.dumps(message)
                    channel.basic_publish(
                        exchange='',
                        routing_key='hzairport',  # 告诉rabbitmq将消息发送到 queue_name_test 队列中
                        body=message,  # 发送消息的内容
                        properties=pika.BasicProperties(delivery_mode=2, )  # 消息持久化
                    )




                while 750 < 2 * y < 800  and 600 < 2 * x < 750 and track_id == track_id and label == label:
                    print(f'idx time divided 变成 0')
                    idx = 0
                    fps = capture.get(5)
                    divided = 0
                    time = 0
                    break


    capture.release()
    cv2.destroyAllWindows()
    try:
        print(first_time, second_time, third_time, fouth_time, fith_time, final_time)
    except Exception as e:
        print(e)



alarm("./video/test.mp4")
alarm("./video/test1.mp4")
alarm("./video/test2.mp4")
alarm("./video/test4.mp4")
alarm("./video/test5.mp4")
alarm("./video/test6.mp4")
alarm("./video/test7.mp4")
alarm("./video/test8.mp4")
alarm("./video/test9.mp4")
alarm("./video/test10.mp4")
alarm("./video/test11.mp4")
alarm("./video/test12.mp4")
alarm("./video/test13.mp4")
alarm("./video/test14.mp4")
alarm("./video/test15.mp4")
alarm("./video/test16.mp4")
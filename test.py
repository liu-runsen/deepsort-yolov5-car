#_*_coding:UTF-8_*_

'''
@Author：Runsen
'''

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

import cv2
import tracker
from detector import Detector
from utils.utils import Point
# 导入点的位置
from utils import *
from algorithm_core import Judge_overspeed

def alarm_video(video):
    # 初始化 yolov5
    detector = Detector()
    # 打开视频
    capture = cv2.VideoCapture(video)
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
                if poly1.contains(Point(2 * x, 2 * y)) and line1_value[y, x] == 1:
                    start_time = time + (divided / fps)
                    print(f'进入第一块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : start_time: {start_time}')
                    try:
                        print(f'第一次进入时间： {start_time}')
                    except:
                        print(f'不存在：start_time 类别: {label} | id: {track_id} | 在进入第一块矩形没有检测到')
                # 同一车同一track_id

                if poly2.contains(Point(2 * x, 2 * y)) and line2_value[
                    y, x] == 1 and track_id == track_id and label == label:
                    first_time = time + (divided / fps)
                    # spend_time_1 = first_time - start_time
                    print(f'进入第二块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {first_time}')
                    try:
                        print(f'第一块花费的时间： {first_time - start_time}')
                    except:
                        print(f'不存在：start_time 类别: {label} | id: {track_id} | 在进入第一块矩形没有检测到')

                if poly3.contains(Point(2 * x, 2 * y)) and line3_value[
                    y, x] == 1 and track_id == track_id and label == label:
                    second_time = time + (divided / fps)
                    # spend_time_2 = second_time - first_time
                    print(f'进入第三块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {second_time}')
                    try:
                        print(f'第二块花费的时间： {second_time - first_time}')
                    except:
                        print(f'不存在：first_time 类别: {label} | id: {track_id} | 在进入第二块矩形前没有检测到')

                if poly4.contains(Point(2 * x, 2 * y)) and line4_value[
                    y, x] == 1 and track_id == track_id and label == label:
                    third_time = time + (divided / fps)
                    print(f'进入第四块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {third_time}')
                    try:
                        print(f'第四块花费的时间： {third_time - second_time}')
                    except:
                        print(f'不存在：second_time 类别: {label} | id: {track_id} | 在进入第三块矩形前没有检测到')

                if poly5.contains(Point(2 * x, 2 * y)) and line5_value[
                    y, x] == 1 and track_id == track_id and label == label:
                    fouth_time = time + (divided / fps)
                    print(f'进入第五块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {fouth_time}')

                    try:
                        print(f'第五块花费的时间： {fouth_time - third_time}')
                    except:
                        print(f'不存在：second_time 类别: {label} | id: {track_id} | 在进入第四块矩形前没有检测到')

                if poly6.contains(Point(2 * x, 2 * y)) and line6_value[
                    y, x] == 1 and track_id == track_id and label == label:
                    fith_time = time + (divided / fps)
                    print(f'进入第六块矩形类别: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {fith_time}')

                    try:
                        print(f'第六块花费的时间： {fith_time - fouth_time}')
                    except:
                        print(f'不存在：second_time 类别: {label} | id: {track_id} | 在进入第五块矩形前没有检测到')

                if poly7.contains(Point(2 * x, 2 * y)) and line7_value[y, x] == 1 and track_id == track_id and label == label:
                    final_time = time + (divided / fps)
                    print(f'离开的时间:: {label} | id: {track_id} | : 碰撞点的坐标 {x, y} | : time: {final_time}')
                while 2 * y >= 750  and track_id == track_id and label == label:
                    print(f'idx time divided 变成 0')
                    idx = 0
                    fps = capture.get(5)
                    divided = 0
                    time = 0
                    break


    capture.release()
    cv2.destroyAllWindows()
    try:
        print(start_time, first_time, second_time, third_time, fouth_time, fith_time, final_time)
    except Exception as e:
        print(e)

    return start_time, first_time, second_time, third_time, fouth_time, fith_time, final_time


start_time, first_time, second_time, third_time, fouth_time, fith_time, final_time = alarm_video('./video/test2.mp4')

print(Judge_overspeed(DISTANCE, start_time, first_time, second_time, third_time, fouth_time, fith_time, final_time))
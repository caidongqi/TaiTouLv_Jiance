
# !/usr/bin/python
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
#   This example shows how to run a CNN based face detector using dlib.  The
#   example loads a pretrained model and uses it to find faces in images.  The
#   CNN model is much more accurate than the HOG based model shown in the
#   face_detector.py example, but takes much more computational power to
#   run, and is meant to be executed on a GPU to attain reasonable speed.
#
#   You can download the pre-trained model from:
#       http://dlib.net/files/mmod_human_face_detector.dat.bz2
#
#   The examples/faces folder contains some jpg images of people.  You can run
#   this program on them and see the detections by executing the
#   following command:
#       ./cnn_face_detector.py mmod_human_face_detector.dat ../examples/faces/*.jpg
#
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#   or
#       python setup.py install --yes USE_AVX_INSTRUCTIONS --yes DLIB_USE_CUDA
#   if you have a CPU that supports AVX instructions, you have an Nvidia GPU
#   and you have CUDA installed since this makes things run *much* faster.
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake and boost-python installed.  On Ubuntu, this can be done easily by
#   running the command:
#       sudo apt-get install libboost-python-dev cmake
#
#   Also note that this example requires scikit-image which can be installed
#   via the command:
#       pip install scikit-image
#   Or downloaded from http://scikit-image.org/download.html.

import tkinter as tk
import time
from tkinter import ttk
import sys
import dlib
from skimage import io


window = tk.Tk()  # 这是一个窗口object
window.title('抬头率监测系统')
window.geometry('600x400')  # 窗口大小


def gettime():  # 当前时间显示
    timestr = time.strftime('%Y.%m.%d %H:%M', time.localtime(time.time()))
    lb.configure(text=timestr)
    window.after(1000, gettime)


lb = tk.Label(window, text='', font=("黑体", 20))
lb.grid(column=0, row=0)
gettime()

# 选择教室标签加下拉菜单
choose_classroom = tk.Label(window, text="选择教室", width=15, height=2, font=("黑体", 12)).grid(column=0, row=1, sticky='w')
class_room = tk.StringVar()
class_room_chosen = ttk.Combobox(window, width=20, height=10, textvariable=class_room, state='readonly')
class_room_chosen['values'] = ('N101', 'N103', 'S101', 'S103')
class_room_chosen.grid(column=1, row=1, sticky='w')

# 选择课时标签加下拉菜单
choose_time = tk.Label(window, text="选择课时", width=15, height=2, font=("黑体", 12)).grid(column=0, row=3, sticky='w')
course_time = tk.StringVar()
course_time_chosen = ttk.Combobox(window, width=20, height=10, textvariable=course_time, state='readonly')
course_time_chosen['values'] = ("周一一二节", "周一三四节", "周一五六节", "周一七八节")
course_time_chosen.grid(column=1, row=3, sticky='w')


# 检测人脸数核心函数
def inspect():
    str1 = "教室"
    str2 = "课上的抬头人数为："

    sys_argv=[r'C:\Users\86132\Desktop\dlib\dlib_data\mmod_human_face_detector.dat',
              r'C:\Users\86132\Desktop\dlib\dlib-master\examples\faces\1.jpg',
              r'C:\Users\86132\Desktop\dlib\dlib-master\examples\faces\3.jpg']
    '''
    if len(sys.argv) < 3:  # 如果检测输入的参数不够标准的三个，提示去获取模型文件
        print(
            "Call this program like this:\n"
            "   ./cnn_face_detector.py mmod_human_face_detector.dat ../examples/faces/*.jpg\n"
            "You can get the mmod_human_face_detector.dat file from:\n"
            "    http://dlib.net/files/mmod_human_face_detector.dat.bz2")
        exit()
    '''
    cnn_face_detector = dlib.cnn_face_detection_model_v1(sys_argv[0])  # 调用cnn_face_detection模型

    # win = dlib.image_window()

    for f in sys_argv[2:]:  # 处理sys.argv[2]地址处的图片
        print("Processing file: {}".format(f))
        img = io.imread(f)
        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.
        dets = cnn_face_detector(img, 1) # img中所有检测到的脸的数组
        '''cnn_face_detector
        This detector returns a mmod_rectangles object. This object contains a list of mmod_rectangle objects.
        These objects can be accessed by simply iterating over the mmod_rectangles object
        The mmod_rectangle object has two member variables, a dlib.rectangle object, and a confidence score.

        It is also possible to pass a list of images to the detector.
            - like this: dets = cnn_face_detector([image list], upsample_num, batch_size = 128)
        In this case it will return a mmod_rectangless object.
        This object behaves just like a list of lists and can be iterated over.
        '''
        a = len(dets)
        str3 = str(a)
        var.set(class_room_chosen.get() + str1 + course_time.get() + str2 + str3)
        # print("Number of faces detected: {}".format(len(dets)))
        # for i, d in enumerate(dets):
        #   print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
        #       i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))

        # rects = dlib.rectangles()
        # rects.extend([d.rect for d in dets])

        # win.clear_overlay()
        # win.set_image(img)
        # win.add_overlay(rects)
        # dlib.hit_enter_to_continue()


var = tk.StringVar()  # tkinter中的字符串
display = tk.Label(window, textvariable=var, font=('Arial', 12), width=38, height=10)
display.grid(column=1, row=5, sticky='w')

# Adding a Button
b = ttk.Button(window, text="Click Me!", command=inspect)
b.grid(column=0, row=5)

window.mainloop()

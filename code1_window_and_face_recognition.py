#!/usr/bin/env python
# coding: utf-8

# In[14]:


import cv2
import numpy as np
import sys, os, glob, numpy
from skimage import io
from PIL import Image, ImageTk
import tkinter as tk
import time
from tkinter import ttk
from tkinter import IntVar
import xlrd

##GUI代码
window = tk.Tk()  # 这是一个窗口object
window.title('抬头率监测系统')
window.geometry('600x400')  # 窗口大小


def read_data():
    path = r'C:\Users\10485\Desktop\head_detecting\py_excel.xlsx'

    # 打开文件
    data = xlrd.open_workbook(path)
    # path + '/' +file 是文件的完整路径
    # 获取表格数目
    # nums = len(data.sheets())
    # for i in range(nums):
    #     # 根据sheet顺序打开sheet
    #     sheet1 = data.sheets()[i]

    # 根据sheet名称获取
    sheet1 = data.sheet_by_name('Sheet1')
    sheet2 = data.sheet_by_name('Sheet2')
    # 获取sheet（工作表）行（row）、列（col）数
    nrows = sheet1.nrows  # 行
    ncols = sheet1.ncols  # 列
    # print(nrows, ncols)

    # 获取教室名称列表
    global room_name, time_name
    room_name = sheet2.col_values(0)
    time_name = sheet2.col_values(1)
    print(room_name)
    print(time_name)
    # 获取单元格数据
    # 1.cell（单元格）获取
    # cell_A1 = sheet2.cell(0, 0).value
    # print(cell_A1)
    # 2.使用行列索引
    # cell_A2 = sheet2.row(0)[1].value


read_data()


def gettime():  # 当前时间显示
    timestr = time.strftime('%Y.%m.%d %H:%M', time.localtime(time.time()))
    lb.configure(text=timestr)
    window.after(1000, gettime)


lb = tk.Label(window, text='', font=("黑体", 20))
lb.grid(column=0, row=0)
gettime()








# In[ ]:


# 选择教室标签加下拉菜单
choose_classroom = tk.Label(window, text="选择教室", width=15, height=2, font=("黑体", 12)).grid(column=0, row=1, sticky='w')
class_room = tk.StringVar()
class_room_chosen = ttk.Combobox(window, width=20, height=10, textvariable=class_room, state='readonly')
class_room_chosen['values'] = room_name
class_room_chosen.grid(column=0, row=1, sticky='e')

# 选择课时标签加下拉菜单
choose_time = tk.Label(window, text="选择课时", width=15, height=2, font=("黑体", 12)).grid(column=0, row=2, sticky='w')
course_time = tk.StringVar()
course_time_chosen = ttk.Combobox(window, width=20, height=10, textvariable=course_time, state='readonly')
course_time_chosen['values'] = time_name
course_time_chosen.grid(column=0, row=2, sticky='e')

pic_tip = tk.Label(window, text="所选教室时实图像", width=16, height=2, font=("黑体", 12)).grid(column=1, row=2, sticky='s')

img = r'C:\Users\10485\Desktop\head_detecting\faces\1.jpg'
img_open = Image.open(img)
# 显示图片的代码
(x, y) = img_open.size  # read image size
x_s = 200  # define standard width
y_s = y * x_s // x  # calc height based on standard width
img_adj = img_open.resize((x_s, y_s), Image.ANTIALIAS)
img_png = ImageTk.PhotoImage(img_adj)

Image2 = tk.Label(window, bg='white', bd=20, height=y_s * 0.83, width=x_s * 0.83,
                  image=img_png)  ##0.83用来消除白框
Image2.grid(column=1, row=4, sticky='w')

flag = IntVar()
flag.set(0)

'''
    if(flag.get()!=0):
    pic_path = str(flag.get())+'.jpg'

    img_open = Image.open(img)
    # 显示图片的代码
    (x, y) = img_open.size  # read image size
    x_s = 200  # define standard width
    y_s = y * x_s // x  # calc height based on standard width
    img_adj = img_open.resize((x_s, y_s), Image.ANTIALIAS)
    img_png = ImageTk.PhotoImage(img_adj)
    Image2 = tk.Label(window, bg='black', bd=20, height=y_s * 0.83, width=x_s * 0.83, imagevariable=img_png)  ##0.83用来消除白框
    Image2.grid(column=1, row=4, sticky='w')
'''
face = 0


def rate_cal():
    path = r'C:\Users\10485\Desktop\head_detecting\py_excel.xlsx'
    data = xlrd.open_workbook(path)
    sheet1 = data.sheet_by_name('Sheet1')
    nrows = sheet1.nrows  # 行
    ncols = sheet1.ncols  # 列
    total = 0
    for i in range(nrows):
        if (sheet1.cell(i, 0).value == class_room_chosen.get() and sheet1.cell(i, 1).value == course_time_chosen.get()):
            total = sheet1.cell(i, 2).value
    print(total)
    global rate
    rate = face / total
    print(rate)



def pic_re():
    if (flag.get() == 0):
        pic_path = str(class_room_chosen.get()) + str(course_time_chosen.get()) + '.jpg'
        img = os.path.join(r'C:\Users\10485\Desktop\head_detecting\faces', pic_path)
        img_open = Image.open(img)
        # 显示图片的代码
        (x, y) = img_open.size  # read image size
        global x_s
        global y_s
        x_s = 200  # define standard width
        y_s = y * x_s // x  # calc height based on standard width
        img_adj = img_open.resize((x_s, y_s), Image.ANTIALIAS)
        global img_png  ##这里一定要设置为全局变量，不然图片无法正常显示！！！！！！！！！！！
        img_png = ImageTk.PhotoImage(img_adj)
        Image2.configure(image=img_png)
    window.update_idletasks()


def inspect():
    str1 = "教室"
    str2 = "课上的抬头人数为："
    path = r'C:\Users\10485\Desktop\head_detecting\faces'
    pic_path = str(class_room_chosen.get()) + str(course_time_chosen.get()) + '.jpg'
    p = path +'/'+pic_path
    img = cv2.imread(p)
    color = (0, 255, 0)

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    classfier = cv2.CascadeClassifier(
        r"C:\Users\10485\Desktop\head_detecting\haarcascade_frontalface_alt2.xml")
    faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    a = len(faceRects)
    global face
    face = a
    str3 = str(a)
    var.set(class_room_chosen.get() + str1 + course_time.get() + str2 + str3)


var = tk.StringVar()  # tkinter中的字符串
display = tk.Label(window, textvariable=var, font=('Arial', 12), width=38, height=10)
display.grid(column=0, row=4, sticky='n')

# Adding a Button
b = ttk.Button(window, text="Click Me!", command=inspect)
b.grid(column=0, row=4)

rate_button = ttk.Button(window, text="Get_rate", command=rate_cal).grid(column=0, row=6)

pic_button = ttk.Button(window, text="Updata picture", command=pic_re).grid(column=0, row=5)
window.mainloop()


# In[ ]:





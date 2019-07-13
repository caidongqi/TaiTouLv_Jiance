
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
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk


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
class_room_chosen.grid(column=0,row=1, sticky='e')

# 选择课时标签加下拉菜单
choose_time = tk.Label(window, text="选择课时", width=15, height=2, font=("黑体", 12)).grid(column=0, row=2, sticky='w')
course_time = tk.StringVar()
course_time_chosen = ttk.Combobox(window, width=20, height=10, textvariable=course_time, state='readonly')
course_time_chosen['values'] = ("周一一二节", "周一三四节", "周一五六节", "周一七八节")
course_time_chosen.grid(column=0, row=2, sticky='e')

pic_tip = tk.Label(window,text="所选教室时实图像",width=16,height=2,font=("黑体",12)).grid(column=1,row=2,sticky='s')
#显示图片的代码
img = r'C:\Users\86132\Desktop\dlib\dlib-master\examples\faces\1.jpg'

img_open = Image.open(img)
(x,y) = img_open.size #read image size
x_s = 200 #define standard width
y_s = y * x_s // x #calc height based on standard width
img_adj=img_open.resize((x_s,y_s),Image.ANTIALIAS)
img_png = ImageTk.PhotoImage(img_adj)


Image2 = tk.Label(window, bg='white', bd=20, height=y_s*0.83 ,width=x_s*0.83, image=img_png)##0.83用来消除白框
Image2.grid(column=1,row=4,sticky='w')



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
        dets = (img, 1)  # img中所有检测到的脸的数组    待删除
        ##dets = cnn_face_detector(img, 1) # img中所有检测到的脸的数组
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
display.grid(column=0, row=4, sticky='n')

# Adding a Button
b = ttk.Button(window, text="Click Me!", command=inspect)
b.grid(column=0, row=4)

window.mainloop()
void
SMG_Init(void)
{
    GPIO_InitTypeDef
GPIO_InitStructure;

RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC, ENABLE); // 开启GPIO时钟

GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1 | GPIO_Pin_2 \
                              | GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_5;
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT; // 输出模式
GPIO_InitStructure.GPIO_OType = GPIO_OType_PP; // 推挽输出
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; // 速度设置为50MHz
GPIO_Init(GPIOC, & GPIO_InitStructure);
}

int main(void)
{
NVIC_PriorityGroupConfig(NVIC_PriorityGroup_0);// 初始化 NVIC 分组
EXTI_Configure();//初始化中断向量和拨码开关
Delay_Init(); //初始化延时函数
SMG_Init(); //初始化数码管
while(1)
 {
SMG_Display();//点亮一个数码管
if(Flag == 1)
{
Draw_Data_number();//¸将学号传输到数码管当中，并显示
}
else
{
Draw_Data_null();//¸熄灭数码管
}
 }
}

 uint8_t
 digivalue[] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07 //
 0x00

 , 0x7f, 0x6f, 0x77, 0x7c, 0x39, 0x5e, 0x79, 0x71, 0x00};
 uint8_t
 smg_data[8] = {0x00, 0x01, 0x00, 0x06, 0x00, 0x04, 0x00, 0x07};//此处为两人的学号数据
 void
 SMG_Sele(uint8_t
 index)
 {
 HC595_Send(digivalue[smg_data[index]]);
 switch(index)
 {
     case
 0: \
     HC138_C = 0;
 HC138_B = 0;
 HC138_A = 0;
 break;
 case
 1:
 HC138_C = 0;
 HC138_B = 0;
 HC138_A = 1;
 break;
case
2:
HC138_C = 0;
HC138_B = 1;
HC138_A = 0;
break;
case
3:
HC138_C = 0;
HC138_B = 1;
HC138_A = 1;
break;
case
4:
HC138_C = 1;
HC138_B = 0;
HC138_A = 0;
break;
case
5:
HC138_C = 1;
HC138_B = 0;
HC138_A = 1;
break;
case
6:
HC138_C = 1;
HC138_B = 1;
HC138_A = 0;
break;
case
7:
HC138_C = 1;
HC138_B = 1;
HC138_A = 1;
break;
default:
break;
}
}

 void
 SMG_Display(void)
 {
 static
 uint8_t
 i = 0;
 SMG_Sele(i); // 进行位选
 i + +;
 i &= 0x07;
}




void
 EXTI0_IRQHandler(void)
 {
 // 判断中断线是否触发中断
 if (EXTI_GetITStatus(EXTI_Line0))
     {
     // 判断两开关是否同时闭合
     if (GPIO_ReadInputDataBit(GPIOF, GPIO_Pin_1) == 0 & &
         GPIO_ReadInputDataBit(GPIOF, GPIO_Pin_0) == 0)
     {
         flag = 1;
     EXTI_ClearITPendingBit(EXTI_Line0); // 清除相应中断线中断标
     志位
     }
     else
     {
         flag = 0;
     EXTI_ClearITPendingBit(EXTI_Line1); // 清除相应中断线中断标
     志位
     }
     }
     }
     void
     EXTI1_IRQHandler(void)
     {
     // 判断中断线是否触发中断
 if (EXTI_GetITStatus(EXTI_Line1))
     {
     // 判断两开关是否同时闭合
     if (GPIO_ReadInputDataBit(GPIOF, GPIO_Pin_1) == 0 & &
         GPIO_ReadInputDataBit(GPIOF, GPIO_Pin_0) == 0)
     {
         flag = 1;
     EXTI_ClearITPendingBit(EXTI_Line1); // 清除相应中断线标志位
     }
     else
     {
         flag = 0;
     EXTI_ClearITPendingBit(EXTI_Line1); // 清除相应中断线标志位
     }
     }
     }

 void
 EXTI_Configure(void)
 {
 GPIO_InitTypeDef
 GPIO_TypeDefStructure;
 EXTI_InitTypeDef
 EXTI_TypeDefStructure;
 NVIC_InitTypeDef
 NVIC_TypeDefStructure;
 // 开启中断输入端口时钟
 RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOF, ENABLE);
 // 开启外部中断时钟（系统配置时钟）
 RCC_APB2PeriphClockCmd(RCC_APB2Periph_SYSCFG, ENABLE);
 GPIO_TypeDefStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1; // 要初始化的端口
 GPIO_TypeDefStructure.GPIO_Mode = GPIO_Mode_IN; // 通用输入模式
 GPIO_TypeDefStructure.GPIO_PuPd = GPIO_PuPd_UP; // 上拉
 GPIO_Init(GPIOF, & GPIO_TypeDefStructure); // 初始化配置
 // GPIO
 中断线关联
 SYSCFG_EXTILineConfig(EXTI_PortSourceGPIOF, EXTI_PinSource0);
 SYSCFG_EXTILineConfig(EXTI_PortSourceGPIOF, EXTI_PinSource1);
 // 中断线配置
 // 所用
 EXTI
 中断编号是
 EXTI_Line0, EXTI_Line1
EXTI_TypeDefStructure.EXTI_Line = EXTI_Line0 | EXTI_Line1;
EXTI_TypeDefStructure.EXTI_Mode = EXTI_Mode_Interrupt;
EXTI_TypeDefStructure.EXTI_Trigger = EXTI_Trigger_Rising_Falling; // 上升下降
沿触发
EXTI_TypeDefStructure.EXTI_LineCmd = ENABLE;
EXTI_Init( & EXTI_TypeDefStructure);
（2）函数分析
本函数设置了两个中断线
EXTI_Line0, EXTI_Line1，并对外部中断进行了相应的配置，
如打开时钟，初始化
GPIO
模块，设置外部中断触发方式，设置中断向量优先级等。
特别地，设置两中断响应优先级不同，这样当两中断同时发生时，会有先后执行顺序。
// 中断向量优先级配置
NVIC_TypeDefStructure.NVIC_IRQChannel = EXTI0_IRQn;
NVIC_TypeDefStructure.NVIC_IRQChannelPreemptionPriority = 0; // 抢占优先级
NVIC_TypeDefStructure.NVIC_IRQChannelSubPriority = 7; // 响应优先级
// 设置
IRQ
通道中断使能
NVIC_TypeDefStructure.NVIC_IRQChannelCmd = ENABLE;
NVIC_Init( & NVIC_TypeDefStructure);
NVIC_TypeDefStructure.NVIC_IRQChannel = EXTI1_IRQn;
NVIC_TypeDefStructure.NVIC_IRQChannelPreemptionPriority = 0; // 抢占优先级
NVIC_TypeDefStructure.NVIC_IRQChannelSubPriority = 6; // 响应优先级
// 设置
IRQ
通道中断使能
NVIC_TypeDefStructure.NVIC_IRQChannelCmd = ENABLE;
NVIC_Init( & NVIC_TypeDefStructure);
}
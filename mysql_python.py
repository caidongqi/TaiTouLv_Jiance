import pymysql
import tkinter as tk
from tkinter import ttk

code=[]


##获取供应商编码
def get_code():
    #连接数据库
    db = pymysql.connect("localhost", "root", "12345678", "exp_4")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT ProviderID from provider"

    global code  # code是进货商编码，之后会放在下拉菜单中。
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print("Get the ProviderID")
        code = results

    except:
        # 如果连接失败
        print("Error: unable to fetch data")
    # 关闭连接
    db.close()


get_code()

window = tk.Tk()   # 这是一个窗口object
window.title('商品录入系统')
window.geometry('600x300')   # 窗口大小

# 布置页面标签，place用来页面布局
tip = tk.Label(window,text="请输入您的商品信息:",width=20,height=2).place(x=0,y=0)

lb1 = tk.Label(window, text="进货编码", width=8, height=2)
lb1.place(x=150, y=0)

e1 = tk.Entry(window,  width=8,)
e1.place(x=150, y=35)

lb2 = tk.Label(window, text="商品编码", width=8, height=2)
lb2.place(x=220, y=0)

e2 = tk.Entry(window,  width=8)
e2.place(x=220, y=35)

lb3 = tk.Label(window, text="进货日期", width=8, height=2)
lb3.place(x=290, y=0)

e3 = tk.Entry(window,  width=8)
e3.place(x=290, y=35)


lb4 = tk.Label(window, text="进货数量", width=8, height=2)
lb4.place(x=360, y=0)

e4 = tk.Entry(window,  width=8)
e4.place(x=360, y=35)

lb5 = tk.Label(window, text="进货单价", width=8, height=2)
lb5.place(x=430, y=0)

e5 = tk.Entry(window,  width=8)
e5.place(x=430, y=35)

lb6 = tk.Label(window, text="供应商编码", width=8, height=2)
lb6.place(x=500, y=0)

# 创建下拉菜单，并将get_code()中所得到的供应商编码填入
Code_already = tk.StringVar()
GYSbm = ttk.Combobox(window, width=8, height=2, textvariable=Code_already, state='readonly')
GYSbm['values'] = code
GYSbm.place(x=500,y=35)

def insert():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "12345678", "exp_4")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL插入语句
    sql = "INSERT INTO stock(StockID,ProductID,StockDate,StockQuantity,StockPrice,ProviderID) VALUES(%s,%s,%s,%s,%s,%s)"

    # 获取表中已有的进货编码
    cursor.execute("SELECT StockID FROM stock")
    check_date = cursor.fetchall()

    # 创建一个已有进货编码列表
    connect_date = ()
    for i in check_date:
        connect_date = connect_date+i

    # 错误检测，若无进货编码，提示输入，若重复，提示重新输入。
    if e1.get() == "":
        print("Please input StockID!")
    elif int(e1.get()) in connect_date:

        print("The commodity already exists.")
    else:
        try:
            # 执行SQL语句

            cursor.execute(sql%(str(e1.get()),str(e2.get()),str(e3.get()),str(e4.get()),str(e5.get()),str(GYSbm.get())))

            db.commit()
            # 获取所有记录列表
            print("Insert completes.")
        except:
            print("Error: unable to fetch data")


    # 关闭数据库连接
    db.close()




b1 = tk.Button(window, text="确认录入", width=15, height=2, command=insert)
b1.place(x=150, y=100)
window.mainloop()






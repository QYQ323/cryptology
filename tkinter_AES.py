# -*- coding: utf-8 -*-
import AES
import tkinter as tk  # 使用Tkinter前需要先导入

# 第1步，实例化object，建立窗口window
window = tk.Tk()
window.title('AES 工具')
window.geometry('700x360')
l = tk.Label(window, text='明文：', font=('Arial', 12), width=15, height=1)
L = tk.Label(window, text='密文：', font=('Arial', 12), width=15, height=1)
r = tk.Label(window, text='密钥：', font=('Arial', 12), width=15, height=1)
t = tk.Label(window, text='输出明文：', font=('Arial', 12), width=11, height=1)
T = tk.Label(window, text='输出密文：', font=('Arial', 12), width=11, height=1)
l.pack(anchor='w',ipady=20)
L.pack(anchor='w',pady=5)
r.pack(anchor='w',pady=20)
t.pack(anchor='w',pady=11)
T.pack(anchor='w',pady=13)

ming = tk.StringVar()
entry_ming = tk.Entry(window, textvariable=ming, font=('Arial', 13),width=55)
entry_ming.place(x=100,y=20)

mi = tk.StringVar()
entry_mi = tk.Entry(window, textvariable=mi, font=('Arial', 13),width=55)
entry_mi.place(x=100,y=70)

key = tk.StringVar()
entry_key = tk.Entry(window, textvariable=key, font=('Arial', 13),width=55)
entry_key.place(x=100,y=120)

result = tk.Text(window,font=('Arial', 12),width=55,height=1.47)
result.place(x=100,y=175)

Result = tk.Text(window,font=('Arial', 12),width=55,height=1.47)#输出密文，放下边
Result.place(x=100,y=223)

def begin_Encrypt():
    mingwen = ming.get()
    Key = key.get()
    list2 = AES.AES(Key,mingwen,1)
    str2 = "".join(list2)
    result.delete(1.0, "end")
    Result.delete(1.0, "end")
    Result.insert(1.0,str2)

#输出明文，放上边
def begin_Decrypt():
    miwen = mi.get()
    Key = key.get()
    list2 = AES.AES(Key,miwen,0)
    str2 = "".join(list2)
    Result.delete(1.0, "end")
    result.delete(1.0, "end")
    result.insert(1.0, str2)


btn_jiami = tk.Button(window, text='加 密',font=('Arial', 10),width=5,command=begin_Encrypt)
btn_jiami.place(x=625, y=17)
btn_jiemi = tk.Button(window, text='解 密',font=('Arial', 10),width=5,command=begin_Decrypt)
btn_jiemi.place(x=625, y=65)

# 第4步，在图形界面上创建 500 * 200 大小的画布并放置各种元素
#canvas = tk.Canvas(window, height=200, width=700)
# 说明图片位置，并导入图片到画布上
#image_file = tk.PhotoImage(file='111.png')  # 图片位置（相对路径，与.py文件同一文件夹下，也可以用绝对路径，需要给定图片具体绝对路径）
#image = canvas.create_image(625, 0, anchor='n', image=image_file)  # 图片锚定点（n图片顶端的中间点位置）放在画布（250,0）坐标处

#canvas.pack()

# 第6步，触发函数，用来一定指定图形
'''
def moveit():
    canvas.move(image, 2, 2)  # 移动正方形rect（也可以改成其他图形名字用以移动一起图形、元素），按每次（x=2, y=2）步长进行移动
'''

# 第5步，定义一个按钮用来移动指定图形的在画布上的位置
#b = tk.Button(window, text='move item', command=moveit).pack()

window.mainloop()
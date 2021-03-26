# -*- coding: utf-8 -*-
import DES
import tkinter as tk  # 使用Tkinter前需要先导入

# 第1步，实例化object，建立窗口window
window = tk.Tk()
window.title('DES 工具')
window.geometry('800x160')
l = tk.Label(window, text='明文/密文：', font=('Arial', 12), width=11, height=1)
r = tk.Label(window, text='密钥：', font=('Arial', 12), width=15, height=1)
t = tk.Label(window, text='结果：',font=('Arial', 12), width=15, height=1)
l.pack(anchor='w',ipady=20)
r.pack(anchor='w',pady=5)
t.pack(anchor='w',pady=15)

ming_or_mi = tk.StringVar()
entry_ming_or_mi = tk.Entry(window, textvariable=ming_or_mi, font=('Arial', 13),width=65)
entry_ming_or_mi.place(x=100,y=20)

key = tk.StringVar()
entry_key = tk.Entry(window, textvariable=key, font=('Arial', 13),width=65)
entry_key.place(x=100,y=70)

result = tk.Text(window,font=('Arial', 12),width=65,height=1.4)
result.place(x=100,y=116)
#加密
def Encrypt():
    mingwen = ming_or_mi.get()
    Key = key.get()
    list2 = DES.DES("0",mingwen, Key)
    str2 = "".join(list2)
    result.delete(1.0, "end")#结果输入前先将输出框清空
    result.insert(1.0,str2)
#解密
def Decrypt():
    miwen = ming_or_mi.get()
    Key = key.get()
    list2 = DES.DES("1",miwen, Key)
    str2 = "".join(list2)
    result.delete(1.0, "end")#结果输入前先将输出框清空
    result.insert(1.0, str2)

btn_jiami = tk.Button(window, text='加 密',font=('Arial', 10),width=5,command=Encrypt)
btn_jiami.place(x=720, y=17)
btn_jiemi = tk.Button(window, text='解 密',font=('Arial', 10),width=5,command=Decrypt)
btn_jiemi.place(x=720, y=65)

window.mainloop()
# -*- coding: utf-8 -*-

#密钥扩展函数
#CipherKey是一个4字的数组，W是一个44字的数组
#输入的密钥是32位的16进制，也就是要先分成4个字
def KeyExpansion(CipherKey):
    C = list(CipherKey)
    c = [[],[],[],[]]
    for i in range(32):
        if i < 8:#每8位放一个列表
            c[0].append(C[i])
        elif i < 16:
            c[1].append(C[i])
        elif i < 24:
            c[2].append(C[i])
        else:
            c[3].append(C[i])
    for i in range(4):
        c[i] = ''.join(c[i])#把c[i]由列表化为字符串，字符串长8位

    W = [0 for i in range(44)]
    #为了增大效率，将计算得出的倍增函数结果直接存储
    #b列表存放计算之后的轮常数Rcon,RC[0]...
    b = ['01000000','02000000', '04000000', '08000000', '10000000', '20000000',
         '40000000', '80000000', '1b000000', '36000000', '6c000000']
    for i in range(4):#前4个字就是首轮密钥
        W[i] = c[i]
    #开始扩展
    for i in range(4,44):
        Temp = W[i-1]
        if i%4==0:
            a = Rotl(Temp)#a为一个8位的字符串，对一个字里的字节以字节为单位进行循环移位的函数
            x = SubByte(a)#输入一个8位的16进制，也就是一个字，S盒变换
            Temp = yihuo_32(x,b[(i//4)-1])

        W[i] = yihuo_32(W[i - 4], Temp)
    return W #生成扩展密钥

#两个8位16进制数，即32位2进制的异或运算
def yihuo_32(a0,a1):
    A = []
    ten_a0 = int(a0,16)
    ten_a1 = int(a1, 16)
    ten_bin_a0 = '{:032b}'.format(ten_a0)
    ten_bin_a1 = '{:032b}'.format(ten_a1)
    list_a0 = list(ten_bin_a0)
    list_a1 = list(ten_bin_a1)
    for i in range(32):
        a = int(list_a0[i])^int(list_a1[i])
        A.append(a)
    c_1 = [str(i) for i in A]
    c = ''.join(c_1)
    c = int(c, 2)
    c = '{:08x}'.format(c)#这一步16进制没规定规格坑死人
    return c

#2个8位2进制的异或运算，两位16进制
def yihuo_16(a0,a1):#2位16进制
    A = []
    ten_a0 = int(a0,16)
    ten_a1 = int(a1,16)
    ten_bin_a0 = '{:08b}'.format(ten_a0)
    ten_bin_a1 = '{:08b}'.format(ten_a1)
    list_a0 = list(ten_bin_a0)
    list_a1 = list(ten_bin_a1)
    for i in range(8):
        a = int(list_a0[i])^int(list_a1[i])
        A.append(a)
    c_1 = [str(i) for i in A]
    c = ''.join(c_1)
    c = int(c, 2)
    c = '{:02x}'.format(c)
    return c

#左循环移位函数，输入一个字，以字节为单位左移，输出也是一个字的字符串
#对一个字里的字节以字节为单位进行循环移位的函数
def Rotl(W):
    a = list(W)#有八位
    a = a[2:] + a[:2]#左移两位16进制数
    b = ''.join(a)#重新转换为字符串
    return b
#输入8位的16进制，也就是一个字
#S盒运算
def SubByte(E,flag=1):#flag默认为1是加密
    if flag == 1:
        S = ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76',
             'ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0',
             'b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15',
             '04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'e8', '27', 'b2', '75',
             '09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84',
             '53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf',
             'd0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8',
             '51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2',
             'cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73',
             '60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db',
             'e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79',
             'e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08',
             'ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a',
             '70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e',
             'e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df',
             '8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']
    else:#逆S盒表
        S = ['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb',
             '7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb',
             '54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e',
             '08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25',
             '72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92',
             '6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84',
             '90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06',
             'd0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b',
             '3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73',
             '96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e',
             '47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b',
             'fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4',
             '1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f',
             '60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef',
             'a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61',
             '17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']
    A = []
    e = list(E)#len(e)=8
    if len(e) == 8:
        for i in  range(0,8,2):#每次加2
            a = int(e[i],16)#高位16进制转换为10进制
            b = int(e[i+1],16)#低位16进制转换为10进制
            c = S[a*16+b]#找到对应的16进制
            A.append(c)
        B = ''.join(A)
    else:
        for i in range(0, 32, 2):  # 每次加2
            a = int(e[i], 16)  # 高位16进制转换为10进制
            b = int(e[i + 1], 16)  # 低位16进制转换为10进制
            c = S[a * 16 + b]  # 找到对应的16进制
            A.append(c)
        B = ''.join(A)
    return B

#轮密钥加函数，输入状态和密钥,RoundKey是32位字符串
#轮密钥与经过列混合之后的数相加
#RoundKey是32位16进制
def AddRoundKey(State,RoundKey):
    k = list(RoundKey)
    d = list(State)
    E = []
    for i in range(32):
        a = int(k[i], 16)#16进制转换为10进制
        b = int(d[i], 16)
        e =a ^ b        #10进制可以进行异或
        e = format(e,'x')#异或后的值转换为16进制
        E.append(e)     #16进制以列表存放
    E =''.join(E)       #转换为字符串
    return E

#行移位变换函数
def ShiftRow(B,flag=1):
    A = list(B)
    r0 = []
    r1 = []
    r2 = []
    r3 = []
    R = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in  range(0,32,2):#每次加2
        if i%8 == 0:#处理第0行
            a = A[i]#'6'
            b = A[i+1]#'3'
            a = a + b#'63'
            r0.append(a)
        elif i%8 == 2:#处理第1行
            a = A[i]
            b = A[i + 1]
            a = a + b
            r1.append(a)
        elif i%8 == 4:#处理第2行
            a = A[i]
            b = A[i + 1]
            a = a + b
            r2.append(a)
        else:#处理第3行
            a = A[i]
            b = A[i + 1]
            a = a + b
            r3.append(a)
    if flag == 1:
        r1 = r1[1:] + r1[:1]#第1行循环左移一个字节
        r2 = r2[2:] + r2[:2]#第2行循环左移两个字节
        r3 = r3[3:] + r3[:3]#第3行循环左移三个字节
    else:
        r1 = r1[3:] + r1[:3]  # 第1行循环左移一个字节
        r2 = r2[2:] + r2[:2]  # 第2行循环左移两个字节
        r3 = r3[1:] + r3[:1]  # 第3行循环左移三个字节
    for i in range(16):
        if i%4 == 0:
            R[i] = r0[i//4]
        elif i%4 == 1:
            R[i] = r1[(i-1)//4]
        elif i%4 ==2:
            R[i] = r2[(i-2)//4]
        else:
            R[i] = r3[(i-3)//4]
    r = ''.join(R)
    #print(r)
    return r
#列混合变换函数
def MixColumn(r,flag=1):
    r = list(r)
    A0 = []
    A1 = []
    A2 = []
    A3 = []
    B0 = [0,0,0,0]
    B1 = [0,0,0,0]
    B2 = [0,0,0,0]
    B3 = [0,0,0,0]
    D = [0,0,0,0]
    E = [0,0,0,0]
    for i in range(0,32,2):
        if i < 8:
            a = r[i]
            b = r[i+1]
            a = a + b #a=63
            A0.append(a)#A0=[63,e0,63,89]
        elif i<16:
            a = r[i]
            b = r[i + 1]
            a = a + b
            A1.append(a)#A1=['51','7c','63','63']
        elif i < 24:
            a = r[i]
            b = r[i + 1]
            a = a + b
            A2.append(a)
        else:
            a = r[i]
            b = r[i + 1]
            a = a + b
            A3.append(a)
    A = [A0,A1,A2,A3]#[['63','e0','63','89'],['51','7c','63','63'],['63','63', 'b7','7c'], ['8e','63','63','b7']]
    if flag == 1:#矩阵乘积形式的矩阵
        C = [['02', '03', '01', '01'], ['01', '02', '03', '01'],['01', '01', '02', '03'], ['03', '01', '01', '02']]
    else:
        C = [['0E', '0B', '0D', '09'], ['09', '0E', '0B', '0D'],['0D', '09', '0E', '0B'], ['0B', '0D', '09', '0E']]
    B = [B0,B1,B2,B3]
    for k in range(4):#循环A
        for j in range(4):#循环C
            for i in range(4):#两位16进制相乘
                if flag == 1:
                    d = xiangcheng_16(C[j][i],A[k][i])#d为2为16进制
                    D[i] = d
                else:
                    d = xiangcheng_16_jiemi(C[j][i], A[k][i])  # d为2为16进制
                    D[i] = d
            for i in range(4):#异或后即是[1,1]
                if i == 0:
                    z = D[i]
                else:
                    z = yihuo_16(z,D[i])
                B[k][j] = z

    for i in range(4):
        a = B[i]
        b_1 = [str(i) for i in a]
        b = ''.join(b_1)
        E[i] = b
    e = ''.join(E)
    return e
#a,c为两个16进制数
def xiangcheng_16(c,a):
    ten_c = int(c,16)
    ten_a = int(a,16)
    if c == '01':
        b = a#b是16进制
    elif c == '02':
        b = xtime(a)
        b = int(b,16)
        b = '{:02x}'.format(b)
    else:#ten_c=03时
        b = xtime(a)
        b = int(b, 16)
        b = b^ten_a
        b = '{:02x}'.format(b)
    return b#返回2位16进制
def xiangcheng_16_jiemi(c,a):
    ten_a = int(a,16)
    A = xtime(a)
    A = int(A,16)
    B = xtime(xtime(a))
    B = int(B,16)
    C = xtime(xtime(xtime(a)))
    C = int(C,16)
    if c == '0E':#1110
        b = C ^ B ^ A
    elif c == '0B':#1011
        b = C ^ A ^ ten_a
    elif c == '0D':#1101
        b = C ^ B ^ ten_a
    else:#09 1001
        b = C ^ ten_a
    b = '{:02x}'.format(b)
    return b#返回2位16进制

def xtime(x):#x乘法，‘02’乘法，x是2位16进制
    x = int(x,16)
    temp = x << 1
    if x & 0x80 != 0:#为1的话溢出，再异或1b,否则返回移位之后的值
        temp = temp ^ 0x1b#temp是int
        temp = format(temp, 'b')#temp位数大于8
        a = list(temp)
        b = [0,0,0,0,0,0,0,0]
        for i in range(8):
            b[7-i] = a[len(a)-1-i]
        c = ''.join(b)
        temp = int(c,2)
    temp = '{:02x}'.format(temp)
    return temp#temp是十六进制数

def AES(CipherKey,State,flag=1):
    a = KeyExpansion(CipherKey)#扩展密钥,是一个列表，共44个值
    b = [0,0,0,0,0,0,0,0,0,0,0]
    c = [0,0,0,0]
    for i in range(11):
        for j in range(4):
            c[j] = a[4*i+j]
        b[i] = ''.join(c)
    if flag == 1:
        E = AddRoundKey(State, b[0])#初始轮密钥加
    else:
        E = AddRoundKey(State, b[10])

    for i in range(1,10):
        B = SubByte(E,flag)
        r = ShiftRow(B,flag)
        e = MixColumn(r,flag)
        if flag == 1:
            E = AddRoundKey(e, b[i])
        else:
            b[10-i] = MixColumn(b[10-i],flag)
            E = AddRoundKey(e, b[10-i])

    B = SubByte(E,flag)
    r = ShiftRow(B,flag)
    if flag == 1:
        E = AddRoundKey(r, b[10])
    else:
        E = AddRoundKey(r, b[0])

    return E
#AES.AES('00012001710198aeda79171460153594','0001000101a198afda78173486153566')


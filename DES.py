# -*- coding: utf-8 -*-

#生成子密钥
#64位密钥经过置换选择1、循环左移、置换选择2等变换，产生16个48位长的子密钥
#参数是64位密钥
def generkey(key):
    keylist = list(key)#将输入密钥转换为列表

    #置换选择1
    left = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,
            10,2,59,51,43,35,27,19,11,3,60,52,44,36]
    right = [63,55,47,39,31,23,15,7,62,54,46,38,30,22,
             14,6,61,53,45,37,29,21,13,5,28,20,12,4] #28位
    C0 = []
    D0 = []
    for i in range(len(left)):
        a = left[i]
        b = right[i]
        C0.append(keylist[a-1])
        D0.append(keylist[b-1])

    C = [] #C=[C0,C1,C2...C16]
    D = []
    C.append(C0)
    D.append(D0)
    K = []
    Movetime = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    for i in range(16):
        a = Movetime[i]#循环左移的位数
        l = C[i]
        l = l[a:]+l[:a]#循环左移，得到下一个Ci
        C.append(l)
        r = D[i]
        r = r[a:]+r[:a]
        D.append(r)
        inter_result= C[i+1] + D[i+1] # Ci+Di,并成56位的中间数据
        K.append(inter_result)

    #置换选择2，选出16个48位的子密钥Ki
    Result = [14,17,11,24,1,5,
              3,28,15,6,21,10,
              23,19,12,4,26,8,
              16,7,27,20,13,2,
              41,52,31,37,47,55,
              30,40,51,45,33,48,
              44,49,39,56,34,53,
              46,42,50,36,29,32]
    for i in range(16):
        a = K[i]
        d = []
        for j in range(48):
            c = Result[j] #第一轮
            b = a[c-1]    #b=a[13]
            d.append(b)   #子密钥的第一位是中间数据的第14位
        K[i] = d    #生成的子密钥
    return K

#初始置换IP
#将64位明文打乱成重排，并分成左右两半，左边32位作为L0,右边32位为R0
#参数是64位明文
def chushizhihuan(mingwen):
    Minglist = list(mingwen)
    zhihuan_matrix = [58,50,42,34,26,18,10,2,
                      60,52,44,36,28,20,12,4,
                      62,54,46,38,30,22,14,6,
                      64,56,48,40,32,24,16,8,
                      57,49,41,33,25,17,9,1,
                      59,51,43,35,27,19,11,3,
                      61,53,45,37,29,21,13,5,
                      63,55,47,39,31,23,15,7]
    L0 = []
    R0 = []
    for i in range(32):
        l = zhihuan_matrix[i] #l = 58,=Minglist[58]第58位
        L = Minglist[l-1]
        L0.append(L)
        r = zhihuan_matrix[i+32]
        R = Minglist[r-1]
        R0.append(R)
    M=[0,0]
    M[0]=L0
    M[1]=R0
    return M #返回置换之后的明文

#加密函数f
#在第i次加密迭代中用密钥Ki对Ri-1进行加密
#参数Ri是32位输入A，k是48位子密钥
def f_func(Ri,k):
    #选择运算，对32为数据组A进行选择和排列，产生48位结果
    A = list(Ri) #a=32位
    E = [32,1,2,3,4,5,
         4,5,6,7,8,9,
         8,9,10,11,12,13,
         12,13,14,15,16,17,
         16,17,18,19,20,21,
         20,21,22,23,24,25,
         24,25,26,27,28,29,
         28,29,30,31,32,1]
    b = []
    for i in range(48):
        c = E[i]    #第一轮，c=32
        d = A[c-1]  #48位中间结果的第一位是A的第32位
        b.append(d) #b即48位的中间结果

    #中间结果与子密钥异或运算
    for i in range(48):
        b[i] = int(b[i]) ^ int(k[i])
    #盒子S运算
    s = [0, 0, 0, 0, 0, 0, 0, 0]
    #将异或结果分成8组，每组6位
    for i in range(8):
        s[i] = b[i * 6:(i + 1) * 6]

    S=[0,0,0,0,0,0,0,0]
    #8个S盒
    S[0] = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]

    S[1] = [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
           [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
           [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
           [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

    S[2] = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
           [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
           [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
           [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]

    S[3]= [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
           [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
           [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
           [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]

    S[4] = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]

    S[5] = [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]

    S[6] = [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]

    S[7] = [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    #输入s
    s2 = []
    for i in range(8):
        row = s[i][0] * 2 + s[i][5]#第1位和第6位代表选中的行号
        col = s[i][1]*8+s[i][2]*4+s[i][3]*2+s[i][4]#其余4位代表选中的列号
        s1=S[i][row][col]#
        s1='{:04b}'.format(s1)#将选中的数转换成4位二进制字符串
        s1 = list(s1)
        s2 = s2 + s1
    d = zhihuanyunsuan(s2)
    return d

#置换运算P
#把S盒输出的32位数据打乱重排，得到32位的加密函数输出
#输入参数是S盒输出的32位数据
def zhihuanyunsuan(s2):
    a = s2
    P = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,
         2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
    d = []
    for i in range(32):
        b = P[i]#b=16
        c = a[b-1]
        d.append(c)
    return d

#是初始置换IP的逆置换，它把64位加密迭代的结果打乱重排，形成64位密文
#输入参数是最后一轮的R，L
def nizhuanhuan_IP(R16,L16):
    IP = R16+L16
    c = []
    ip = [40,8,48,16,56,24,64,32,
          39,7,47,15,55,23,63,31,
          38,6,46,14,54,22,62,30,
          37,5,45,13,53,21,61,29,
          36,4,44,12,52,20,60,28,
          35,3,43,11,51,19,59,27,
          34,2,42,10,50,18,58,26,
          33,1,41,9,49,17,57,25]
    for i in range(64):
        a = ip[i]#a=40
        b = IP[a-1]
        c.append(b)
    list1 = [str(i) for i in c]
    list2 = ''.join(list1)
    return list2

#flag为1时是解密，0是加密
#参数mingwen是明文或者密文，key是密钥
def DES(flag,mingwen,key):
    Key = generkey(key)#生成密钥
    M = chushizhihuan(mingwen)
    L0 = M[0]
    R0 = M[1]

    R = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],[]]
    R[0] = R0
    L = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],[]]
    L[0] = L0
    d = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for j in range(16):
        if flag == "0":
            d[j]=f_func(R[j],Key[j])
        else:
        #解密时使用子密钥的顺序正好反过来
            d[j] = f_func(R[j], Key[15-j])
        for i in range(32):
            qin = int(d[j][i])^int(L[j][i])
            R[j+1].append(qin)
        L[j+1] = R[j]

    list2 = nizhuanhuan_IP(R[16],L[16])
    return list2

#key 0011000100110010001100110011010000110101001101100011011100111000
#明文 0011000000110001001100100011001100110100001101010011011000110111
#密文 1000101110110100011110100000110011110000101010010110001001101101
#DES.DES("0","0011000000110001001100100011001100110100001101010011011000110111","0011000100110010001100110011010000110101001101100011011100111000")
#DES.DES("1","1000101110110100011110100000110011110000101010010110001001101101","0011000100110010001100110011010000110101001101100011011100111000")
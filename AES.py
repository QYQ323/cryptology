# -*- coding: utf-8 -*-
import generkey
def AES(CipherKey,State,flag=1):
    a = generkey.KeyExpansion(CipherKey)#扩展密钥,是一个列表，共44个值
    b = [0,0,0,0,0,0,0,0,0,0,0]
    c = [0,0,0,0]
    for i in range(11):
        for j in range(4):
            c[j] = a[4*i+j]
        b[i] = ''.join(c)
    if flag == 1:
        E = generkey.AddRoundKey(State, b[0])#初始轮密钥加
    else:
        E = generkey.AddRoundKey(State, b[10])

    for i in range(1,10):
        B = generkey.SubByte(E,flag)
        r = generkey.ShiftRow(B,flag)
        e = generkey.MixColumn(r,flag)
        if flag == 1:
            E = generkey.AddRoundKey(e, b[i])
        else:
            b[10-i] = generkey.MixColumn(b[10-i],flag)
            E = generkey.AddRoundKey(e, b[10-i])

    B = generkey.SubByte(E,flag)
    r = generkey.ShiftRow(B,flag)
    if flag == 1:
        E = generkey.AddRoundKey(r, b[10])
    else:
        E = generkey.AddRoundKey(r, b[0])

    return E
#AES.AES('00012001710198aeda79171460153594','0001000101a198afda78173486153566')


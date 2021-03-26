# -*- coding: utf-8 -*-

SboxTable = [
    0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
    0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
    0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
    0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
    0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
    0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
    0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
    0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
    0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
    0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
    0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
    0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
    0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
    0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
    0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
    0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48,
]

FK = ['a3b1bac6', '56aa3350', '677d9197', 'b27022dc']

CK = [
    '00070e15', '1c232a31', '383f464d', '545b6269',
    '70777e85', '8c939aa1', 'a8afb6bd', 'c4cbd2d9',
    'e0e7eef5', 'fc030a11', '181f262d', '343b4249',
    '50575e65', '6c737a81', '888f969d', 'a4abb2b9',
    'c0c7ced5', 'dce3eaf1', 'f8ff060d', '141b2229',
    '30373e45', '4c535a61', '686f767d', '848b9299',
    'a0a7aeb5', 'bcc3cad1', 'd8dfe6ed', 'f4fb0209',
    '10171e25', '2c333a41', '484f565d', '646b7279'
]

#s盒变换，一次处理一个字，共用4个S盒
#输入一个8位16进制的字符串，如'abcd1234'
def S_box(S_Input):
    #将8位字符串分成4组
    A = list(S_Input)
    a = [0,0,0,0]
    Out=[0,0,0,0]
    a[0] = [A[0],A[1]]#a0=['a','b']
    a[1] = [A[2],A[3]]
    a[2] = [A[4],A[5]]
    a[3] = [A[6],A[7]]
    #高位的16进制转换成10进制*16+低位的16进制转换成10进制
    for j in range(4):
        for i in range(2):
            a[j][i] = int(a[j][i],16)
        b = int(a[j][0]*16+a[j][1])
        Out[j] = SboxTable[b]
    for i in range(4):
        Out[i]='{:02x}'.format(Out[i])
    S_out = ''.join(Out)
    #print (S_out)
    return S_out

def xianxing_L(S_out,flag):#flag为1则处理论函数，为0则是密钥扩展
    B = list(S_out)
    for i in range(8):
        B[i]=int(B[i],16)
        B[i]='{:04b}'.format(B[i])
    B = B[0]+B[1]+B[2]+B[3]+B[4]+B[5]+B[6]+B[7]
    B_2 = B[2:] + B[:2]
    B_10 = B[10:] + B[:10]
    B_18 = B[18:] + B[:18]
    B_24 = B[24:] + B[:24]
    B_13 = B[13:] + B[:13]
    B_23 = B[23:] + B[:23]
    print(B)
    B = list(B)
    if flag==1:
        for i in range(32):
            B[i] = int(B[i])^int(B_2[i])^int(B_10[i])^int(B_18[i])^int(B_24[i])
    else:
        for i in range(32):
            B[i] = int(B[i]) ^ int(B_13[i]) ^ int(B_23[i])
    A = ['','','','','','','','']
    for i in range(8):
        for j in range(4):
            a = str(B[4*i+j])
            A[i] = A[i] + a
        A[i] = int(A[i],2)
        A[i] = '{:01x}'.format(A[i])
    L_out = ''.join(A)
    return L_out

def T(A,flag):#为1则论函数，为0则扩展密钥
    S_out = S_box(A)
    T_out = xianxing_L(S_out,flag)
    return T_out

#参数应该都为8位16进制字符串
def lun_func(X0,X1,X2,X3,rk,flag):#为1则论函数，为0则扩展密钥
    x1 = yihuo_32(X1,X2)
    x2 = yihuo_32(x1,X3)
    x3 = yihuo_32(x2,rk)
    T_out = T(x3,flag)
    F_out = yihuo_32(T_out,X0)
    return F_out

#两个8位16进制数，即32位2进制的异或运算
def yihuo_32(a0,a1):
    A = []
    ten_a0 = int(a0,16)#16进制转换为10进制
    ten_a1 = int(a1, 16)
    ten_bin_a0 = '{:032b}'.format(ten_a0)#10进制转换为32进制
    ten_bin_a1 = '{:032b}'.format(ten_a1)
    list_a0 = list(ten_bin_a0)
    list_a1 = list(ten_bin_a1)
    for i in range(32):#按位异或
        a = int(list_a0[i])^int(list_a1[i])
        A.append(a)
    c_1 = [str(i) for i in A]
    c = ''.join(c_1)
    c = int(c, 2)#二进制转换为10进制
    c = '{:08x}'.format(c)#10进制转换为8位16进制，一定要规范位数
    return c

def extend_key(MK0,MK1,MK2,MK3):#'01234567','89abcdef','fedcba98','76543210'
    K0 = yihuo_32(MK0,FK[0])
    K1 = yihuo_32(MK1,FK[1])
    K2 = yihuo_32(MK2,FK[2])
    K3 = yihuo_32(MK3,FK[3])#'a292ffa1', 'df01febf', '99a12b0f', 'c42410cc'
    K = [K0,K1,K2,K3]#S_box:'e25d48f6','b0903951','93f64305','bb912b1f'
    rk = []#'8283cb69',S_box:'8ad24122'
    for i in range(32):
        a = lun_func(K[i],K[i+1],K[i+2],K[i+3],CK[i],flag=0)
        K.append(a)
        rk.append(a)
    return rk

def encrypt(MK0,MK1,MK2,MK3,X0,X1,X2,X3,en_de):#en_de为1则加密，X是明密文
    rk = extend_key(MK0,MK1,MK2,MK3)#生成扩展密钥
    X = [X0,X1,X2,X3]
    for i in range(32):
        if en_de==1:
            x = lun_func(X[i], X[i+1], X[i+2], X[i+3], rk[i], flag=1)
        else:
            x = lun_func(X[i], X[i + 1], X[i + 2], X[i + 3], rk[31-i], flag=1)
        X.append(x)
    Y = [0,0,0,0]
    for i in range(4):
        Y[i] = X[35-i]
    return Y
print(encrypt('01234567','89abcdef','fedcba98','76543210','01234567','89abcdef','fedcba98','76543210',1))
#密文['681edf34', 'd206965e', '86b3e94f', '536e4246']
#明文/密钥'01234567', '89abcdef', 'fedcba98', '76543210'
#sm4.encrypt('01234567','89abcdef','fedcba98','76543210','01234567','89abcdef','fedcba98','76543210',1)jiami
#sm4.encrypt('01234567','89abcdef','fedcba98','76543210','681edf34','d206965e','86b3e94f','536e4246',0)
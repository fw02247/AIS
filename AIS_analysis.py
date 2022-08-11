"""
#----------------------------------------------------------------------------------
#                   MAIN: AIS_ANALYSIS
#----------------------------------------------------------------------------------
#
#                   @Param   : path of AIS data
#
#                   @Return  :  information —— 拆分开的AIS数据，用于写入AIS.csv
                                datas —— 从AIS中提取出来的数据字段，用于继续解析
                                hours —— 从AIS中提取出来的时间字段，用于观察规律
#
#                   @Author  : Ji HuiTing
#
#                   @Start Date   : 2022/8
#
#----------------------------------------------------------------------------------
"""

import re

"""
!XXYYY,A,B,C,N,Data,V*HH<CR><LF>
XX：使用的设备
    “AI”是船载标志
    “BS”是基站标志。
YYY：语句类型
    "VDM"表示封装的是他船信息
    "VDO"表示封装的是本船信息。
A：报文条数
    （1-9）
B：本条报文的序列数，此字段不能为空。
    （1-9）
C：连续报文的识别码（0-9），给每一份新的多语句电文按序列指配编号，每次加1，计数到9后返回0
    对要求多语句的电文，电文的每一句包含同样序列的电文号，它用于识别包含同一电文各个部分的语句。
    这样，使其他语句可以与包含该同一电文的各语句相互穿插。
    在电文可以使用一个语句时，该字段为空。
N：信道指示为“A”或“B”，报文是从信道“A”还是“B”接收。
    本信道指示与接收该数据包时与AIS的运行状态有关。
    当不提供频道识别时，本数据为空。
    信道“A”或“B”的VHF信道号，可用AIS的一个ACA语句查询得到。
Data：数据部分，封装的最大长度的限制是语句的总字符数不超过82.对于用多语句传送的电文，本字段支持最多62个有效字符。而对于单语句传送的电文，最多为63个有效字符。
V：填充位数（比特数），二进制比特数必须是6的倍数，如果不是，要加入1-5个填充比特。
    本参数指示加到最后一个6比特编码字符上的比特数。未加入填充比特时，本数值为0，本字段不可以为空。
    (即填充字符，由于每条消息语句总位数必须是6的整数倍，否则需填充0-5个字符)
HH：检验字段。AIS数据采用8位CRC，
    取其8位CRC校验码的高四位，并转化为16进制数，构成AIS校验码的第一位，
    取其8位CRC校验码的低四位，转化为16进制数后构成校验码的第二位。
    当AIS接收设备收到一条AIS电文后，按照8位CRC对其数据部分进行重新校验，生成的校验值如果与电文自带的校验值相同，说明电文数据在传输过程中没有出错。
    如果不同，则说明数据在传输过程中出错了。
< CR > < LF >：语句结束标志。
"""

# 解析AIS数据
def ais_analysis(path):
    file = open(path, "r")
    informations = []
    datas = []
    hours = []
    for row in file:
        if row == "\n":
            continue
        if not re.match("\d+-\d+-\d+ \d+:\d+:\d+,!\w{5},\d+,\d+,\d*,[AB],.{0,82},.*..\n$", row):
            print("不符合AIS格式,continue")
            continue
        # !XXYYY,A,B,C,N,Data,V*HH<CR><LF>--------------------------------------------
        time, other = row.split("!", 1)
        information = ["!" + other, time]
        time = time[:-1]  # 删除结尾的逗号
        XY, A, B, C, N, other = other.split(",", 5)
        data, other = other.rsplit(",", 1)
        V, HH = other.split("*")
        LF = HH[2:]
        HH = HH[:2]

        other, hour = time.split(" ")
        hour, other = hour.split(":", 1)

        # 设备--------------------------------------------
        X, Y = XY[:2], XY[2:]
        XX = "ERROR"
        if X == "AI":
            XX = "船载设备"
        elif X == "BS":
            XX = '基站设备'
        elif X == "AB":
            XX = "SAAB"
        information.append(XX)
        # 信息来源--------------------------------------------
        YY = "ERROR"
        if Y == "VDM":
            YY = "他船信息"
        elif Y == "VDO":
            YY = "本船信息"
        information.append(YY)
        # 报文信息--------------------------------------------
        information.append(A)
        information.append(B)
        information.append(C)
        information.append(N)
        # 数据------------------------------------------------
        information.append(data)

        # 为了方便，直接将分段的数据排除。----------------------
        if A == "1":
            informations.append(information)
            datas.append(data)
            hours.append(hour)
        else:
            print("报文数量大于1，continue")

    return informations, datas, hours


"""-------------------------------------------- 
            注：
                以上是简略解析，还有两个点没有详细分析。现在暂时用不上，先不写。
                1、校验字段。关于CRC校验码。即代码中的HH
                2、补充位数，即代码中的V
-------------------------------------------- """
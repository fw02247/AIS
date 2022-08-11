"""
    0 消息识别码6
    1 转发次数2
    2 MMSI码30
    3 转向率8
    4 对地航速10
    5 船位精确度2
    6 船舶经度27
    7 船舶纬度27
    8 对地航向12
    9 真航向9
    10 时间标记6
    11 地方主管机关保留数4
"""

def data_analysis(datas):

    res = []
    cnt = 0
    for data in datas:
        print(data)
        cnt += 1
        # 切片
        num = [0, 6, 2, 30, 8, 10, 2, 27, 27, 12, 9, 6, 4]
        for i in range(1, len(num)):
            num[i] = num[i] + num[i - 1]
        code = []
        for i in range(1, len(num)):
            code.append(data[num[i - 1]:num[i]])
        print(code)
        # 解析
        ans = []
        for each in code:
            ans.append(int(each, 2))
        res.append(ans)
    return res



"""
        0 消息识别码6
        1 转发次数2
        2 MMSI码30
        3 航行状态4
        4 转向率8
        5 对地航速10
        6 船位精确度1
        7 船舶经度28
        8 船舶纬度27
        9 对地航向12
        10 真航向9
        11 时间标记6
        12 地方主管机关保留数4
"""
def data_analysis2(datas):
    res = []
    cnt = 0
    for data in datas:
        print(data)
        cnt += 1
        # 切片
        num = [0, 6, 2, 30, 4, 8, 10, 1, 28, 27, 12, 9, 6, 4, 19]
        for i in range(1, len(num)):
            num[i] = num[i] + num[i - 1]
        code = []
        for i in range(1, len(num)):
            code.append(data[num[i - 1]:num[i]])
        print(code)
        # 解析
        ans = []
        for each in code:
            ans.append(int(each, 2))
        res.append(ans)
    return res
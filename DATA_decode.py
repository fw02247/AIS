def data_decode(datas, hour):
    for data in datas:
        # 4 对地航速10
        if data[4] == 1023:
            data[4] = "不可用"
        else:
            data[4] /= 10
        # 5 船位精确度1
        if data[5] == 0:
            data[5] = "低"
        elif data[5] == 1:
            data[5] = "高"
        # 6 船舶经度28
        data[6] = data[6] / 10000 / 60
        # 7 船舶纬度27
        data[7] = data[7] / 10000 / 60

        # 8 对地航向12
        data[8] /= 10

    res = []
    for i in range(len(hour)):
        line = [hour[i], datas[i][4], datas[i][6], datas[i][7], datas[i][8]]
        res.append(line)
    return res


def data_decode2(datas, hour):
    for data in datas:
        # 3 航行状态
        state = {0: "在航", 1: '抛锚', 2: '失控', 3: '操作受限', 4: '系泊', 5: '吃水受限', 6: '搁浅', 7: '捕捞', 8: '操帆在航', 9: '预留',
                 10: '预留', 11: '待用', 12: '待用', 13: '待用', 14: '待用', 15: '未定义'}
        data[3] = state[data[3]]
        # 4 转向率8
        if data[4] > 127 or data[4] < -127:
            data[4] = "无法获得"
        # 5 对地航速10
        if data[5] == 1023:
            data[5] = "不可用"
        else:
            data[5] /= 10
        # 6 船位精确度1
        if data[6] == 0:
            data[6] = "低"
        elif data[6] == 1:
            data[6] = "高"
        # 7 船舶经度28
        data[7] = data[7] / 10000 / 60
        # 8 船舶纬度27
        data[8] = data[8] / 10000 / 60

        # 9 对地航向12
        data[9] /= 10
        if data[11] == 60:
            data[11] = "不可用"

    res = []
    for i in range(len(hour)):
        line = [hour[i], datas[i][5], datas[i][7], datas[i][8], datas[i][9]]
        res.append(line)
    return res
import os
from AIS_analysis import ais_analysis
from Decode_option import *
from DATA_analysis import data_analysis
from DATA_decode import data_decode


if __name__ == "__main__":
    path = r"file\test.txt"
    savepath = r"file\AIS.csv"
    savepath2 = r"file\data.csv"
    savepath3 = r"file\data_decode.csv"

    # init --------------------------------------------
    if os.path.isfile(savepath):
        os.remove(savepath)
    if os.path.isfile(savepath2):
        os.remove(savepath2)
    if os.path.isfile(savepath3):
        os.remove(savepath3)

    # 解析ais --------------------------------------------
    header = [['AIS', '时间', "设备", "信息来源", "报文条数", "报文序列数", "报文识别码", "信道指示", "数据"]]
    load(savepath, header)
    information, data, hours = ais_analysis(path)
    load(savepath, information)

    analysis_ais = []
    for each in data:
        analysis_ais.append(decode(each))
    # 解析data --------------------------------------------

    header2 = [["消息识别码", "转发次数", "MMSI码", "转向率", "对地航速", "船位精确度", "船舶经度",
                "船舶纬度", "对地航向", "真航向", "时间标记", "地方主管机关保留数", "通信状态"]]
    load(savepath2, header2)

    analysis_data = data_analysis(analysis_ais)
    load(savepath2, analysis_data)
    for each in analysis_data:
        print(each)
    # 解析data --------------------------------------------

    header3 = [["时辰", "航速", "经度", "纬度", "航向"]]
    load(savepath3, header3)

    decode_data = data_decode(analysis_data, hours)
    load(savepath3, decode_data)
    for each in decode_data:
        print(each)
    # over --------------------------------------------
    print("AIS数据解析完毕！共%d条数据！" % len(hours))
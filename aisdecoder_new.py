#-*- coding: UTF-8 -*-
# version:python3.7
# author:leeechsh
# date:2020-08-21

# import ais
import os,sys
import time
import math
import pandas as pd
import zipfile
import re
from datetime import datetime
import time
import multiprocessing
import gc

#minlon = 119
#maxlon = 119.6
#minlat = 24.866667
#maxlat = 25.233333


y2 = 31.5133333
x2 = 121.416667
y4 = 31.391667
x4 = 121.645
y3 = 31.34
x3 = 121.605
y1 = 31.473333
x1 = 121.386667

'''
 （x1，y1）为最左的点、（x2，y2）为最上的点、（x3，y3）为最下的点、（x4， y4）为最右的点。
给定4个点代表的矩形，再给定一个点（x，y），判断（x，y）是否在矩形中。
'''

dx = x4 - x3
dy = y4 - y3
ds = (dx**2 + dy**2)**0.5
cost = dx / ds
sint = dy / ds
# python特性：隐含临时变量存储值
# x, y = cost * x + sint * y, -sint * x + cost * y
x1, y1 = cost * x1 + sint * y1, -sint * x1 + cost * y1
x4, y4 = cost * x4 + sint * y4, -sint * x4 + cost * y4


sourceBasePath = "./raw/"
desBasePath = "./filtered/" # iwrapdata, dedata

timestr = '2018-01-01:00:00:00;'

def filter_ais(sourcefile):             # 返回一个文件对象
    zipfile_path = sourceBasePath + sourcefile
    desfile_path = desBasePath + "iwrapdata/iwrap_" + sourcefile + '.txt'
    dedatafile_path = desBasePath + "dedata/de_" + sourcefile + '.txt'
    logFile = desBasePath  + 'aisdecode_log.log'

    fw = open(desfile_path, "a")
    logfw = open(logFile, "a")
    fw_decode = open(dedatafile_path, "a")
    start = time.time()
    outputBuf = []
    deoutputBuf = []
    try:
        with zipfile.ZipFile(zipfile_path, mode='r') as zfile:  # 只读方式打开压缩包
            nWaitTime = 1
            for name in zfile.namelist():  # 获取zip文档内所有文件的名称列表
                print(name)
                with zfile.open(name, mode='r') as txt_file:
                    lines = txt_file.read().decode('utf8')
                    lines = lines.split('\n')
                    for line in lines:
                        if line != '' and line[3] == '1':
                            timestrs = re.findall(r"c:(.+?)\*", line)[0]
                            line = re.findall(r"!(.+)\r", line)[0]
                            utc_date = datetime.utcfromtimestamp(int(timestrs))
                            timestr = utc_date.strftime("%Y-%m-%d:%H:%M:%S")

                            nmeamsg = line.split(',')
                            #print(nmeamsg)
                            if nmeamsg[0] == 'ABVDM' and nmeamsg[1] == '1':
                                try:
                                    decodedata = ais.decode(
                                        nmeamsg[5], int(nmeamsg[6].split('*')[0]))
                                    if decodedata['id'] != 24:
                                        if isInParRect(decodedata['x'], decodedata['y']):
                                            # print(decodedata, "\n")
                                            # print(decodedata['x'],decodedata['y'])
                                            # print("output======",timestr+line + "-"+str(decodedata['x']) +"-"+ str(decodedata['id']) )
                                            outputline = timestr + ';!'+line + "\n"
                                            outputBuf.append(outputline)

                                            if 'name' in decodedata.keys():
                                                # print(decodedata,"\n")
                                                deline = timestrs + ',' + str(decodedata['mmsi']) + ',' + str(
                                                    decodedata['x']) + ',' + str(decodedata['y']) + ',' + str(decodedata['cog']) + ',' + str(decodedata['sog']) + ',' + str(decodedata['type_and_cargo']) + ',' + str(decodedata['dim_a']+decodedata['dim_b']) + ',' + str(decodedata['dim_c']+decodedata['dim_d']) + "\n"
                                            else:
                                                deline = timestrs + ',' + str(decodedata['mmsi']) + ',' + str(
                                                    decodedata['x']) + ',' + str(decodedata['y']) + ',' + str(decodedata['cog']) + ',' + str(decodedata['sog']) + ',' + str(0) + ',' + str(0) + ',' + str(0) + "\n"
                                            # fw.write(deline + "\n")
                                            deoutputBuf.append(deline)
                                            # print(outputline)
                                            # fw.write(outputline)
                                except Exception as ex:
                                    pass
                                    # print("Decode Exception",ex)
                    del lines
                    gc.collect()

        zfile.close()
    except Exception as e:
        print("====", e)
        logfw.write("file---" + zipfile_path + "\n")
    # iwrap
    fw.writelines(outputBuf)
    # 明文格式
    fw_decode.writelines(deoutputBuf)
    
    fw.close()
    fw_decode.close()
    logfw.close()
    end = time.time()
    print("time = ",end - start)
    

def isInParRect(x, y):
    x, y = cost * x + sint * y, -sint * x + cost * y
    if x <= x1:
        return False
    if x >= x4:
        return False
    if y >= y1:
        return False
    if y <= y4:
        return False
    return True

def write_log(desfile,line):
    logPath = desfile + '_log.log'
    logf = open(logPath, "a")
    logf.write(line + "\n")
    logf.close()

def month_handle(month_index):

    daynum = [31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31]
    monthlist = ['201805', '201806', '201807', '201808', '201809',
                 '201810', '201811', '201812', '201901', '201902', '201903', '201904', '201905']

    desFilePath = desBasePath + monthlist[month_index] + '.txt'

    for day in range(1, daynum[month_index]+1):
        for hour in range(24):
            sourceFilePath = sourceBasePath + monthlist[month_index] + "%02d" % day + "%02d" % hour
            print(sourceFilePath, "---", desFilePath)
            if os.path.exists(sourceFilePath):
                filter_ais(sourceFilePath, desFilePath)
            else:
                print("===Given file path is exist.", sourceFilePath)
                write_log(desFilePath, "===Given file path is exist."+ sourceFilePath+ '\n')

def get_filename():
    print("===")


def file_name_walk(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files  # 当前路径下所有非目录子文件

def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.zip':
                L.append(file)
                # L.append(os.path.join(root, file))
                
    return L

if __name__ == '__main__':
    
    start = time.time()

    filelist = file_name(sourceBasePath)
    filelist.sort()
    print(filelist, "\n")

    print(multiprocessing.cpu_count())
    pool = multiprocessing.Pool(processes=5)
    pool.map_async(filter_ais, filelist)
    pool.close()
    pool.join()

    end = time.time()
    print("time = ", end - start)

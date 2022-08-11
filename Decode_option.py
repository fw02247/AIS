import csv
import copy
def load(path, old_data):
    data = copy.deepcopy(old_data)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if not isinstance(data[i][j], str):
                data[i][j] = str(data[i][j])
    with open(path, mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


# 经纬度转换
def latitude(num):
    num /= 10000
    c = num % 1
    num //= 1
    num /= 60
    c += num % 1 * 60
    num //= 1
    return [num, c]


# data转化为二进制编码
def decode(data):
    ans = ""
    for each in data:
        """
            param：  ascii字符串
            decode： ascii   -->     8bit型十进制 (ord)
                     8bit型十进制   -->     6bit型十六进制 (-48 or -56)
                     十六进制    -->     二进制 (与运算：0x3f)
                     取最低六位
        """
        num = ord(each)
        if 48 <= num <= 87:
            num -= 48
        elif 96 <= num <= 119:
            num -= 56
        num = num & 0x3f
        res = str(bin(num))
        res = res[2:]
        res = res.zfill(8)
        res = res[2:]
        print("-------------------------------------------- ", res)
        ans += res
        print(ans)
    return ans
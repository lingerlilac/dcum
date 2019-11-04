#-*—coding:utf8-*-
import gc
# import re
import sys
import csv
import numpy as np
import matplotlib as mpl
# import time as tm
from matplotlib import pyplot
from statsmodels.distributions.empirical_distribution import ECDF
mpl.use('pdf')


fname = sys.argv[1]
fwname = sys.argv[2]
try:
    ff = open(fname, 'r')
    fr = csv.reader(ff)
except Exception:
    print("tcp.txt openfailed")
    exit()
try:
    f1 = open(fwname, 'w')
    fw = csv.writer(f1)
except Exception:
    print(fwname, 'open failed')
    exit()
dic = {}
data = []
# count = 0
# try:
#     ftmp = open('test_cubic.csv', 'w')
#     ftw = csv.writer(ftmp)
# except Exception:
#     print('test.csv open failed')

# for item in fr:
#     count += 1
#     if count > 1000000:
#         break
#     ftw.writerow(item)
# if(ftmp):
#     ftmp.close()
# exit()


def drawCumulativeHist(h0, h1, fname):
    # 创建累积曲线
    # 第一个参数为待绘制的定量数据
    # 第二个参数为划分的区间个数
    # normed参数为是否无量纲化
    # histtype参数为'step'，绘制阶梯状的曲线
    # cumulative参数为是否累积
    pyplot.rc('font', family='serif', serif='Times')
    pyplot.rc('text', usetex=True)
    pyplot.rc('xtick', labelsize=8)
    pyplot.rc('ytick', labelsize=8)
    pyplot.rc('axes', labelsize=8)
    # width as measured in inkscape
    width = 3.487
    height = width / 1.618

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)

    length = int(min(len(h0), len(h1)))
    ecdf = ECDF(h0)
    ecdf1 = ECDF(h1)
    x = np.linspace(min(h0), max(h0), length)
    y = ecdf(x)
    y1 = ecdf1(x)
    # pyplot.hist(h0, length, normed=True, histtype='step',
    #             cumulative=True, label="RSSI")
    # pyplot.hist(h1, length, normed=True, histtype='step',
    #             cumulative=True, label="LR")
    pyplot.step(x, y, label="RSSI")
    pyplot.step(x, y1, label="LR")
    pyplot.xlabel('Jitters/ms')
    pyplot.ylabel('CDF')
    pyplot.xlim(0, 300)
    pyplot.title('CDF of Jitters')
    pyplot.legend(loc='lower right')
    fig.set_size_inches(width, height)
    fig.savefig(fname + '.pdf')
    pyplot.show()


def compute_derivation(data, fname):
    data_re = []
    # try:
    #     fc = open(fname, 'w')
    #     fcw = csv.writer(fc)
    # except Exception:
    #     print(fname, 'openfailed')
    length = len(data)
    for i in range(0, length - 2):
        ic = i
        ix = i + 1
        x0 = data[ic][1]
        x1 = data[ix][1]
        # y0 = data[ic][0]
        # y1 = data[ix][0]
        try:
            val = (x1 - x0)
            if(val < 0):
                val = val * (-1.0)
        except Exception:
            print(x0, i)
            continue
        if val < 0:
            val = val * (-1)
        if(val != 0):
            data_re.append(val)
        # fcw.writerow((val,))
    # if(fc):
    #     fc.close()
    return data_re


for item in fr:
    try:
        (a, b, c, rtt, e, f) = item
        b = int(b)
        c = int(c)
    except Exception:
        continue
    a = int(a)
    rtt = float(rtt)
    data_item = (c, a, rtt)
    data.append(data_item)
    key = (b, c)
    try:
        dic[key].add(rtt)
    except Exception:
        dic[key] = set()
    # fw.writerow(data_item)

del_set = set()
for key in sorted(dic.keys()):
    # print(key, len(dic[key]))
    if(len(dic[key]) < 5):
        (a, b) = key
        # print(key, a, b)
        b = int(b)
        del_set.add(b)
# print(del_set)
keep_dic = {}
for key in dic.keys():
    (t1, t2) = key
    if t2 not in del_set:
        keep_dic[t2] = []

for i in data:
    (a, b, c) = i
    # print(i)
    a = int(a)
    # print(a, keep_dic.keys(), del_set, dic.keys())
    try:
        keep_dic[a].append([b, c])
    except Exception:
        pass
del data
gc.collect()
d_cubic = []
for key in keep_dic.keys():
    d_cubic += compute_derivation(keep_dic[key], str(key))
    # print(key, keep_dic[key])
del keep_dic, dic, del_set
if(f1):
    f1.close()

if ff:
    ff.close()
gc.collect()

fname = sys.argv[3]
fwname = sys.argv[4]
try:
    ff = open(fname, 'r')
    fr = csv.reader(ff)
except Exception:
    print("tcp.txt openfailed")
    exit()
try:
    f1 = open(fwname, 'w')
    fw = csv.writer(f1)
except Exception:
    print(fwname, 'open failed')
    exit()
dic = {}
data = []

for item in fr:
    try:
        (a, b, c, rtt, e, f) = item
        b = int(b)
        c = int(c)
    except Exception:
        continue
    a = int(a)
    rtt = float(rtt)
    data_item = (c, a, rtt)
    data.append(data_item)
    key = (b, c)
    try:
        dic[key].add(rtt)
    except Exception:
        dic[key] = set()
    # fw.writerow(data_item)

del_set = set()
for key in sorted(dic.keys()):
    # print(key, len(dic[key]))
    if(len(dic[key]) < 5):
        (a, b) = key
        # print(key, a, b)
        b = int(b)
        del_set.add(b)
# print(del_set)
keep_dic = {}
for key in dic.keys():
    (t1, t2) = key
    if t2 not in del_set:
        keep_dic[t2] = []

for i in data:
    (a, b, c) = i
    # print(i)
    a = int(a)
    # print(a, keep_dic.keys(), del_set, dic.keys())
    try:
        keep_dic[a].append([b, c])
    except Exception:
        pass
del data
gc.collect()
d_bbr = []
for key in keep_dic.keys():
    d_bbr += compute_derivation(keep_dic[key], str(key))
    # print(key, keep_dic[key])
del keep_dic, dic, del_set
if(f1):
    f1.close()

if ff:
    ff.close()

drawCumulativeHist(d_cubic, d_bbr, "jitter")
gc.collect()

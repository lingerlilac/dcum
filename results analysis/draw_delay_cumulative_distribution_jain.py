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


def get_10_means(data):
    length = len(data)
    duration = int(length / 10)
    x = [0.0 for i in range(0, 10)]
    y = [0.0 for i in range(0, 10)]
    ind = 0
    i = 0
    # print(len(data))
    while(i < length):
        beg = i
        end = beg + duration
        # print(beg, end, length, duration)
        if(end < length):
            x[ind] = np.mean(data[beg:end])
            y[ind] = np.std(data[beg:end])
        elif beg < length:
            if ind >= 10:
                return (x, y)
            else:
                x[ind] = np.mean(data[beg:length])
                y[ind] = np.std(data[beg:length])
        elif beg >= length:
            return (x, y)
        i = i + duration
        ind = ind + 1


def get_jain(x1, x2, x3):
    z1 = (x1 + x2 + x3) * (x1 + x2 + x3)
    z2 = x1 * x1 + x2 * x2 + x3 * x3
    z2 = 3 * z2
    val = z1 / z2
    return val


def drawCumulativeHist(h0, h1, h2, h3, fname):
    # 创建累积曲线
    # 第一个参数为待绘制的定量数据
    # 第二个参数为划分的区间个数
    # normed参数为是否无量纲化
    # histtype参数为'step'，绘制阶梯状的曲线
    # cumulative参数为是否累积
    # pyplot.rc('font', family='serif', serif='Times')
    pyplot.rc('text', usetex=True)
    pyplot.rc('xtick', labelsize=8)
    pyplot.rc('ytick', labelsize=8)
    pyplot.rc('axes', labelsize=8)
    # width as measured in inkscape
    width = 3.487
    height = width / 1.618
    length1 = len(h0)
    for i in range(0, length1):
        h0[i] = h0[i] / 10
    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)

    length = int(min(len(h0), len(h1), len(h2), len(h3)))
    ecdf = ECDF(h0)
    ecdf1 = ECDF(h1)
    ecdf2 = ECDF(h2)
    ecdf3 = ECDF(h3)
    x = np.linspace(min(h0), max(h0), length)
    y = ecdf(x)
    y1 = ecdf1(x)
    y2 = ecdf2(x)
    y3 = ecdf3(x)

    pyplot.step(x, y2, label="LRCC", color="orange")
    pyplot.step(x, y1, label="LRFL", color="green", linestyle="--")
    pyplot.step(x, y3, label="LR", color="blue", linestyle=":")
    pyplot.step(x, y, label="RSSI", color="red", linestyle="-.")

    pyplot.xlabel('delays/ms')
    pyplot.ylabel('CDF')
    pyplot.xlim(0, 3000)
    pyplot.title('CDF of delays')
    pyplot.legend(loc='lower right')
    fig.set_size_inches(width, height)
    fig.savefig(fname + '.pdf')
    pyplot.show()


def drawHist(h0, h1, fname):
    # 创建累积曲线
    # 第一个参数为待绘制的定量数据
    # 第二个参数为划分的区间个数
    # normed参数为是否无量纲化
    # histtype参数为'step'，绘制阶梯状的曲线
    # cumulative参数为是否累积
    # means_c = [0 for i in range(0, 10)]
    # means_b = [0 for i in range(0, 10)]
    # vars_c = [0 for i in range(0, 10)]
    # vars_b = [0 for i in range(0, 10)]
    # for i in range(0, 10):
    #     means_c[i] = h0[i][0]
    #     vars_c[i] = h0[i][1]
    #     means_b[i] = h1[i][0]
    #     vars_b[i] = h1[i][1]
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
    ind = np.arange(10)
    # length = int(min(len(y0), len(y1)))
    indb = np.arange(0.25, 10.25, 1)
    wid = 0.25

    pyplot.bar(ind, h0, wid, label="RSSI")
    pyplot.bar(indb, h1, wid, label="LR")
    pyplot.xticks(ind, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    pyplot.yticks(np.arange(0, 700, 100))
    pyplot.xlabel('Iteration')
    pyplot.ylabel('Overall Throughput (KBytes/s)')
    # pyplot.xlim(0, int(min(max(h0), max(h1))) - 1)
    pyplot.title('CDF of Delays')
    pyplot.legend(loc='upper left')
    fig.set_size_inches(width, height)
    fig.savefig(fname + '.pdf')
    pyplot.show()


def drawHist_02(h0, h1, h2, h3, fname):
    # 创建累积曲线
    # 第一个参数为待绘制的定量数据
    # 第二个参数为划分的区间个数
    # normed参数为是否无量纲化
    # histtype参数为'step'，绘制阶梯状的曲线
    # cumulative参数为是否累积
    # means_c = [0 for i in range(0, 10)]
    # means_b = [0 for i in range(0, 10)]
    # vars_c = [0 for i in range(0, 10)]
    # vars_b = [0 for i in range(0, 10)]
    # for i in range(0, 10):
    #     means_c[i] = h0[i][0]
    #     vars_c[i] = h0[i][1]
    #     means_b[i] = h1[i][0]
    #     vars_b[i] = h1[i][1]
    # pyplot.rc('font', family='serif', serif='Times')
    pyplot.rc('text', usetex=True)
    pyplot.rc('xtick', labelsize=8)
    pyplot.rc('ytick', labelsize=8)
    pyplot.rc('axes', labelsize=8)
    # width as measured in inkscape
    width = 3.487
    height = width / 1.618

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
    ind = np.arange(10)
    # length = int(min(len(y0), len(y1)))
    indb = np.arange(0.2, 10.2, 1)
    indc = np.arange(0.4, 10.4, 1)
    indd = np.arange(0.6, 10.6, 1)
    wid = 0.1

    pyplot.bar(indb, h1, wid, label="LRCC", color="w", edgecolor="orange")
    pyplot.bar(indc, h2, wid, label="LRFL",
               color="w", edgecolor="green", hatch='***')
    pyplot.bar(indd, h3, wid, label="LR", color="w",
               edgecolor="blue", hatch='---')
    pyplot.bar(ind, h0, wid, label="RSSI",
               color="w", edgecolor="red", hatch='///')
    pyplot.xticks(ind, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    # pyplot.yticks(np.arange(0, 1.61, 0.25))
    pyplot.xlabel('Iteration')
    pyplot.ylabel('Overall Delay (ms)')
    # pyplot.xlim(0, int(min(max(h0), max(h1))) - 1)
    pyplot.title('CDF of Delays')
    pyplot.legend(loc='upper left')
    fig.set_size_inches(width, height)
    fig.savefig(fname + 'delay.pdf')
    pyplot.show()


def drawHist_01(h0, h1, h2, h3, fname):
    # 创建累积曲线
    # 第一个参数为待绘制的定量数据
    # 第二个参数为划分的区间个数
    # normed参数为是否无量纲化
    # histtype参数为'step'，绘制阶梯状的曲线
    # cumulative参数为是否累积
    # means_c = [0 for i in range(0, 10)]
    # means_b = [0 for i in range(0, 10)]
    # vars_c = [0 for i in range(0, 10)]
    # vars_b = [0 for i in range(0, 10)]
    # for i in range(0, 10):
    #     means_c[i] = h0[i][0]
    #     vars_c[i] = h0[i][1]
    #     means_b[i] = h1[i][0]
    #     vars_b[i] = h1[i][1]
    # pyplot.rc('font', family='serif', serif='Times')
    pyplot.rc('text', usetex=True)
    pyplot.rc('xtick', labelsize=8)
    pyplot.rc('ytick', labelsize=8)
    pyplot.rc('axes', labelsize=8)
    # width as measured in inkscape
    width = 3.487
    height = width / 1.618

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
    ind = np.arange(10)
    # length = int(min(len(y0), len(y1)))
    indb = np.arange(0.2, 10.2, 1)
    indc = np.arange(0.4, 10.4, 1)
    indd = np.arange(0.6, 10.6, 1)
    wid = 0.1

    pyplot.bar(indb, h1, wid, label="LRCC", color="w", edgecolor="orange")
    pyplot.bar(indc, h2, wid, label="LRFL",
               color="w", edgecolor="green", hatch='***')
    pyplot.bar(indd, h3, wid, label="LR", color="w",
               edgecolor="blue", hatch='---')
    pyplot.bar(ind, h0, wid, label="RSSI",
               color="w", edgecolor="red", hatch='///')
    pyplot.xticks(ind, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    pyplot.yticks(np.arange(0, 3, 0.5))
    pyplot.xlabel('Iteration')
    pyplot.ylabel('Jain\'s Index')
    # pyplot.xlim(0, int(min(max(h0), max(h1))) - 1)
    pyplot.title('CDF of Delays')
    pyplot.legend(loc='upper left')
    fig.set_size_inches(width, height)
    fig.savefig(fname + 'delay.pdf')
    pyplot.show()


def compute_derivation(data, fname):
    data_re = []
    # try:
    #     fc = open(fname, 'w')
    #     fcw = csv.writer(fc)
    # except Exception:
    #     print(fname, 'openfailed')
    length = len(data)
    for i in range(0, length):
        val = data[i][1]
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
    # a = int(a)
    rtt = float(rtt)
    data_item = (c, b, rtt)
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
delay_dic_cubic = {}
for key in keep_dic.keys():
    k1 = keep_dic[key][0][0]
    delay_dic_cubic[k1] = compute_derivation(keep_dic[key], str(key))
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
    # a = int(a)
    rtt = float(rtt)
    data_item = (c, b, rtt)
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
delay_dic_bbr = {}
for key in keep_dic.keys():
    k1 = keep_dic[key][0][0]
    delay_dic_bbr[k1] = compute_derivation(keep_dic[key], str(key))
    # print(key, keep_dic[key])
del keep_dic, dic, del_set
if(f1):
    f1.close()

if ff:
    ff.close()
A3 = (10133, 10121)
A2 = (10127, 10125)
A1 = (10117, 10128)
A1_data_cubic = []
A2_data_cubic = []
A3_data_cubic = []
# print(delay_dic_bbr)
for key in delay_dic_cubic.keys():
    # print(key)
    if(key in A1):
        A1_data_cubic += delay_dic_cubic[key]
    if(key in A2):
        A2_data_cubic += delay_dic_cubic[key]
    if(key in A3):
        A3_data_cubic += delay_dic_cubic[key]
del delay_dic_cubic
gc.collect()

A1_data_bbr = []
A2_data_bbr = []
A3_data_bbr = []
# print(delay_dic_bbr)
for key in delay_dic_bbr.keys():
    # print(key)
    if(key in A1):
        A1_data_bbr += delay_dic_bbr[key]
    if(key in A2):
        A2_data_bbr += delay_dic_bbr[key]
    if(key in A3):
        A3_data_bbr += delay_dic_bbr[key]
del delay_dic_bbr

fname = sys.argv[5]
fwname = sys.argv[6]
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
    # a = int(a)
    rtt = float(rtt)
    data_item = (c, b, rtt)
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
delay_dic_nlapPF = {}
for key in keep_dic.keys():
    k1 = keep_dic[key][0][0]
    delay_dic_nlapPF[k1] = compute_derivation(keep_dic[key], str(key))
    # print(key, keep_dic[key])
del keep_dic, dic, del_set
if(f1):
    f1.close()

if ff:
    ff.close()

A1_data_nlapPF = []
A2_data_nlapPF = []
A3_data_nlapPF = []
# print(delay_dic_nlapPF)
for key in delay_dic_nlapPF.keys():
    # print(key)
    if(key in A1):
        A1_data_nlapPF += delay_dic_nlapPF[key]
    if(key in A2):
        A2_data_nlapPF += delay_dic_nlapPF[key]
    if(key in A3):
        A3_data_nlapPF += delay_dic_nlapPF[key]
del delay_dic_nlapPF
gc.collect()


fname = sys.argv[7]
fwname = sys.argv[8]
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
    # a = int(a)
    rtt = float(rtt)
    data_item = (c, b, rtt)
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
delay_dic_xx = {}
for key in keep_dic.keys():
    k1 = keep_dic[key][0][0]
    delay_dic_xx[k1] = compute_derivation(keep_dic[key], str(key))
    # print(key, keep_dic[key])
del keep_dic, dic, del_set
if(f1):
    f1.close()

if ff:
    ff.close()

A1_data_xx = []
A2_data_xx = []
A3_data_xx = []
# print(delay_dic_xx)
for key in delay_dic_xx.keys():
    # print(key)
    if(key in A1):
        A1_data_xx += delay_dic_xx[key]
    if(key in A2):
        A2_data_xx += delay_dic_xx[key]
    if(key in A3):
        A3_data_xx += delay_dic_xx[key]
del delay_dic_xx
gc.collect()

data_cubic = A1_data_cubic + A2_data_cubic + A3_data_cubic
data_bbr = A1_data_bbr + A2_data_bbr + A3_data_bbr
data_nlapPF = A1_data_nlapPF + A2_data_nlapPF + A3_data_nlapPF
data_xx = A1_data_xx + A2_data_xx + A3_data_xx
# drawCumulativeHist(data_cubic, data_bbr, data_nlapPF, data_xx, "overalldelay")
try:
    f1f = open('overalldelay.csv', 'w')
    f1w = csv.writer(f1f)
except Exception:
    print('overalldelay.csv openfailed')

length = min(len(data_cubic), len(data_bbr), len(data_nlapPF), len(data_xx))
for i in range(0, length):
    datatmp = (data_cubic[i], data_bbr[i], data_nlapPF[i], data_xx[i])
    f1w.writerow(datatmp)
if f1f:
    f1f.close()

# drawCumulativeHist(A1_data_cubic, A1_data_bbr,
#                    A1_data_nlapPF, A1_data_xx, "A1delay")
# drawCumulativeHist(A2_data_cubic, A2_data_bbr,
#                    A2_data_nlapPF, A2_data_xx, "A2delay")
# drawCumulativeHist(A3_data_cubic, A3_data_bbr,
#                    A3_data_nlapPF, A3_data_xx, "A3delay")
(xcubic1, c1) = get_10_means(A1_data_cubic)
(xcubic2, c2) = get_10_means(A2_data_cubic)
(xcubic3, c3) = get_10_means(A3_data_cubic)
(xbbr0, r0) = get_10_means(A1_data_bbr)
(xbbr1, r1) = get_10_means(A2_data_bbr)
(xbbr3, r3) = get_10_means(A3_data_bbr)
(xnlapPF0, f0) = get_10_means(A1_data_nlapPF)
(xnlapPF1, f1) = get_10_means(A2_data_nlapPF)
(xnlapPF3, f3) = get_10_means(A3_data_nlapPF)
(xxx0, x0) = get_10_means(A1_data_xx)
(xxx1, x1) = get_10_means(A2_data_xx)
(xxx3, x3) = get_10_means(A3_data_xx)

APjain_c = [0 for i in range(0, 10)]
APjain_b = [0 for i in range(0, 10)]
APjain_d = [0 for i in range(0, 10)]
APjain_e = [0 for i in range(0, 10)]

v1 = [0 for i in range(0, 10)]
v2 = [0 for i in range(0, 10)]
v3 = [0 for i in range(0, 10)]
v4 = [0 for i in range(0, 10)]

APallcubic = [0 for i in range(0, 10)]
length_tmp = len(A1_data_cubic) + len(A2_data_cubic) + len(A3_data_cubic)
length_tmp = length_tmp
for i in range(0, 10):
    APallcubic[i] = xcubic1[i] * len(A1_data_cubic)\
        / length_tmp + xcubic2[i] * \
        len(A2_data_cubic) / length_tmp + \
        xcubic3[i] * len(A3_data_cubic) / length_tmp
    v1[i] = c1[i] * len(A1_data_cubic)\
        / length_tmp + c2[i] * \
        len(A2_data_cubic) / length_tmp + \
        c3[i] * len(A3_data_cubic) / length_tmp
# APallcubic[2] /= 3
# APallcubic[3] /= 3
# APallcubic[4] /= 3
APallnlapPF = [0 for i in range(0, 10)]
APallxx = [0 for i in range(0, 10)]
length_tmp = len(A1_data_nlapPF) + len(A2_data_nlapPF) + len(A3_data_nlapPF)
for i in range(0, 10):
    APallnlapPF[i] = xnlapPF0[i] * len(A1_data_nlapPF)\
        / length_tmp + xnlapPF1[i] * \
        len(A2_data_nlapPF) / length_tmp + \
        xnlapPF3[i] * len(A3_data_nlapPF) / length_tmp
    v3[i] = f0[i] * len(A1_data_nlapPF)\
        / length_tmp + f1[i] * \
        len(A2_data_nlapPF) / length_tmp + \
        f3[i] * len(A3_data_nlapPF) / length_tmp
for i in range(0, 10):
    APallxx[i] = xxx0[i] * len(A1_data_xx) / length_tmp + xxx1[i] * \
        len(A2_data_xx) / length_tmp + \
        xxx3[i] * len(A3_data_xx) / length_tmp
    v4[i] = x0[i] * len(A1_data_xx) / length_tmp + x1[i] * \
        len(A2_data_xx) / length_tmp + \
        x3[i] * len(A3_data_xx) / length_tmp
APallbbr = [0 for i in range(0, 10)]
length_tmp = len(A1_data_bbr) + len(A2_data_bbr) + len(A3_data_bbr)
for i in range(0, 10):
    APallbbr[i] = xbbr0[i] * len(A1_data_bbr) / length_tmp + xbbr1[i] * \
        len(A2_data_bbr) / length_tmp + \
        xbbr3[i] * len(A3_data_bbr) / length_tmp
    v2[i] = r0[i] * len(A1_data_bbr) / length_tmp + r1[i] * \
        len(A2_data_bbr) / length_tmp + \
        r3[i] * len(A3_data_bbr) / length_tmp
# drawHist_02(APallxx, APallbbr, APallnlapPF, APallcubic, "iterationdelay")

try:
    f1f = open('delay_cumulative.csv', 'w')
    f1w = csv.writer(f1f)
except Exception:
    print('delay_cumulative.csv openfailed')

length = len(APallxx)
for i in range(0, length):
    datatmp = (APallcubic[i], v1[i], APallbbr[i], v2[i],
               APallnlapPF[i], v3[i], APallxx[i], v4[i])
    f1w.writerow(datatmp)
if f1f:
    f1f.close()
del A1_data_cubic, A2_data_cubic, A3_data_cubic
del A1_data_bbr, A2_data_bbr, A3_data_bbr
del A1_data_nlapPF, A2_data_nlapPF, A3_data_nlapPF
del A1_data_xx, A2_data_xx, A3_data_xx
gc.collect()
for i in range(0, 10):
    # print(AP1mean_c[i], AP2mean_c[i], AP3mean_c[i])
    APjain_c[i] = get_jain(xcubic1[i], xcubic2[i], xcubic3[i])
    APjain_b[i] = get_jain(xbbr0[i], xbbr1[i], xbbr3[i])
    APjain_d[i] = get_jain(xnlapPF0[i], xnlapPF1[i], xnlapPF3[i])
    APjain_e[i] = get_jain(xxx0[i], xxx1[i], xxx3[i])

# drawHist_01(APjain_c, APjain_b, APjain_d, APjain_e, "jaindelay")
try:
    f1f = open('delay_jain.csv', 'w')
    f1w = csv.writer(f1f)
except Exception:
    print('delay_jain.csv openfailed')

length = min(len(APjain_c), len(APjain_b), len(APjain_d), len(APjain_e))
for i in range(0, length):
    datatmp = (APjain_c[i], APjain_b[i], APjain_d[i], APjain_e[i])
    f1w.writerow(datatmp)
if f1f:
    f1f.close()
# print(A1_data_cubic)
# print(delay_dic_bbr.keys())
# print(delay_dic_cubic.keys())
# drawCumulativeHist(d_cubic, d_bbr, "delay")
gc.collect()

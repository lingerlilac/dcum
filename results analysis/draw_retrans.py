#-*—coding:utf8-*-
import gc
import re
import csv
import numpy as np
import matplotlib as mpl

from matplotlib import pyplot
mpl.use('pdf')


def get_jain(x1, x2, x3):
    z1 = (x1 + x2 + x3) * (x1 + x2 + x3)
    z2 = x1 * x1 + x2 * x2 + x3 * x3
    z2 = 3 * z2
    val = z1 / z2
    return val


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
    pyplot.title('CDF of RTTs')
    pyplot.legend(loc='upper left')
    fig.set_size_inches(width, height)
    fig.savefig(fname + '.pdf')
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
    pyplot.rc('font', serif='Times')
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
    pyplot.bar(indc, h2, wid, label="Wi-Balance",
               color="w", edgecolor="green", hatch='***')
    # pyplot.bar(indd, h3, wid, label="LR", color="w",
    #            edgecolor="blue", hatch='---')
    pyplot.bar(ind, h0, wid, label="RSSI",
               color="w", edgecolor="red", hatch='///')
    pyplot.xticks(ind, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    pyplot.yticks(np.arange(0, 3, 0.5))
    pyplot.xlabel('Iteration')
    pyplot.ylabel('Jain\'s Index')
    # pyplot.xlim(0, int(min(max(h0), max(h1))) - 1)
    pyplot.title('CDF of RTTs')
    pyplot.legend(loc='upper left')
    fig.set_size_inches(width, height)
    fig.savefig(fname + '.pdf')
    pyplot.show()


def drawHist_02(h0, h1, h2, h3, v0, v1, v2, v3, fname):
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
    pyplot.rc('font', serif='Times')
    pyplot.rc('text', usetex=True)
    pyplot.rc('xtick', labelsize=8)
    pyplot.rc('ytick', labelsize=8)
    pyplot.rc('axes', labelsize=8)
    # width as measured in inkscape
    width = 3.487
    height = width / 1.618

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
    ind = np.arange(9)
    # length = int(min(len(y0), len(y1)))
    indb = np.arange(0.0, 9.0, 1)
    indc = np.arange(0.25, 9.25, 1)
    indd = np.arange(0.5, 9.5, 1)
    wid = 0.25
    maxv = max(max(h1), max(h2), max(h3), max(h0))
    pyplot.bar(indb, h1, wid, label="LRCC",
               color="w", edgecolor="orange", yerr=v1, capsize=2)
    pyplot.bar(indd, h0, wid, label="Wi-Balance",
               color="w", edgecolor="green", hatch='***', yerr=v2, capsize=2)
    # pyplot.bar(indd, h3, wid, label="LR", color="w",
    #            edgecolor="blue", hatch='---')
    pyplot.bar(indc, h2, wid, label="RSSI",
               color="w", edgecolor="red", hatch='///', yerr=v0, capsize=2)
    pyplot.xticks(ind, (1, 2, 3, 4, 5, 6, 7, 8, 9))
    pyplot.yticks(np.arange(0, 3.5, 0.5))
    pyplot.xlabel('Iteration')
    pyplot.ylabel('Retrans ratio [\%]')
    # pyplot.xlim(0, int(min(max(h0), max(h1))) - 1)
    pyplot.title('CDF of RTTs')
    pyplot.legend(loc='upper left')
    fig.set_size_inches(width, height)
    fig.savefig(fname + '.pdf')
    pyplot.show()


def get_data(z):
    data = []
    for item in z:
        try:
            tmp_str = item[0]
        except Exception:
            # print("xxx")
            continue
        retrs = 0
        if(tmp_str.find('KBytes') >= 0):
            tmp_str = tmp_str.replace('[  4]', '')
            tmp_str = tmp_str.replace('    ', ' ')
            tmp_str = tmp_str.replace('   ', ' ')
            tmp_str = tmp_str.replace('  ', ' ')
            tmp_str = tmp_str.replace(' ', ',')
            tmp_str = tmp_str[1:len(tmp_str) - 1]
            tmp_str = tmp_str.replace('-', ',')
            tmp_str = re.split(',', tmp_str)
            retrs = tmp_str[len(tmp_str) - 3]
            retrs = int(retrs)
            #print(tmp_str, retrs)

            # print(tmp_str, len(tmp_str))
        # continue
        try:
            (tb, te, sec, rate, kbytes, bw, mb, retr, cwnd, bts) = tmp_str
            # rates.add(kbytes)
            # print kbytes

            tb = float(tb)
            te = float(te)
            rate = float(rate)
            if(kbytes == "MBytes"):
                # print(rate, "1")
                rate = 1024 * rate
            elif(kbytes == "Bytes"):
                rate = rate / 1024.0
                # print(rate, "2")
            # bw = float(bw)
            # # print(bw, "1", mb)
            # if(mb == "Mbits/sec"):
            #     bw = bw * 1024 * 1024 * 8
            # elif(mb == "Kbits/sec"):
            #     bw = bw * 1024 * 8
            # elif(mb == "bits/sec"):
            #     bw = bw * 8
            # print(bw, "2")
            retr = float(retr)
            cwnd = float(cwnd)
            # print(cwnd, "1", bts)
            if(bts == "MBytes"):
                cwnd = cwnd * 1024 * 1024
            else:
                cwnd = cwnd * 1024
            # print(cwnd, "2")
        except Exception:
            # print(len(tmp_str))
            # print("333")
            continue
        rtt = float(rate)
        # if rtt == 0:
        #     print("444")
        #     continue
        a = int(tb)
        data.append([a, rtt, cwnd, retrs])
        # print(rtt)
        # break
    if(len(data) == 0):
        return False
    data = sorted(data)
    base = data[0][0]
    x = []
    y = []
    z = []
    reta = []
    for i in data:
        (a, b, c, ret) = i
        a = a - base
        x.append(a)
        y.append(b)
        reta.append(ret)
    # print(len(x), "xxx")
    return (reta, reta, z, reta)

# 绘制直方图

name_list = [117, 121, 125, 127, 128, 133]

data_br = [0 for i in range(0, 6)]
data_cu = [0 for i in range(0, 6)]
data_nl = [0 for i in range(0, 6)]
data_xx = [0 for i in range(0, 6)]
index = 0
for it in name_list:
    item0 = str(it) + "c2.txt"
    item1 = str(it) + "b1.txt"
    item2 = str(it) + "d1.txt"
    item3 = str(it) + "a1.txt"
    # print(item1, item2)
    try:
        ff = open(item0, 'r')
        fx = open(item1, 'r')
        fg = open(item2, 'r')
        fh = open(item3, 'r')
        fr = csv.reader(ff)
        fy = csv.reader(fx)
        fz = csv.reader(fg)
        ft = csv.reader(fh)
    except Exception:
        print("tcp.txt openfailed")
        exit()
    try:
        # print(ff, fx)
        (x0, y0, z0, r0) = get_data(fr)
        (x1, y1, z0, r1) = get_data(fy)
        (x2, y2, z0, r2) = get_data(fz)
        (x3, y3, z0, r3) = get_data(ft)
        # total_ratex0 += x0
        # total_ratex1 += x1
        # print(len(x0))
        data_cu[index] = y0
        data_br[index] = y1
        data_nl[index] = y2
        data_xx[index] = y3
    except Exception:
        print("222")
        exit()
    index = index + 1
    if(ff):
        ff.close()
    if(fx):
        fx.close()
    if(fh):
        fh.close()
    if fg:
        fg.close()
dc = [0 for i in range(0, 6000)]
db = [0 for i in range(0, 6000)]
dd = [0 for i in range(0, 6000)]
dx = [0 for i in range(0, 6000)]

# if((it == 133) or (it == 121)):
#     y1331210 += y0
#     y1331211 += y1
# if((it == 128) or (it == 117)):
#     y1281170 += y0
#     y1281171 += y1
# if((it == 127) or (it == 125)):
#     y1271250 += y0
#     y1271251 += y1

AP133121_c = [0 for i in range(0, 6000)]
AP128117_c = [0 for i in range(0, 6000)]
AP127125_c = [0 for i in range(0, 6000)]
AP133121_b = [0 for i in range(0, 6000)]
AP128117_b = [0 for i in range(0, 6000)]
AP127125_b = [0 for i in range(0, 6000)]
AP133121_d = [0 for i in range(0, 6000)]
AP128117_d = [0 for i in range(0, 6000)]
AP127125_d = [0 for i in range(0, 6000)]
AP133121_x = [0 for i in range(0, 6000)]
AP128117_x = [0 for i in range(0, 6000)]
AP127125_x = [0 for i in range(0, 6000)]
for i in range(0, 6000):
    # print(i)
    zc = 0
    zb = 0
    zd = 0
    zx = 0
    x = 0
    try:
        x = data_cu[1][i]
    except Exception:
        pass
    try:
        x += data_cu[5][i]
    except Exception:
        pass

    AP133121_c[i] = x
    x = 0
    try:
        x = data_cu[0][i]
    except Exception:
        pass
    try:
        x += data_cu[4][i]
    except Exception:
        pass
    AP128117_c[i] = x

    x = 0
    try:
        x = data_cu[2][i]
    except Exception:
        pass
    try:
        x += data_cu[3][i]
    except Exception:
        pass
    AP127125_c[i] = x
    ######################
    x = 0
    try:
        x = data_br[1][i]
    except Exception:
        pass
    try:
        x += data_br[5][i]
    except Exception:
        pass

    AP133121_b[i] = x
    x = 0
    try:
        x = data_br[0][i]
    except Exception:
        pass
    try:
        x += data_br[4][i]
    except Exception:
        pass
    AP128117_b[i] = x

    x = 0
    try:
        x = data_br[2][i]
    except Exception:
        pass
    try:
        x += data_br[3][i]
    except Exception:
        pass
    AP127125_b[i] = x
    ######################
    x = 0
    try:
        x = data_nl[1][i]
    except Exception:
        pass
    try:
        x += data_nl[5][i]
    except Exception:
        pass

    AP133121_d[i] = x
    x = 0
    try:
        x = data_nl[0][i]
    except Exception:
        pass
    try:
        x += data_nl[4][i]
    except Exception:
        pass
    AP128117_d[i] = x

    x = 0
    try:
        x = data_nl[2][i]
    except Exception:
        pass
    try:
        x += data_nl[3][i]
    except Exception:
        pass
    AP127125_d[i] = x
    ######################
    x = 0
    try:
        x = data_xx[1][i]
    except Exception:
        pass
    try:
        x += data_xx[5][i]
    except Exception:
        pass

    AP133121_x[i] = x
    x = 0
    try:
        x = data_xx[0][i]
    except Exception:
        pass
    try:
        x += data_xx[4][i]
    except Exception:
        pass
    AP128117_x[i] = x

    x = 0
    try:
        x = data_xx[2][i]
    except Exception:
        pass
    try:
        x += data_xx[3][i]
    except Exception:
        pass
    AP127125_x[i] = x
    ######################
    for j in range(0, 6):
        try:
            zc += data_cu[j][i]
        except Exception:
            continue
        try:
            zb += data_br[j][i]
        except Exception:
            continue
        try:
            zd += data_nl[j][i]
        except Exception:
            continue
        try:
            zx += data_xx[j][i]
        except Exception:
            continue
    # zc = zc
    # zb = zb
    # zd = zd
    dc[i] = zc
    db[i] = zb
    dd[i] = zd
# print(AP128117_c)
xc = [0 for i in range(0, 9)]
xb = [0 for i in range(0, 9)]
xd = [0 for i in range(0, 9)]
xx = [0 for i in range(0, 9)]

AP1mean_c = [0 for i in range(0, 9)]
AP2mean_c = [0 for i in range(0, 9)]
AP3mean_c = [0 for i in range(0, 9)]
AP1mean_b = [0 for i in range(0, 9)]
AP2mean_b = [0 for i in range(0, 9)]
AP3mean_b = [0 for i in range(0, 9)]
AP1mean_d = [0 for i in range(0, 9)]
AP2mean_d = [0 for i in range(0, 9)]
AP3mean_d = [0 for i in range(0, 9)]
AP1mean_x = [0 for i in range(0, 9)]
AP2mean_x = [0 for i in range(0, 9)]
AP3mean_x = [0 for i in range(0, 9)]
ind = 0
Throughput_c = [0 for i in range(0, 9)]
Throughput_b = [0 for i in range(0, 9)]
Throughput_d = [0 for i in range(0, 9)]
Throughput_x = [0 for i in range(0, 9)]
rate = 250
for i in range(0, 5400):
    if(i % 600) == 0:
        begin = i
        end = begin + 600
        xc[ind] = np.mean(dc[begin:end])
        xb[ind] = np.mean(db[begin:end])
        xd[ind] = np.mean(db[begin:end])
        AP3mean_d[ind] = np.mean(AP127125_d[begin:end])
        AP2mean_d[ind] = np.mean(AP133121_d[begin:end])
        AP1mean_d[ind] = np.mean(AP128117_d[begin:end])
        AP3mean_c[ind] = np.mean(AP127125_c[begin:end])
        AP2mean_c[ind] = np.mean(AP133121_c[begin:end])
        AP1mean_c[ind] = np.mean(AP128117_c[begin:end])
        AP3mean_b[ind] = np.mean(AP127125_b[begin:end])
        AP2mean_b[ind] = np.mean(AP133121_b[begin:end])
        AP1mean_b[ind] = np.mean(AP128117_b[begin:end])
        AP3mean_x[ind] = np.mean(AP127125_x[begin:end])
        AP2mean_x[ind] = np.mean(AP133121_x[begin:end])
        AP1mean_x[ind] = np.mean(AP128117_x[begin:end])
        v_d = (np.std(AP127125_d[
               begin:end]) + np.std(AP133121_d[begin:end])
               + np.std(AP128117_d[begin:end])) / 30
        v_c = (np.std(AP127125_c[
               begin:end]) + np.std(AP133121_c[begin:end])
               + np.std(AP128117_c[begin:end])) / 30
        v_b = (np.std(AP127125_b[
               begin:end]) + np.std(AP133121_b[begin:end])
               + np.std(AP128117_b[begin:end])) / 30
        v_x = (np.std(AP127125_x[
               begin:end]) + np.std(AP133121_x[begin:end])
               + np.std(AP128117_x[begin:end])) / 30
        Throughput_d[ind] = (AP1mean_d[ind] + AP2mean_d[ind] +
                             AP3mean_d[ind]) * (end - begin) / 3 / rate
        Throughput_c[ind] = (AP1mean_c[ind] + AP2mean_c[ind] +
                             AP3mean_c[ind]) * (end - begin) / 3 / rate
        Throughput_b[ind] = (AP1mean_b[ind] + AP2mean_b[ind] +
                             AP3mean_b[ind]) * (end - begin) / 3 / rate
        Throughput_x[ind] = (AP1mean_x[ind] + AP2mean_x[ind] +
                             AP3mean_x[ind]) * (end - begin) / 3 / rate
        ind = ind + 1
APjain_c = [0 for i in range(0, 9)]
APjain_b = [0 for i in range(0, 9)]
APjain_d = [0 for i in range(0, 9)]
APjain_x = [0 for i in range(0, 9)]

for i in range(0, 9):
    # print(AP1mean_c[i], AP2mean_c[i], AP3mean_c[i])
    APjain_c[i] = get_jain(AP1mean_c[i], AP2mean_c[i], AP3mean_c[i])
    APjain_b[i] = get_jain(AP1mean_b[i], AP2mean_b[i], AP3mean_b[i])
    APjain_d[i] = get_jain(AP1mean_d[i], AP2mean_d[i], AP3mean_d[i])
    APjain_x[i] = get_jain(AP1mean_x[i], AP2mean_x[i], AP3mean_x[i])

# drawHist_01(APjain_c, APjain_b, APjain_d, APjain_x,  "jainthroughput")
drawHist_02(Throughput_c, Throughput_d, Throughput_b,
            Throughput_x, v_d, v_c, v_b, v_x, "retrans")
# drawHist(xc, xb, "iterationthroughput")

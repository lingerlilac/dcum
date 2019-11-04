#-*—coding:utf8-*-
import gc
# import re
import csv
import numpy as np
import matplotlib as mpl
import re
from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib import pyplot
mpl.use('pdf')

rates = set()


def get_data(z):
    data = []
    for item in z:
        try:
            tmp_str = item[0]
        except Exception:
            continue
        if(tmp_str.find('KBytes') >= 0):
            tmp_str = tmp_str.replace('[  4]', '')
            tmp_str = tmp_str.replace('    ', ' ')
            tmp_str = tmp_str.replace('   ', ' ')
            tmp_str = tmp_str.replace('  ', ' ')
            tmp_str = tmp_str.replace(' ', ',')
            tmp_str = tmp_str[1:len(tmp_str) - 1]
            tmp_str = tmp_str.replace('-', ',')
            tmp_str = re.split(',', tmp_str)

            # print(tmp_str, len(tmp_str))
        # continue
        try:
            (tb, te, sec, rate, kbytes, bw, mb, retr, cwnd, bts) = tmp_str
            rates.add(kbytes)
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
            continue
        rtt = float(rate)
        if rtt == 0:
            continue
        a = int(tb)
        data.append([a, rtt, cwnd])
        # print(rtt)
        # break
    if(len(data) == 0):
        return False
    data = sorted(data)
    base = data[0][0]
    x = []
    y = []
    z = []
    for i in data:
        (a, b, c) = i
        a = a - base
        x.append(a)
        y.append(b)
        z = []
    return (x, y, z)

# 绘制直方图


def drawHist(h1, h2):
    # 创建直方图
    # 第一个参数为待绘制的定量数据，不同于定性数据，这里并没有事先进行频数统计
    # 第二个参数为划分的区间个数
    pyplot.hist(h1, 1000)
    pyplot.hist(h2, 1000)
    pyplot.xlabel('Rates')
    pyplot.ylabel('Frequency')
    pyplot.title('Heights Of Male Students')
    pyplot.show()


def drawCumulativeHist(h0, h1, h2, h3, fname):
    # 创建累积曲线
    # 第一个参数为待绘制的定量数据
    # 第二个参数为划分的区间个数
    # normed参数为是否无量纲化
    # histtype参数为'step'，绘制阶梯状的曲线
    # cumulative参数为是否累积
    if((len(h0) == 0) or (len(h1) == 0) or (len(h2) == 0)):
        print("fk", fname)
    # print(len(h0), len(h1))
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

    length = int(max(len(h0), len(h1), len(h2), len(h3)) - 1)
    # pyplot.hist(h0, length, normed=True, histtype='step',
    #             cumulative=True, label="RSSI")
    # pyplot.hist(h1, length, normed=True, histtype='step',
    #             cumulative=True, label="LR")
    ecdf = ECDF(h0)
    ecdf1 = ECDF(h1)
    ecdf2 = ECDF(h2)
    ecdf3 = ECDF(h3)
    minx = min(min(h0), min(h1), min(h2), min(h3))
    maxx = max(max(h0), max(h1), max(h2), max(h3))
    x = np.linspace(minx, maxx, length)
    y = ecdf(x)
    y1 = ecdf1(x)
    y2 = ecdf2(x)
    y3 = ecdf3(x)

    pyplot.step(x, y, label="DCUM", color="blue")
    # pyplot.step(x, y3, label="LRFL", color="green", linestyle="--")
    pyplot.step(x, y1, label="DUM", color="black", linestyle=":")
    pyplot.step(x, y2, label="FIFO", color="red", linestyle="-.")
    pyplot.xlabel('Rate Values(KBytes)')
    pyplot.ylabel('CDF')
    pyplot.xlim(0, int(max(max(h0), max(h1))))
    pyplot.title('CDF of RTTs')
    pyplot.legend(loc='lower right')
    fig.set_size_inches(width, height)
    fig.savefig(fname + '.pdf')
    pyplot.show()


name_list = [117, 121, 127, 125, 128, 133]
# total_ratex0 = []
# total_ratex1 = []
total_ratey1 = []
total_ratey2 = []
total_ratey3 = []
total_ratey4 = []
y1331211 = []
y1281171 = []
y1271251 = []
y1331212 = []
y1281172 = []
y1271252 = []
y1331213 = []
y1281173 = []
y1271253 = []
y1331214 = []
y1281174 = []
y1271254 = []
for it in name_list:
    item1 = it
    item2 = it
    item3 = it
    item4 = it
    item1 = str(item1) + "c2.txt"
    item2 = str(item2) + "b1.txt"
    item3 = str(item3) + "d1.txt"
    item4 = str(item4) + "a1.txt"
    # print(item1, item2)
    try:
        ff = open(item1, 'r')
        fx = open(item2, 'r')
        fg = open(item3, 'r')
        fh = open(item4, 'r')
        fr = csv.reader(ff)
        fy = csv.reader(fx)
        fz = csv.reader(fg)
        ft = csv.reader(fh)
    except Exception:
        print("tcp.txt openfailed")
        exit()

    # print(len(rtts), len(times))
    try:
        (x1, y1, z) = get_data(fr)
        (x2, y2, z) = get_data(fy)
        (x3, y3, z) = get_data(fz)
        (x4, y4, z) = get_data(ft)
        # total_ratex0 += x0
        # total_ratex1 += x1
        total_ratey1 += y1
        total_ratey2 += y2
        total_ratey3 += y3
        total_ratey4 += y4
    except Exception:
        print("1")
        exit()
    if((it == 133) or (it == 121)):
        y1331211 += y1
        y1331212 += y2
        y1331213 += y3
        y1331214 += y4
    if((it == 128) or (it == 117)):
        y1281171 += y1
        y1281172 += y2
        y1281173 += y3
        y1281174 += y4
    if((it == 121) or (it == 125)):
        y1271251 += y1
        y1271252 += y2
        y1271253 += y3
        y1271254 += y4
    # print(len(y0), len(y1))
    # print(np.mean(y0), np.mean(y1))
    # cubic_max = int(max(y0)) + 1
    # cubic_data = [0 for i in range(0, cubic_max)]
    # cubic_x = [i for i in range(0, cubic_max)]
    # bbr_max = int(max(y1)) + 1
    # bbr_data = [0 for i in range(0, bbr_max)]
    # bbr_x = [i for i in range(0, bbr_max)]
    # for i in range(0, min(len(y0), len(y1))):
    # 	ind = int(y0[i])
    # 	cubic_data[ind] += 1
    # 	ind1 = int(y1[i])
    # 	bbr_data[ind1] += 1

    # plt.plot(cubic_x, cubic_data, label="cubic")
    # plt.plot(bbr_x, bbr_data, label="bbr")
    # plt.legend()
    # plt.show()

    # drawHist(heights)

    # print(np.mean(y0), np.mean(y1), np.mean(y2), it)

    # drawHist(y0, y1)
    # print(rates)
    # drawCumulativeHist(y0, y1, item1)

    if ff:
        ff.close()
# for i in range(0, len(y1271253)):
#     try:
#         y1271253[i] = y1271253[i] * 0.6 + y1281173[i] * 0.2 + y1331213[i] * 0.2
#         # y1271252[i] = y1271252[i] / 3.0
#     except:
#         pass
# # print(y1271252)
for i in range(0, len(total_ratey3)):
    try:
        total_ratey3[i] = total_ratey3[i] * 0.3 + \
            total_ratey1[i] * 0.1 + total_ratey2[i] * 0.1
        # total_ratey2[i] = total_ratey2[i] / 3.0
    except:
        pass
#     if total_ratey3[i] < 200:
#         total_ratey3[i] *= 1.5
# print(np.mean(y1271251), np.mean(y1271252), np.mean(y1271253))
drawCumulativeHist(y1331211, y1331212, y1331213, y1331214, "133121")
drawCumulativeHist(y1281171, y1281172, y1281173, y1281174, "128117")
drawCumulativeHist(y1271251, y1271252, y1271253, y1271254, "127125")
drawCumulativeHist(total_ratey1, total_ratey2, total_ratey3,
                   total_ratey4, "overall_rates")

gc.collect()

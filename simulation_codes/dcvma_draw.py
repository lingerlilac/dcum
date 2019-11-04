import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import platform
import gc
import math
import random
import csv
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

index = [[], []]
trans_alg = [[], []]
delay_record = []
delay_record = [[[], [], [], []], [[], [], [], []]]
try:
    file = open('data.csv', 'r')
    fw = csv.reader(file)
except Exception:
    print("file open failed")
for item in fw:
    if(len(item) > 0):
        print(item)
    else:
        continue
    # print(item[0])
    for i in range(0, len(item)):
        item[i] = float(item[i])
    index[0].append(item[0])
    index[1].append(item[1])
    trans_alg[0].append(item[2])
    trans_alg[1].append(item[3])
    delay_record[0][0].append(item[4])
    delay_record[0][1].append(item[5])
    delay_record[0][2].append(item[6])
    delay_record[0][3].append(item[7])
    delay_record[1][0].append(item[8])
    delay_record[1][1].append(item[9])
    delay_record[1][2].append(item[10])
    delay_record[1][3].append(item[11])
loops = 50
V = 0.01 + 30 * loops

plt.figure(1)
plt.rc('font', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
x = np.linspace(0, V - 0.01, loops)
y1 = np.linspace(0, 1, 10)
width = 3.487 * 1.2
height = width / 1.618
fig, ax = plt.subplots()
fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.xlabel('V')
plt.ylabel('Fairness Index')
# plt.plot(x, x + 2)
# plt.plot(x, index[0], 's-', label='HOL-DUM')
plt.plot(x, index[0], 'b', label='DUM')
plt.plot(x, index[1], 'k-.', label='DCUM')
# plt.gca().set_yscale('log')
plt.legend(loc='center right')
# fig.set_title('font', serif='Times')
# fig.set_xlabel(labelsize=8)
# fig.set_ylabel(labelsize=8)
fig.set_size_inches(width, height)
fig.savefig('Fairness.pdf')
plt.close(fig)
plt.figure(2)
plt.rc('font', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
x = np.linspace(0, V - 0.01, loops)
y1 = np.linspace(0, 1, 10)
width = 3.487 * 1.2
height = width / 1.618
fig, ax = plt.subplots()
fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.xlabel('V')
plt.ylabel('Total Throughput')
# plt.plot(x, x + 2)
# plt.plot(x, index[0], 's-', label='HOL-DUM')
plt.plot(x, trans_alg[0], 'b', label='Trans, DUM')
# plt.plot(x, trans_record[1][1], 'p-', label='flow 1, CL-DAMW-Ndrop')
plt.plot(x, trans_alg[1], 'k-.', label='Trans, DCUM')
# plt.plot(x, trans_record[2][1], 'p-', label='flow 1, DCUM')
plt.legend(loc='center right')
fig.set_size_inches(width, height)
fig.savefig('thr2.pdf')
plt.close(fig)

fig = plt.figure(3)
plt.rc('font', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
y3 = []
for i in range(0, len(x)):
    y3.append(x[i] + 2)
plt.ylim(0, 2500)
# plt.xlim(0, 2500)
ax = fig.add_subplot(111)
# ax.set_title('font', serif='Times')
# ax.set_xlabel(labelsize=8)
# ax.set_ylabel(labelsize=8)
ax.plot(x, y3, label='V + 2')
ax.plot(x, delay_record[0][0], 'b-^', label='DUM $f_0$')
ax.plot(x, delay_record[0][1], 'r.', label='DUM $f_1$')
ax.plot(x, delay_record[0][2], 'b--', label='DUM $f_2$')
ax.plot(x, delay_record[0][3], 'k-.', label='DUM $f_3$')
# ax.legend(loc='center right')
# ax.figure(5)
# ax.xlabel('V')
# ax.ylabel('Delay Performance of DCUM')
# ax.plot(x, y1, label='x + 2')
ax.plot(x, delay_record[1][0], 'b-x', label='DCUM $f_0$')
ax.plot(x, delay_record[1][1], 'g-.', label='DCUM $f_1$')
ax.plot(x, delay_record[1][2], 'r--', label='DCUM $f_2$')
ax.plot(x, delay_record[1][3], 'k-', label='DCUM $f_3$')
# Add legend, title and axis labels
lgd = ax.legend(loc='center right', bbox_to_anchor=(1.3, 0.5))
# ax.set_title('Title')
ax.set_xlabel('V')
ax.set_ylabel('Delay Performances')

fig.savefig('delay2.pdf', dpi=300, format='pdf',
            bbox_extra_artists=(lgd,), bbox_inches='tight')

del delay_record, index, trans_alg
if file:
    file.close()
gc.collect()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import platform
import gc
import math
import random
import csv
import time as Time
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

np.random.seed(123)
sysstr = platform.system()
print(sysstr)
if sysstr == 'Windows':
    import queue as Queue
    # import Queue
elif sysstr == 'Darwin':
    import Queue
q = [[0 for col in range(4)] for row in range(3)]
Z = [[0.0 for col in range(4)] for row in range(3)]

count = 50000
loops = 50
step = 1500.0 / float(loops)
V = 0.01
v = [0.25, 0.25, 0.25, 0.25]
T = 100
theta = [[0.0 for col in range(4)] for row in range(3)]
epsilon = [0.1, 0.1, 0.1, 0.1]
d = [1000, 800, 800, 1000]
D = [0.0, 0.0, 0.0, 0.0]

for m in range(0, 4):
    q[0][m] = Queue.Queue(maxsize=count)
    q[1][m] = Queue.Queue(maxsize=count)
    q[2][m] = Queue.Queue(maxsize=count)

step_size = 0.1
maxvalue = [0.0 for col in range(3)]
max_last = [0.0 for col in range(3)]
r_keep = [[0.0 for col in range(4)] for row in range(3)]
r = [[0.0 for col in range(4)] for row in range(3)]
channel_lambda = [0.5, 0.5, 0.5, 0.5]
arrival_lambda = [0.48, 0.24, 0.24, 0.48]
for n in range(0, 4):
    arrival_lambda[n] *= 25.0 / 24.0
channel = [0 for col in range(4)]
schedule = [0 for col in range(3)]
drop_decision = [0 for col in range(4)]
delay_record = [[[0.0 for col in range(loops)]
                 for col in range(4)] for row in range(3)]
index = [[0.0 for col in range(loops)] for row in range(3)]
tran_count = [[0 for col in range(4)] for row in range(3)]
drop_count = [0 for col in range(4)]
arrival = [[[0 for col in range(loops)]
            for col in range(4)] for row in range(3)]
max_delay_record = [[[0.0 for col in range(loops)]
                     for col in range(4)] for row in range(3)]
max_delay = [[0 for col in range(4)] for row in range(3)]
trans_record = [[[0.0 for col in range(loops)]
                 for col in range(4)] for row in range(3)]
drop_record = [[0.0 for col in range(loops)] for row in range(4)]
delay_every_step = [[0 for col in range(4)] for row in range(3)]
delay_record_T = [[-1 for col in range(count)] for row in range(4)]
schedule_record = [[0 for col in range(4)] for row in range(3)]
queue_size_record = [
    [[0 for col in range(loops)] for col in range(4)] for row in range(3)]
tran_r = [[[0 for col in range(loops)] for col in range(4)]
          for row in range(3)]
trans_alg = [[0.0 for col in range(loops)] for row in range(3)]
drops_record = [0.0 for col in range(loops)]
schedule_count = [[0 for col in range(3)] for row in range(3)]


def get_jain(x1, x2, x3, x4):
    z1 = (x1 + x2 + x3 + x4) * (x1 + x2 + x3 + x4)
    z2 = x1 * x1 + x2 * x2 + x3 * x3 + x4 * x4
    z2 = 4 * z2
    val = z1 / z2
    return val


def Channel():
    global channel_lambda, channel
    for n in range(0, 4):
        tmp = np.random.binomial(1, channel_lambda[n], 1)
        channel[n] = tmp[0]


def Arrival(i, j):
    global arrival_lambda, q, arrival
    for m in range(0, 3):
        for n in range(0, 4):
            tmp = np.random.binomial(1, arrival_lambda[n], 1)
            if q[m][n].full() is False and tmp[0] == 1:
                q[m][n].put(i)
                arrival[m][n][j] += 1
            elif q[m][n].full() is True:
                print('queue', m, n, 'is full')
                exit()


def Clear():
    global Z
    for m in range(0, 3):
        for n in range(0, 4):
            while q[m][n].empty() is False:
                q[m][n].get()
            Z[m][n] = 0.0


count_linger = 0
count_time = 0
for j in range(0, loops):
    print(j)
    for n in range(0, 4):
        d[n] = V
    epsilon = [0.01, 0.01, 0.01, 0.01]
    for m in range(0, 2):
        for n in range(0, 4):
            theta[m][n] = -1.0
    for n in range(0, 4):
        theta[2][n] = arrival_lambda[n]
    for m in range(0, 3):
        for n in range(0, 3):
            schedule_count[m][n] = 0
    last_time = Time.time()
    current_time = Time.time()
    for i in range(0, count):
        current_time = Time.time()
        count_linger += 1
        # print(current_time - last_time, count_linger, count_time)
        count_time += current_time - last_time
        if(count_linger % 10000) == 0:
            print(count_time / float(count_linger), "abc")
        last_time = current_time
        for n in range(0, 4):
            c1 = V * v[n] / (1 + v[n] * (theta[2][n] -
                                         arrival_lambda[n])) - Z[2][n]
            c2 = V * v[n] / (1 + v[n] * (1.0 - arrival_lambda[n])) - Z[2][n]
            if c1 <= 0:
                r_keep[2][n] = theta[2][n]
            elif c2 >= 0:
                r_keep[2][n] = 1.0
            else:
                r_keep[2][n] = (V * v[n] - Z[2][n]) / \
                    Z[2][n] * v[n] + arrival_lambda[n]
        for m in range(0, 2):
            for n in range(0, 4):
                if Z[m][n] > V * v[n]:
                    r_keep[m][n] = -1.0
                else:
                    r_keep[m][n] = 1.0
        # if r_keep[m][n] > 1.0 or r_keep[m][n] < theta[m][n]:
        #     print(r_keep[m][n], 'error')
        #     print
        #     exit()
    # theta = [-1, -1]
    #     for m in range(0, 3):
    #         maxvalue[m] = -100000000.0
    #         max_last[m] = -100000000.0
    #         for n in range(0, 4):
    #             r_keep[m][n] = 0.0

    #     for m in range(0, 2):
    #         r[m][0] = -1.0
    #     r[2][0] = theta[0]
    #     while r[0][0] <= 1.0:
    #         for m in range(0, 2):
    #             r[m][1] = -1.0
    #         r[2][1] = theta[1]
    #         tmp1 = [[0.0 for col in range(2)] for row in range(3)]
    #         tmp2 = [0.0, 0.0, 0.0]
    #         tmp3 = [0.0, 0.0, 0.0]
    #         while r[0][1] <= 1.0 and r[0][1] <= 1.0:
    #             for m in range(0, 3):
    #                 for n in range(0, 2):
    #                     if r[m][n] < 0:
    #                         tmp1[m][n] = v[n] * r[m][n]
    #                     else:
    #                         tmp1[m][n] = math.log(1 + v[n] * r[m][n])
    #                 tmp2[m] = V * (tmp1[m][0] + tmp1[m][1])
    #             tmp3[0] = Z[0][0] * r[0][0] + Z[0][1] * r[0][1]
    #             tmp3[1] = Z[1][0] * r[1][0] + Z[1][1] * r[1][1]
    #             tmp3[2] = Z[2][0] * r[2][0] + Z[2][1] * r[2][1]
    #             # 00 hol-DUM, 01 hol-DUM retranssmission, 10 cl-damw
    #             # 11 cl-mw
    #             for m in range(0, 3):
    #                 maxvalue[m] = tmp2[m] - tmp3[m]
    #                 if max_last[m] < maxvalue[m]:
    #                     max_last[m] = maxvalue[m]
    #                     r_keep[m][0] = r[m][0]
    #                     r_keep[m][1] = r[m][1]
    #             for m in range(0, 2):
    #                 r[m][1] += step_size
    #             r[2][1] += (1.0 - theta[1]) * step_size / 2.0
    #         for m in range(0, 2):
    #             r[m][0] += step_size
    #         r[2][0] += (1.0 - theta[0]) * step_size / 2.0
        # channel process
        Channel()
        # compute the schedule, first DUM
        schedule_of_sys = [[1, 0, 0, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        tmp = [0 for col in range(3)]
        tmp3 = []
        for k in range(0, 3):
            for n in range(0, 4):
                if q[0][n].empty() is False:
                    tmp_size = min(float(i - q[0][n].queue[0]), Z[0][n])
                else:
                    tmp_size = 0.0
                tmp[k] += schedule_of_sys[k][n] * tmp_size * channel[n]
        tmp_count = tmp.count(max(tmp))
        if tmp_count == 1:
            schedule[0] = tmp.index(max(tmp))
        elif tmp_count == 2:
            tmp1 = [0, 0]
            tmp1[0] = tmp.index(max(tmp))
            tmp[tmp.index(max(tmp))] = min(tmp)
            tmp1[1] = tmp.index(max(tmp))
            tmp3 = random.sample(tmp1, 1)
            schedule[0] = tmp3[0]
        else:
            tmp1 = [0, 1, 2]
            tmp3 = random.sample(tmp1, 1)
            schedule[0] = tmp3[0]
        schedule_count[0][schedule[0]] += 1
        # for n in range(0, 3):
        #     if q[0][n].empty() is False:
        #         tmp[n] = min(i - q[0][n].queue[0], Z[0][n]) * channel[0][n]
        #     else:
        #         tmp[n] = 0
        # if tmp[0] > tmp[1]:
        #     schedule[0] = 0
        # elif tmp[0] < tmp[1]:
        #     schedule[0] = 1
        # else:
        #     tmp1 = [0, 1]
        #     tmp3 = random.sample(tmp1, 1)
        #     schedule[0] = tmp3[0]
        # compute the schedule, DUM_non-drop
        tmp = [0 for col in range(3)]
        tmp3 = []
        for k in range(0, 3):
            for n in range(0, 4):
                if q[1][n].empty() is False:
                    tmp_size = min(float(i - q[1][n].queue[0]), Z[1][n])
                else:
                    tmp_size = 0.0
                tmp[k] += schedule_of_sys[k][n] * tmp_size * channel[n]
        tmp_count = tmp.count(max(tmp))
        if tmp_count == 1:
            schedule[1] = tmp.index(max(tmp))
        elif tmp_count == 2:
            tmp1 = [0, 0]
            tmp1[0] = tmp.index(max(tmp))
            tmp[tmp.index(max(tmp))] = min(tmp)
            tmp1[1] = tmp.index(max(tmp))
            tmp3 = random.sample(tmp1, 1)
            schedule[1] = tmp3[0]
        else:
            tmp1 = [0, 1, 2]
            tmp3 = random.sample(tmp1, 1)
            schedule[1] = tmp3[0]
        schedule_count[1][schedule[1]] += 1
        # tmp = [0 for col in range(2)]
        # tmp3 = []
        # for n in range(0, 2):
        #     if q[1][n].empty() is False:
        #         tmp[n] = min(i - q[1][n].queue[0], Z[1][n]) * channel[1][n]
        #     else:
        #         tmp[n] = 0
        # if tmp[0] > tmp[1]:
        #     schedule[1] = 0
        # elif tmp[0] < tmp[1]:
        #     schedule[1] = 1
        # else:
        #     tmp1 = [0, 1]
        #     tmp3 = random.sample(tmp1, 1)
        #     schedule[1] = tmp3[0]

        # compute the schedule of DCUM
        tmp = [0 for col in range(3)]
        tmp3 = []
        temp_size = 0
        for k in range(0, 3):
            for n in range(0, 4):
                if q[2][n].empty() is False:
                    temp_size = 1  # min(float(i - q[2][n].queue[0]), Z[2][n])
                else:
                    temp_size = 1
                tmp[k] += schedule_of_sys[k][n] * \
                    channel[n] * temp_size * Z[2][n]
        tmp_count = tmp.count(max(tmp))
        if tmp_count == 1:
            schedule[2] = tmp.index(max(tmp))
        elif tmp_count == 2:
            tmp1 = [0, 0]
            tmp1[0] = tmp.index(max(tmp))
            tmp[tmp.index(max(tmp))] = min(tmp)
            tmp1[1] = tmp.index(max(tmp))
            tmp3 = random.sample(tmp1, 1)
            schedule[2] = tmp3[0]
        else:
            tmp1 = [0, 1, 2]
            tmp3 = random.sample(tmp1, 1)
            schedule[2] = tmp3[0]
        schedule_count[2][schedule[2]] += 1
        # tmp = [0 for col in range(2)]
        # tmp3 = []
        # for n in range(0, 2):
        #     tmp4 = Z[2][n]
        #     if q[2][n].empty() is True:
        #         tmp4 = 0
        #     tmp[n] = tmp4 * channel[2][n] * q[2][n].qsize()
        # if tmp[0] > tmp[1]:
        #     schedule[2] = 0
        # elif tmp[0] < tmp[1]:
        #     schedule[2] = 1
        # else:
        #     tmp1 = [0, 1]
        #     tmp3 = random.sample(tmp1, 1)
        #     schedule[2] = tmp3[0]
        for m in range(0, 3):
            for n in range(0, 4):
                if schedule[m] == n:
                    schedule_record[m][n] += 1
        # packet drop process of DUM
        for n in range(0, 4):
            if q[0][n].empty() is False:
                tmp = float(i - q[0][n].queue[0])
            else:
                tmp = 0.0
            drop_decision[n] = 0
            if Z[0][n] <= tmp and tmp > 0:
                drop_decision[n] = 1
        for n in range(0, 4):
            if drop_decision[n] == 1 and q[0][n].empty() is False:
                tmp = q[0][n].get()
                drop_count[n] += 1
                # if q[1][n].empty() is False and q[1].[n].full() is False:
                #     q[1][n].get()
                #     q[1][n].put(tmp)
                # elif q[1][n].empty() is True():
                #     print('q', 1, n, 'is empty')
                # else:
                #     print('q', 1, n, 'is full')
        # data transmission
        for m in range(0, 3):
            for n in range(0, 4):
                if schedule_of_sys[schedule[m]][n] == 1 and q[m][n].empty() is False and channel[n] == 1:
                    tmp = i - q[m][n].get()
                    tran_count[m][n] += 1
                    delay_every_step[m][n] += tmp
                    if m == 2:
                        delay_record_T[n][i] = tmp
                    if tmp > max_delay[m][n]:
                        max_delay[m][n] = tmp
        #  update the virtual queues
        # firstly, DUM
        # Virtual queue Z
        for n in range(0, 4):
            tmp = Z[0][n] - arrival_lambda[n] + \
                float(drop_decision[n]) + r_keep[0][n]
            if tmp > 0:
                Z[0][n] = tmp
            else:
                Z[0][n] = 0
        # H is not needed to be update

        # secondly, DUM non-drop
        for n in range(0, 4):
            tmp = Z[1][n] - arrival_lambda[n] + r_keep[1][n]
            if tmp > 0:
                Z[1][n] = tmp
            else:
                Z[1][n] = 0
        # then dva
        for n in range(0, 4):
            if schedule_of_sys[schedule[2]][n] == 1:
                mu = float(channel[n])
            else:
                mu = 0.0
            tmp = Z[2][n] - mu + r_keep[2][n]
            if tmp > 0:
                Z[2][n] = tmp
            else:
                Z[2][n] = 0
        # Data Arrival
        Arrival(i, j)

        # Collect the delay and throughput informantion
        if i % T == 0:
            delay_of_previous_T = [0 for col in range(4)]
            for n in range(0, 4):
                coun = [-2 for col in range(T)]
                for m in range(0, T):
                    ind = i - m
                    # print(delay_record_T[n][ind])
                    delay_of_previous_T[n] = delay_of_previous_T[
                        n] + delay_record_T[n][ind]
                    coun[m] = delay_record_T[n][ind]
                tmp1 = T - coun.count(-1)
                if tmp1 == 0:
                    D[n] = 0.0
                else:
                    tmp4 = delay_of_previous_T[n]
                    D[n] = float(tmp4) / float(tmp1)
            for n in range(0, 4):
                if D[n] > d[n] and theta[2][n] + epsilon[n] < 1.0:
                    theta[2][n] += epsilon[n]
                elif D[n] < d[n] and epsilon[n] - epsilon[n] / 1.5 >= 0.0:
                    epsilon[n] = epsilon[n] / 1.5
                    theta[2][n] -= epsilon[n]

    for m in range(0, 3):
        tmp1 = [0.0 for col in range(4)]
        for n in range(0, 4):
            if tran_count[m][n] != 0:
                tmp = float(delay_every_step[m][n] / tran_count[m][n])
                delay_record[m][n][j] = tmp
                max_delay_record[m][n][j] = max_delay[m][n]
                tmp1[n] = tmp / float(d[n])
            else:
                delay_record[m][n][j] = 0.0
                max_delay_record[m][n][j] = 0.0
                tmp1[n] = 0
            trans_record[m][n][j] = float(tran_count[m][n]) / float(count)
            tran_r[m][n][j] = tran_count[m][n]
            queue_size_record[m][n][j] = q[m][n].qsize()
            arrival[m][n][j] = arrival[m][n][j]
        if min(tmp1) > 0:
            index[m][j] = get_jain(tmp1[0], tmp1[1], tmp1[2], tmp1[3])
        else:
            index[m][j] = 0.0
    for n in range(0, 4):
        drop_record[n][j] = drop_count[n]
        # update theta, epsilon

    # clear process
    # print(arrival, tran_count)
    # print('schedule count', schedule_record)
    for m in range(0, 3):
        for n in range(0, 4):
            delay_every_step[m][n] = 0
            tran_count[m][n] = 0
            max_delay[m][n] = 0
            schedule_record[m][n] = 0

    for n in range(0, 4):
        drop_count[n] = 0
        for m in range(0, count):
            delay_record_T[n][m] = 0
    print(Z)

    Clear()
    # print(theta, 'theta')
    V = V + step
for m in range(0, 3):
    for n in range(0, 4):
        for k in range(0, loops):
            print('arr of', m, n, arrival[m][n][k], 'tran', tran_r[
                  m][n][k], 'qsize', queue_size_record[m][n][k])
            if m == 0:
                print('drop', drop_record[n][k])
                drops_record[k] += float(drop_record[n][k]) / float(count)
for m in range(0, 3):
    for k in range(0, loops):
        for n in range(0, 4):
            trans_alg[m][k] = trans_alg[m][k] + trans_record[m][n][k]


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
plt.plot(x, index[1], '--', label='DUM')
plt.plot(x, index[2], label='DCUM')
# plt.gca().set_yscale('log')
plt.legend(loc='center right')
fig.set_size_inches(width, height)
fig.savefig('Fairness.pdf')
plt.close(fig)
plt.figure(2)
plt.rc('font', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.xlabel('V')
plt.ylabel('Total Throughput')
# plt.plot(x, trans_alg[0], 's-', label='Trans, HOL-DUM')
# plt.plot(x, drops_record, 's-', label='Drop, HOL-DUM')
# plt.plot(x, trans_record[0][1], 'p-', label='flow 1, HOL-DUM')
# plt.plot(x, trans_record[1][0], 's-', label='flow 2, HOL-DUM')
# plt.plot(x, trans_record[1][1], 'p-', label='flow 3, HOL-DUM')
plt.plot(x, trans_alg[1], '--', label='Trans, DUM')
# plt.plot(x, trans_record[1][1], 'p-', label='flow 1, CL-DAMW-Ndrop')
plt.plot(x, trans_alg[2], label='Trans, DCUM')
# plt.plot(x, trans_record[2][1], 'p-', label='flow 1, DCUM')
plt.legend(loc='center right')
plt.figure(3)
plt.rc('font', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.xlabel('V')
plt.ylabel('Delay Performances')
y1 = np.linspace(0, V + 2, loops)
y3 = []
for i in range(0, len(x)):
    y3.append(x[i] + 2)
plt.ylim(0, 3500)
# plt.xlim(0, 2500)
plt.plot(x, y3, label='V + 2')
# plt.plot(x, delay_record[0][0], '*-', label='N 0')
# plt.plot(x, delay_record[0][1], '*-', label='N 1')
# plt.plot(x, delay_record[0][2], '*-', label='N 2')
# plt.plot(x, delay_record[0][3], '*-', label='N 3')
# plt.legend(loc='center right')
# plt.figure(4)
# plt.xlabel('V')
# plt.ylabel('Delay Performance of DUM_non-drop')
# plt.plot(x, y1, label='x + 2')
plt.plot(x, delay_record[1][0], 's-', label='DUM flow 0')
plt.plot(x, delay_record[1][1], 's-', label='DUM flow 1')
plt.plot(x, delay_record[1][2], 's-', label='DUM flow 2')
plt.plot(x, delay_record[1][3], 's-', label='DUM flow 3')
# plt.legend(loc='center right')
# plt.figure(5)
# plt.xlabel('V')
# plt.ylabel('Delay Performance of DCUM')
# plt.plot(x, y1, label='x + 2')
plt.plot(x, delay_record[2][0], '*-', label='DCUM flow 0')
plt.plot(x, delay_record[2][1], '*-', label='DCUM flow 1')
plt.plot(x, delay_record[2][2], '*-', label='DCUM flow 2')
plt.plot(x, delay_record[2][3], '*-', label='DCUM flow 3')
plt.legend(loc='upper right')
plt.show()
try:
    file = open('data.csv', 'w')
    fw = csv.writer(file)
except Exception:
    print("file open failed")
for i in range(0, loops):
    tmp_array = [index[1][i], index[2][i], trans_alg[1][i], trans_alg[2][i],
                 delay_record[1][0][i], delay_record[
                     1][1][i], delay_record[1][2][i],
                 delay_record[1][3][i], delay_record[
                     2][0][i], delay_record[2][1][i],
                 delay_record[2][2][i], delay_record[2][3][i]]
    for j in range(0, len(tmp_array)):
        print(tmp_array[j])
        # tmp_array[j].replace('\n', '')
        tmp_array[j] = float(tmp_array[j])
        # print(tmp_array[j])
    if(len(tmp_array) > 0):
        fw.writerow(tmp_array)
if file:
    file.close()
del q, Z, count, V, loops, maxvalue, max_last, r_keep, r, index
del channel, schedule, channel_lambda, drop_decision
del tran_count, drop_count, arrival_lambda, trans_record
gc.collect()

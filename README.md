# dcum
# author: Larry Lin from Harbin Institute of Techonoloy
This repository is the codes for the article "Towards Delay-Based Utility Maximization: Modeling and Implementation in SDWN Platform". 
We categorize these codes into six catalogs: "Codes run on the controller", "Cross_layer network states sampling modules", "Results analysis", "Simulation_codes", and "TCP information get". We introduce these codes individually.
Firstly, we should introduce our SDWN platform first.
![image](https://github.com/lingersohot/dcum/blob/master/Figures/framework.jpg)


*Data plane part*

We utilize the OpenFlow \cite{McKeown2008} protocol to convert commercial APs into virtual switches (data planes). The OpenFlow protocol needs two software tools: OpenWRT and Open vSwitch \cite{Openvswitch}. OpenWRT is an open-source project for the embedded operating system based on Linux. OpenWRT converts commercial APs into Linux devices. Open vSwitch running on OpenWRT can convert the APs into virtual switches and enable them to support the OpenFlow protocol. With the OpenFlow protocol, the SDWN can be created.
 Rate control, data sampling and load monitoring work on the data plane part and we introduce them in the following paragraphs.


*Rate control*

We focus on TCP traffic in this paper. For TCP, windows play an important role in rate control. There are three kinds of windows for TCP (except BBR \cite{Cardwell2016}): the congestion window (CWND), the send window, and receive window (advertised window in packets). The send window controls the data rate; it must be smaller than the congestion window and the receive window. Receive window can be modified on APs. So, if we can get the congestion window, we can modify the receive window to be a lower value which smaller than the congestion window to limit the data rate (send window must smaller than this modified value). Fortunately, authors of research work in \cite{Hagos2018} propose a machine learning method that can infer the congestion window on APs. We use this method in this paper to control data rates.
Table 1: Categories, sources and sample rates of sampled information

Module  | Location | Rate
----------|-----------|----------
Link  | Mac80211, kernel | 250 Hz 
Channel | Mac80211, kernel | 250 Hz
Queue | sch\_ generic.c, kernel | 250 Hz 
Beacon | Mac80211, kernel | 10 Hz 
Drops | Mac80211, codel.h, kernel | Each drop

*Data sampling*

We sample all the network metrics that may affect wireless data communications. These measurements are comprised of channel information, link information, beacon information, queue information, packet information, and dropped packet information. The locations where we implement sampling modules and the corresponding sampling rates are listed in Table \ref{tab:modules}. The precision of these measurements is high. The link, channel, and queue information is sampled every 4 ms. Beacon information varies slowly, so we sample it every 0.1 seconds. High precision samples cause a large amount of data that needs to be transmitted to the controller in real-time, so some redundancy reduction methods are used to remove the redundancies.

Table 2: Metrics Chosen for Learning

Symbol | Semantics 
---------|------------
congestion drop |Drop rate in queue process.  
noncongestion drop | Drop rate in Mac80211.  
time\_busy | The amount of time when channel is busy.  
time\_rx |  Time for receiving.  
time\_tx |  Time for transmitting.  
time\_scan| Time for scan channel.
noise |  Noise.  
packets\_3 / packet\_5 |  Packets received in the third / fifth queue.  
drops\_3 / drops\_5 |  Packet drops in the third / fifth queue.  
requeues\_3 / requeues\_5 |  Requeues in the third / fifth queue.  
backlog\_3 / backlog\_5 |  Backlog in the third / fifth queue.  
bytes\_3 / bytes\_5 |  Bytes received in the third / fifth queue.  
inactive\_time|  Inactive time of AP.    
expected\_throughput |  Expected throughput.  
sta\_count |  Amount of associated clients.  


*Custom messages and actions*
We implement the monitoring messages carry real-time sampled data to collectors and the controller; we extend the monitoring message in 5G-empower to do these works. We also implement a control message to transmit the generated decision trees to the APs and feedback the transmission results. The overheads of these messages are described in \textsection \ref{sec:trigger}. We also implement custom actions to process the control messages and maintain trees (create, insert, delete, update, search.).

*Logic plane part*

The logic plane is the ``brain'' of our platform. As shown in Fig. \ref{fig:framework}: association control, overload diagnosing, related factors exploration, real-time data receiving, and data preprocessing are working on it. We will introduce these functional modules in the following paragraphs.

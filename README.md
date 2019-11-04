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
Module  | Location | Rate
----------|-----------|----------
Link  | Mac80211, kernel | 250 Hz \\

Channel | Mac80211, kernel | 250 Hz\\

Queue | sch\_ generic.c, kernel | 250 Hz \\

Beacon | Mac80211, kernel | 10 Hz \\

Drops | Mac80211, codel.h, kernel | Each drop\\

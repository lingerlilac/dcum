# dcum
# author: Larry Lin from Harbin Institute of Techonoloy
This repository is the codes for the article "Towards Delay-Based Utility Maximization: Modeling and Implementation in SDWN Platform". 
We categorize these codes into six catalogs: "Codes run on the controller", "Cross_layer network states sampling modules", "Results analysis", "Simulation_codes", and "TCP information get". We introduce these codes individually.
Firstly, we should introduce our SDWN platform first.
\section{OVERVIEW OF TRIGGER-BASED DYNAMIC LOAD-BALANCING PLATFORM}
\label{sec:platform}
In this section, we introduce the design of our load balancing platform. The introductions describe how our platform monitors network loads and how it acts when network traffic should be redistributed.
\begin{table}
\caption{{Metrics used to model the AP load in previous researches}}
\setlength{\tabcolsep}{3pt}
\begin{tabular}{|l|l|}
\hline
{Metrics} & {Researches} \\
\hline
Data arriving rates  & \cite{Bejerano2010, Jabri2008, DeSchepper2017, Zeljkovic2018} \\
The amount of associated stations  &\cite{Bianchi2003, Bianchi2002} \\ 
 RSSI, the amount of associated stations & \cite{Papanikos2001, Collotta2012, Geier2017}\\
Signal strength, aggregated traffic rates &\cite{Gong2008}\\
Channel utilization& \cite{Coronado2018, Sawma2008, Krishan2015, Rangisetti2014}\\
Packet errors & \cite{Furtado2012, Jang2010, Baran2015}\\
Aggregated traffic rates, protocols & \cite{Gong2014}\\
\hline
\end{tabular}
\label{tab:set}
\end{table}%%%End of the table
\par We implement a load balancing platform in this paper, which is shown in Fig. \ref{fig:framework}. This platform consists of two parts, and it has six functions. The two parts are the data plane part and the logic plane part. The six functions are rate control, data sampling, load monitoring, association control, overload diagnosing, and related factors exploration. Rate control, data sampling, and load monitoring work on the data plane part, and the other three functions work on the logic plane part. Custom messages are used for data and messages transmission between the data plane and logic plane, and there are two kinds of custom messages: monitoring messages and control messages. We introduce these items in the following paragraphs. 
\Figure[t!](topskip=0pt, botskip=0pt, midskip=0pt)[width= \textwidth]{framework}
{Overview of our load balancing platform.\label{fig:framework}}

\subsection{Data plane part} 
We utilize the OpenFlow \cite{McKeown2008} protocol to convert commercial APs into virtual switches (data planes). The OpenFlow protocol needs two software tools: OpenWRT and Open vSwitch \cite{Openvswitch}. OpenWRT is an open-source project for the embedded operating system based on Linux. OpenWRT converts commercial APs into Linux devices. Open vSwitch running on OpenWRT can convert the APs into virtual switches and enable them to support the OpenFlow protocol. With the OpenFlow protocol, the SDWN can be created.
\par Rate control, data sampling and load monitoring work on the data plane part and we introduce them in the following paragraphs.
\paragraph{Rate control}
We focus on TCP traffic in this paper. For TCP, windows play an important role in rate control. There are three kinds of windows for TCP (except BBR \cite{Cardwell2016}): the congestion window (CWND), the send window, and receive window (advertised window in packets). The send window controls the data rate; it must be smaller than the congestion window and the receive window. Receive window can be modified on APs. So, if we can get the congestion window, we can modify the receive window to be a lower value which smaller than the congestion window to limit the data rate (send window must smaller than this modified value). Fortunately, authors of research work in \cite{Hagos2018} propose a machine learning method that can infer the congestion window on APs. We use this method in this paper to control data rates.


\begin{table}
\caption{Categories, sources and sample rates of sampled information}
\label{tab:modules}
\setlength{\tabcolsep}{3pt}
\begin{tabular}{|p{1.2cm}|p{4cm}|p{1.6cm}|}
\hline
{Module}  & {Location}& {Rate}\\
\hline
Link  & Mac80211, kernel & 250 Hz \\

Channel & Mac80211, kernel & 250 Hz\\

Queue & sch\_ generic.c, kernel & 250 Hz \\

Beacon & Mac80211, kernel & 10 Hz \\

Drops & Mac80211, codel.h, kernel & Each drop\\
\hline
\end{tabular}
\end{table}%%%End of the table
\paragraph{Data sampling} 
We sample all the network metrics that may affect wireless data communications. These measurements are comprised of channel information, link information, beacon information, queue information, packet information, and dropped packet information. The locations where we implement sampling modules and the corresponding sampling rates are listed in Table \ref{tab:modules}. The precision of these measurements is high. The link, channel, and queue information is sampled every 4 ms. Beacon information varies slowly, so we sample it every 0.1 seconds. High precision samples cause a large amount of data that needs to be transmitted to the controller in real-time, so some redundancy reduction methods are used to remove the redundancies.
\par Table \ref{tab:metrics} lists the sampled and computed network statistics. These metrics are statistics computed from real-time sampled data from APs.

\begin{table}
\caption{{Metrics Chosen for Learning}}
\begin{tabular}{|l|l|}
\hline
{Symbol} & { Semantics} \\
\hline
congestion drop &Drop rate in queue process. \\ 
noncongestion drop & Drop rate in Mac80211. \\ 
time\_busy & The amount of time when channel is busy. \\ 
time\_rx &  Time for receiving. \\ 
time\_tx &  Time for transmitting. \\ 
time\_scan& Time for scan channel.\\
noise &  Noise. \\ 
packets\_3 / packet\_5 &  Packets received in the third / fifth queue. \\ 
drops\_3 / drops\_5 &  Packet drops in the third / fifth queue. \\ 
requeues\_3 / requeues\_5 &  Requeues in the third / fifth queue. \\ 
backlog\_3 / backlog\_5 &  Backlog in the third / fifth queue. \\ 
bytes\_3 / bytes\_5 &  Bytes received in the third / fifth queue. \\ 
inactive\_time&  Inactive time of AP. \\   
expected\_throughput &  Expected throughput. \\ 
sta\_count &  Amount of associated clients. \\ 
\hline
\end{tabular}
\label{tab:metrics}
\end{table}%%%End of the table
Some details about these metrics are explained as follows:
\begin{enumerate}
\item Packets are mainly dropped by queue algorithms and the Mac80211 driver. Drops by the queue algorithms are called congestion drops, and those dropped by the Mac80211 are called noncongestion drops.
\item There are five queues for the OpenWRT-based APs, with almost no data in queues 1, 2, and 4. Data are mainly transmitted in queue 3, and some data are transmitted by queue 5 when a high arriving data rate happens.
\item Expected\_throughput are computed by Mac80211. 
\item There are four kinds of channel utilities in this paper: time\_busy, time\_rx, time\_tx, and time\_scan. time\_busy is a measure of how much time channel is in use during the last 1000 milliseconds. time\_rx is a measure of how much time the current AP is receiving data during the last 1000 milliseconds. time\_tx is a measure of how much time the current AP is transmitting data during the last 1000 milliseconds. time\_scan  is a measure of how much time current AP is scanning channels during the last 1000 milliseconds.
%\item Delay and jitter cannot be obtained directly on APs. Although some research has been focused on, their methods are protocol-dependent \cite{Jaiswal2004, Hagos2018}. There are no methods to infer delay or jitter of packets on APs.
\end{enumerate}
%\par It is hard to combine network metrics by a mathematical formulation. There are two main reasons for this: a) protocols are hard to formulate, and channel processes are complex. b) Various factors are naturally interdependent of each other. 


\paragraph{Load monitoring}
In a typical SDWN, a controller controls several wired connected APs, the wireless termination points are connected with these APs. The data transmission performance is important for SDWN, and re-associations are needed when the traffic is severely uneven. We implement the load monitoring module to characterize the AP's data transmission performance and trigger re-associations.  The details of the load monitoring module will be introduced in \textsection \ref{sec:trigger}.
\paragraph{Custom messages and actions}
We implement the monitoring messages carry real-time sampled data to collectors and the controller; we extend the monitoring message in 5G-empower to do these works. We also implement a control message to transmit the generated decision trees to the APs and feedback the transmission results. The overheads of these messages are described in \textsection \ref{sec:trigger}. We also implement custom actions to process the control messages and maintain trees (create, insert, delete, update, search.).
\subsection{Logic plane part}
\par The logic plane is the ``brain'' of our platform. As shown in Fig. \ref{fig:framework}: association control, overload diagnosing, related factors exploration, real-time data receiving, and data preprocessing are working on it. We will introduce these functional modules in the following paragraphs.
\paragraph{Data receiving and processing:} 
Typical SDWN will produce large amounts of data samples that should be processed and transmitted in real-time to other functions. It is challenging to guarantee time performance when the scale of the WLAN is big enough to cause abundant computational loads. There are several kinds of computations. For example, maintaining data to compute link statistics, packet statistics, channel statistics, packet statistics; merging these statistics to be useful data items, and preprocessing these data items. To guarantee time performance, we code all the data receiving modules with the C language, and apply numerous optimization methods in these modules.
\paragraph{Association control} 
Based on Algorithm \ref{alg:algfirest}, association control computes new associations for all the clients when the amount of overloaded APs exceeds a threshold. The details of association control will be described in \ref{sec:selection}.
\paragraph{Overload diagnosing}
This function is designed to diagnose the overload reasons, i.e., to find the patterns of network metrics when overloaded events happen. Additionally, decision trees that recognize network state on APs are the outputs of this function; the details will be introduced in \textsection \ref{sec:trigger}. 
\paragraph{Related factors exploration}
This function is designed to explore the relationships between AP load and metrics, and Table \ref{tab:metrics} lists the results. The metrics without effects (on load) will be removed from information sampling. The details will be introduced in \textsection \ref{sec:trigger}. 

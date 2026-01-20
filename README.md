# xApp for Throughput Prediction Kitoko David & Hassan Salifou Moubarak

## 

This README provides a concise overview of your successful deployment of an OAI 5G Core, FlexRIC, and RAN components on a Kubernetes infrastructure, including the execution of various xApps for network monitoring and slicing.

## Infrastructure Setup

### Disable swap for Kubernetes stability
sudo swapoff -a

### Initialize the Control Plane
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

### Configure local access
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

### Install Flannel CNI and allow pods on master node
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
kubectl taint nodes --all node-role.kubernetes.io/control-plane-

## 5G Network Components

Deployed via Ansible in the blueprint namespace, the stack includes:

    5G Core: AMF, SMF, UPF, UDM, UDR, AUSF, NRF, and MySQL.

    RAN: OAI-gNB (configured with E2 agent).

    UE: OAI-nr-ue.

    RIC: FlexRIC (O-RAN compliant Near-Real-Time RIC).

  
ansible-playbook -i inventories/UTH 5g.yaml --extra-vars "@params.oai-flexric.yaml"

# Verify the deployment
kubectl get pods -n blueprint -o wide
    
  Pod Name,IP,Function
  oai-flexric,10.244.0.28,Near-RT RIC
  oai-gnb,10.244.0.29,5G Base Station
  oai-nr-ue,10.244.0.30,User Equipment

  

## xApp Execution & Monitoring

All xApps were executed by accessing the oai-flexric container:
kubectl exec -it <oai-flexric-pod-name> -n blueprint -- /bin/bash

    xApp: xapp_kpm_moni

    Action: Subscribes to RAN Function ID 2 (ORAN-E2SM-KPM).

    root@oai-flexric-74df96bd4b-r9qsn:/flexric/build/examples/xApp/c/monitor# ./xapp_kpm_moni
[UTIL]: Setting the config -c file to /usr/local/etc/flexric/flexric.conf
[UTIL]: Setting path -p for the shared libraries to /usr/local/lib/flexric/
[xAapp]: Initializing ... 
[xApp]: nearRT-RIC IP Address = 10.244.0.28, PORT = 36422
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/librlc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libkpm_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libpdcp_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libgtp_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libmac_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libtc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/librc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libslice_sm.so 
[NEAR-RIC]: Loading SM ID = 143 with def = RLC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 2 with def = ORAN-E2SM-KPM 
[NEAR-RIC]: Loading SM ID = 144 with def = PDCP_STATS_V0 
[NEAR-RIC]: Loading SM ID = 148 with def = GTP_STATS_V0 
[NEAR-RIC]: Loading SM ID = 142 with def = MAC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 146 with def = TC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 3 with def = ORAN-E2SM-RC 
[NEAR-RIC]: Loading SM ID = 145 with def = SLICE_STATS_V0 
[xApp]: DB filename = /tmp/xapp_db_1768924036995958 
 [xApp]: E42 SETUP-REQUEST tx
[xApp]: E42 SETUP-RESPONSE rx 
[xApp]: xApp ID = 7 
[xApp]: Registered E2 Nodes = 1 
Connected E2 nodes = 1
[xApp]: registered node 0 ran func id = 2 
 [xApp]: registered node 1 ran func id = 3 
 [xApp]: registered node 2 ran func id = 142 
 [xApp]: registered node 3 ran func id = 143 
 [xApp]: registered node 4 ran func id = 144 
 [xApp]: registered node 5 ran func id = 145 
 [xApp]: registered node 6 ran func id = 146 
 [xApp]: registered node 7 ran func id = 148 
 [xApp]: reporting period = 1000 [ms]
[xApp]: Filter UEs by S-NSSAI criteria where SST = 1
[xApp]: Filter UEs by S-NSSAI criteria where SST = 1
[xApp]: E42 RIC SUBSCRIPTION REQUEST tx RAN_FUNC_ID 2 RIC_REQ_ID 1 
[xApp]: SUBSCRIPTION RESPONSE rx
[xApp]: Successfully subscribed to RAN_FUNC_ID 2 


    Result: Successfully captures KPM reports from the gNB.

RAN Slicing Control

    xApp: xapp_slice_moni_ctrl

    Functionality:

        Monitoring: Tracks Slice indication message latency (avg. ~400-1000 μs).

        Control: Dynamically adds/deletes slices via E2 Control Requests.

        root@oai-flexric-74df96bd4b-r9qsn:/flexric/build/examples/xApp/c/slice# ./xapp_slice_moni_ctrl 
[UTIL]: Setting the config -c file to /usr/local/etc/flexric/flexric.conf
[UTIL]: Setting path -p for the shared libraries to /usr/local/lib/flexric/
[xAapp]: Initializing ... 
[xApp]: nearRT-RIC IP Address = 10.244.0.28, PORT = 36422
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/librlc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libkpm_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libpdcp_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libgtp_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libmac_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libtc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/librc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libslice_sm.so 
[NEAR-RIC]: Loading SM ID = 143 with def = RLC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 2 with def = ORAN-E2SM-KPM 
[NEAR-RIC]: Loading SM ID = 144 with def = PDCP_STATS_V0 
[NEAR-RIC]: Loading SM ID = 148 with def = GTP_STATS_V0 
[NEAR-RIC]: Loading SM ID = 142 with def = MAC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 146 with def = TC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 3 with def = ORAN-E2SM-RC 
[NEAR-RIC]: Loading SM ID = 145 with def = SLICE_STATS_V0 
[xApp]: DB filename = /tmp/xapp_db_1768924912832921 
 [xApp]: E42 SETUP-REQUEST tx
[xApp]: E42 SETUP-RESPONSE rx 
[xApp]: xApp ID = 8 
[xApp]: Registered E2 Nodes = 1 
Connected E2 nodes len = 1
Registered ran func id = 2 
 Registered ran func id = 3 
 Registered ran func id = 142 
 Registered ran func id = 143 
 Registered ran func id = 144 
 Registered ran func id = 145 
 Registered ran func id = 146 
 Registered ran func id = 148 
 [xApp]: E42 RIC SUBSCRIPTION REQUEST tx RAN_FUNC_ID 145 RIC_REQ_ID 1 
[xApp]: SUBSCRIPTION RESPONSE rx
[xApp]: Successfully subscribed to RAN_FUNC_ID 145 
SLICE ind_msg latency = 3960 μs
SLICE ind_msg latency = 2005 μs
SLICE ind_msg latency = 567 μs
SLICE ind_msg latency = 567 μs
SLICE ind_msg latency = 458 μs
SLICE ind_msg latency = 1797 μs
SLICE ind_msg latency = 712 μs
SLICE ind_msg latency = 373 μs
SLICE ind_msg latency = 1252 μs

        Configuration: Static DL slices created (IDs 0, 2, 5) with specific Resource Block (RB) positions.

Multi-Layer Monitoring

    xApp: xapp_gtp_mac_rlc_pdcp_moni

    root@oai-flexric-74df96bd4b-r9qsn:/flexric/build/examples/xApp/c/monitor# ./xapp_gtp_mac_rlc_pdcp_moni 
[UTIL]: Setting the config -c file to /usr/local/etc/flexric/flexric.conf
[UTIL]: Setting path -p for the shared libraries to /usr/local/lib/flexric/
[xAapp]: Initializing ... 
[xApp]: nearRT-RIC IP Address = 10.244.0.28, PORT = 36422
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/librlc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libkpm_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libpdcp_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libgtp_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libmac_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libtc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/librc_sm.so 
[E2 AGENT]: Opening plugin from path = /usr/local/lib/flexric/libslice_sm.so 
[NEAR-RIC]: Loading SM ID = 143 with def = RLC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 2 with def = ORAN-E2SM-KPM 
[NEAR-RIC]: Loading SM ID = 144 with def = PDCP_STATS_V0 
[NEAR-RIC]: Loading SM ID = 148 with def = GTP_STATS_V0 
[NEAR-RIC]: Loading SM ID = 142 with def = MAC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 146 with def = TC_STATS_V0 
[NEAR-RIC]: Loading SM ID = 3 with def = ORAN-E2SM-RC 
[NEAR-RIC]: Loading SM ID = 145 with def = SLICE_STATS_V0 
[xApp]: DB filename = /tmp/xapp_db_1768925783668096 
 [xApp]: E42 SETUP-REQUEST tx
[xApp]: E42 SETUP-RESPONSE rx 
[xApp]: xApp ID = 9 
[xApp]: Registered E2 Nodes = 1 
Connected E2 nodes = 1
Registered node 0 ran func id = 2 
 Registered node 0 ran func id = 3 
 Registered node 0 ran func id = 142 
 Registered node 0 ran func id = 143 
 Registered node 0 ran func id = 144 
 Registered node 0 ran func id = 145 
 Registered node 0 ran func id = 146 
 Registered node 0 ran func id = 148 
 [xApp]: E42 RIC SUBSCRIPTION REQUEST tx RAN_FUNC_ID 142 RIC_REQ_ID 1 
[xApp]: SUBSCRIPTION RESPONSE rx
[xApp]: Successfully subscribed to RAN_FUNC_ID 142 
[xApp]: E42 RIC SUBSCRIPTION REQUEST tx RAN_FUNC_ID 143 RIC_REQ_ID 2 
[xApp]: SUBSCRIPTION RESPONSE rx
[xApp]: Successfully subscribed to RAN_FUNC_ID 143 
[xApp]: E42 RIC SUBSCRIPTION REQUEST tx RAN_FUNC_ID 144 RIC_REQ_ID 3 
[xApp]: SUBSCRIPTION RESPONSE rx
[xApp]: Successfully subscribed to RAN_FUNC_ID 144 
[xApp]: E42 RIC SUBSCRIPTION REQUEST tx RAN_FUNC_ID 148 RIC_REQ_ID 4 
[xApp]: SUBSCRIPTION RESPONSE rx
[xApp]: Successfully subscribed to RAN_FUNC_ID 148 
[xApp]: E42 RIC_SUBSCRIPTION_DELETE_REQUEST tx RAN_FUNC_ID 142 RIC_REQ_ID 1 
[xApp]: E42 SUBSCRIPTION DELETE RESPONSE rx
[xApp]: E42 RIC_SUBSCRIPTION_DELETE_REQUEST tx RAN_FUNC_ID 143 RIC_REQ_ID 2 
[xApp]: E42 SUBSCRIPTION DELETE RESPONSE rx
[xApp]: E42 RIC_SUBSCRIPTION_DELETE_REQUEST tx RAN_FUNC_ID 144 RIC_REQ_ID 3 
[xApp]: E42 SUBSCRIPTION DELETE RESPONSE rx
[xApp]: E42 RIC_SUBSCRIPTION_DELETE_REQUEST tx RAN_FUNC_ID 148 RIC_REQ_ID 4 
[xApp]: E42 SUBSCRIPTION DELETE RESPONSE rx
[xApp]: Sucessfully stopped 
Test xApp run SUCCESSFULLY


    Scope: Simultaneous subscription to MAC (142), RLC (143), PDCP (144), and GTP (148) service models for full-stack visibility.

# Summary Table of RAN Functions
SM ID	Name	Status
2	ORAN-E2SM-KPM	Operational
142	MAC_STATS_V0	Operational
143	RLC_STATS_V0	Operational
145	SLICE_STATS_V0	Operational

---

### Machine Learning Inference

The collected data (dataset.csv) is used to compare the performance of two prediction models for network throughput.
Running the Comparison Script

The script ml_inference.py evaluates the models based on the KPM dataset.
Bash

# Run the ML comparison
python3 ml_inference.py

Comparison: ARIMA vs. LSTM
Model	Type	Usage	Inference Timing
ARIMA	Statistical	Classic time-series forecasting	Fast, but less adaptable to non-linear bursts.
LSTM	Deep Learning	Recurrent Neural Network (RNN)	Optimized for complex 5G traffic patterns.

Key Link: The dataset.csv file acts as the bridge between the Network Layer (FlexRIC KPM xAppverything has been set up correctly, all the following pods should be deployed:
```bash
kubectl get pods -n blueprint
NAME                              READY   STATUS    RESTARTS   AGE
oai-amf-6486c9d49c-snnt5          1/1     Running   0          45m
oai-ausf-84ffb6bc7c-vjzdj         1/1     Running   0          45m
oai-core-mysql-7f7b695b8b-s4l66   1/1     Running   0          45m
oai-flexric-5db68d7bf6-n28q8      1/1     Running   0          44m
oai-gnb-c5b4659c6-vghc7           1/1     Running   0          44m
oai-nr-ue-7dbdb954fc-4rbn4        1/1     Running   0          44m
oai-nrf-7dbb6d4b9-s9l2v           1/1     Running   0          45m
oai-smf-5d654698cf-7wpnh          1/1     Running   0          45m
oai-udm-7c49dc8f66-wsrtf          1/1     Running   0          45m
oai-udr-5d85996695-zg5g4          1/1     Running   0          45m
oai-upf-86dc5998c8-spzxz          1/1     Running   0          45mMachine Learning Inference

The collected data (dataset.csv) is used to compare the performance of two prediction models for network throughput.
Running the Comparison Script

The script ml_inference.py evaluates the models based on the KPM dataset.

# Run the ML comparison
python3 ml_inference.py

Comparison: ARIMA vs. LSTM
Model	Type	Usage	Inference Timing
ARIMA	Statistical	Classic time-series forecasting	Fast, but less adaptable to non-linear bursts.
LSTM	Deep Learning	Recurrent Neural Network (RNN)	Optimized for complex 5G traffic patterns.



# xApp for Throughput Prediction

## Contact

For help and information regarding this project, please contact: Dimitrios.Kefalas@lip6.fr

## Overview

In this project, you will deploy a fully operational 5G network using OpenAirInterface (OAI) and Kubernetes. The network functions will be containerized and orchestrated within a Kubernetes-based microservices environment, ensuring flexibility and scalability.

The main objective is to utilize the Key Performance Measurement (KPM) service model within FlexRIC to collect real-time Downlink (DL) throughput data from the Radio Access Network (RAN). You will develop and deploy an xApp that processes this data, extracts predictive features, and integrates a machine learning-based model to forecast future DL throughput based on historical patterns, enabling proactive network optimization.

---

## Objective
- Deploy a 5G Network: Set up a fully operational 5G network using OpenAirInterface (OAI) and Kubernetes, with the network functions running as containerized microservices.

- Utilize the KPM Service Model: Leverage the Key Performance Measurement (KPM) service model in FlexRIC to collect real-time Downlink (DL) throughput data from the Radio Access Network (RAN).

- Develop an xApp: Create and deploy an xApp capable of processing the provided DL throughput data and extracting predictive features.

- Integrate Machine Learning: Implement a machine learning-based time-series model (e.g., LSTM, ARIMA) to forecast future DL throughput based on historical patterns.

- Utilize Provided Dataset: Work exclusively with the provided dataset.csv for training and testing the machine learning model, ensuring consistent and standardized evaluation.

---

## Tools & Software
- Kubernetes
- OpenAirInterface5G CN and RAN
- FlexRIC (cloud-based)

---
This repo uses a subpart of this implementation, please refer in case you need more details:
```bash
https://gitlab.noc.onelab.eu/onelab/slices-5g-blueprint/-/blob/main/5G_deployment_revised.md
```
---

## Getting Started

### Step 1: Clone the Repository
Clone the repository to your VMs.
```bash
git clone https://gitlab.noc.onelab.eu/dkefalas/xapp-for-throughput-prediction.git
```
---

### Step 2: Verify Your Kubernetes Environment
Check if you already have a healthy Kubernetes environment:

- If your Kubernetes setup is functional, proceed to the Ansible installation section.
- If you do not have a healthy Kubernetes environment, move to the next step.

---

### Step 3: Setting Up Kubernetes
Navigate to the `kubernetes-setup` folder in the repository.

This folder contains Ansible playbooks for:
- Uninstalling any existing Kubernetes setup.
- Installing a fresh Kubernetes environment.
- Setting up a cluster, including:
  - The control plane node.
  - Worker nodes that will join the cluster.

Follow the instructions in the `kubernetes-setup` folder to set up your Kubernetes environment.

---

### Step 4: Proceed to Ansible Installation
Once your Kubernetes environment is set up, you can proceed with the installation using the provided Ansible playbooks.

Begin by updating the inventories/UTH/hosts.yml file with the correct IPs and node names corresponding to your VMs.

Next, modify the inventories/UTH/group_vars/all file to include the appropriate ansible_user value.

After completing these steps, you can proceed with deploying the scenario by executing the following command:
```bash
ansible-playbook -i inventories/UTH 5g.yaml --extra-vars "@params.oai-flexric.yaml"
```
If everything has been set up correctly, all the following pods should be deployed:
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
oai-upf-86dc5998c8-spzxz          1/1     Running   0          45m
```




At this point, you should be able to ping from your UE to the 5GCN. To do this, execute a command to ping the 5GCN from your UE. 
```bash
kubectl exec -ti oai-nr-ue-7dbdb954fc-4rbn4 -n blueprint -- ping 12.1.1.1
```


**Note**: The pod name in the command above is an example and will likely differ in your setup. Use `kubectl get pods` to find the correct pod name.

---

## Deploying a Monitoring xApp

The next step is to create and deploy a monitoring xApp. To deploy your xApp, run the following commands on the deployment host (master):
```bash
kubectl exec -ti oai-flexric-5db68d7bf6-n28q8 bash -n blueprint
```

This will connect you to the RIC environment, where you can choose the programming language for your xApp (C or Python3):

- For **C language**: Navigate to `/flexric/build/examples/xApp/c`
- For **Python3**: Navigate to `/flexric/build/examples/xApp/python3`

**Example**: To run an xApp that monitors KPM metrics for the RAN, use the following command:

```bash
./xapp_kpm_moni
```

## Configuration Files and Directories

You can view or edit configuration files for the Core, RAN, FlexRIC, and UE in the following directories:

- **Core Files**:  
  `roles/flexric/files/blueprint/oai-flexric/core_files`

- **Core Configurations**:  
  `roles/flexric/files/blueprint/oai-flexric/core_values`

- **RAN Files**:  
  `roles/flexric/files/blueprint/oai-flexric/ran_files`

- **RAN Configurations**:  
  `roles/flexric/files/blueprint/oai-flexric/ran_values`

- **FlexRIC Files**:  
  `roles/flexric/files/blueprint/oai-flexric/flexric_files`

- **FlexRIC Configurations**:  
  `roles/flexric/files/blueprint/oai-flexric/flexric_values`

- **UE Files**:  
  `roles/flexric/files/blueprint/oai-flexric/ue_files`

- **UE Configurations**:  
  `roles/flexric/files/blueprint/oai-flexric/ue_values`

---

## Uninstalling the Previous Deployment

To uninstall the previous deployment (OAI Core, RF Simulator, FlexRIC, and UE), run the following Ansible playbook:

```bash
ansible-playbook -i inventories/UTH destroy-oai-flexric.yaml
```

This playbook will cleanly remove all components of the blueprint deployment.

---

## Project Goals
The primary goal of this project is to develop and deploy an xApp within a 5G network environment that leverages the Key Performance Measurement (KPM) service model in FlexRIC to collect and analyze real-time Downlink (DL) throughput data from the Radio Access Network (RAN). The main objective is to evaluate and compare the inference time performance of multiple time-series machine learning predictors, such as LSTM, ARIMA, and other forecasting models, when applied to real-time DL throughput data.

You can use the file named dataset.csv for both training and testing purposes. The dataset should be split into two subsets: one for training the machine learning models and another for testing their performance. A common approach is to allocate 70–80% of the data for training and 20–30% for testing, ensuring that the models are trained effectively while reserving sufficient data for evaluation.

To test the system, you can deploy a script to generate traffic from the UPF to the UE using the iperf command. The xApp can then direct its output to a Python script, where each pre-trained time-series model (e.g., LSTM, ARIMA, etc.) will be executed to measure its inference time and predictive efficiency under real network conditions.

This project uses:
- Kubernetes for orchestration.
- OpenAirInterface5G for Core Network (CN) and Radio Access Network (RAN).
- FlexRIC for RIC-based monitoring and control.


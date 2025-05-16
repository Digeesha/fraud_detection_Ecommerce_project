# 🛡️ E-commerce Fraud Detection using Machine Learning and Blockchain

This project implements a hybrid fraud detection system that combines **machine learning** and **blockchain technology** to identify and securely log potentially fraudulent transactions in an e-commerce environment. The goal is to prevent financial loss, ensure transparency, and build customer trust by using AI for prediction and blockchain for immutable transaction records.

---

## 🎯 Project Objective

To develop an intelligent fraud detection system that uses historical transaction data to train a machine learning model capable of identifying fraud and integrates a smart contract on the Ethereum blockchain to securely log and verify high-risk transactions.

---
## 📊 Dataset Description

The dataset used in this project is publicly available on Kaggle:

📎 **Source:** [Credit Card Fraud Detection Dataset – Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

It contains 284,807 anonymized transactions made by European credit card holders in September 2013, with 492 labeled as fraud (Class = 1).

| Feature              | Description                                  |
|----------------------|----------------------------------------------|
| `V1` to `V28`        | Principal components obtained using PCA      |
| `Amount`             | Transaction amount                           |
| `Time`               | Seconds elapsed between transactions         |
| `Class`              | Target variable (1 = Fraud, 0 = Legitimate)  |

> ⚠️ You can download the dataset from Kaggle and place `creditcard.csv` inside the `dataset/` folder of this project.


The dataset consists of labeled e-commerce transaction records with the following features:

| Feature              | Description                                  |
|----------------------|----------------------------------------------|
| `transaction_amount` | Total cost of the transaction                |
| `product_category`   | Type/category of the product                 |
| `customer_age`       | Age of the customer                          |
| `account_age_days`   | Age of the customer’s account                |
| `payment_method`     | Type of payment used (card, wallet, etc.)    |
| `quantity`           | Number of items purchased                    |
| `device_used`        | Device used for the transaction              |
| `transaction_hour`   | Hour of the day the transaction was made     |
| `is_fraud`           | Target variable (1 = Fraud, 0 = Legitimate)  |

> ⚠️ Due to privacy or size constraints, the dataset is not included in the repository. You can place your `.csv` file inside the `dataset/` folder.

---

## 🧠 Machine Learning Model

A **feed-forward neural network** built with TensorFlow/Keras:

- **Input Layer:** Based on selected features
- **Hidden Layers:**  
  - Dense(64) → ReLU  
  - Dropout(0.3)  
  - Dense(32) → ReLU  
- **Output Layer:** Dense(1) → Sigmoid

---

## ⚙️ Training Details

- **Loss Function:** Binary Crossentropy  
- **Optimizer:** Adam  
- **Metrics:** Accuracy, AUC (ROC)  
- **Imbalance Handling:** Class weights  
- **Epochs:** 20 (EarlyStopping used)  
- **Train/Test Split:** 80/20

---

## 📈 Model Performance

- **Training Accuracy:** ~93.8%  
- **Validation Accuracy:** ~94.1%  
- **AUC-ROC Score:** ~0.94

---

## 📊 Output Visualizations

### 📌 Accuracy Over Epochs


### 📌 ROC Curve


---

## 🔗 Blockchain Integration

To ensure tamper-proof logging of high-risk transactions, a **smart contract** was developed and deployed locally using:

- 🧠 **Smart Contract:** Written in Solidity
- ⚙️ **Ganache:** Used as the local Ethereum blockchain
- 🦊 **MetaMask:** Used for wallet interaction and transaction signing

High-risk (predicted fraudulent) transactions are hashed and recorded on the blockchain for transparency and immutability.

### Example Use Case:
- Transaction flagged as fraud → transaction hash sent to smart contract → permanently recorded on chain.

Smart contract handles:
- Storing transaction hashes
- Retrieving records for audit purposes

---


## 🗂️ Project Structure
![metamask](https://github.com/user-attachments/assets/b39bde8b-1a69-4726-8263-092d42575487)


---

## 🚀 How to Run the Project

### 1. 📦 Install Dependencies
```bash
pip install -r requirements.txt
from train import train_model
import pandas as pd

df = pd.read_csv("dataset/your_file.csv")
train_model(df, 'is_fraud')
cd backend
python app.py

4. (Optional) 🖥 Use Frontend
Use a simple React app or HTML form to send requests to http://localhost:5000/predict.


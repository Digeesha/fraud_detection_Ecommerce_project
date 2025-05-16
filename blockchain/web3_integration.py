from web3 import Web3
import pickle
import pandas as pd
import json

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if web3.is_connected():
    print("✅ Connected to Ganache Blockchain")
else:
    print("❌ Failed to connect to Ganache Blockchain")

# Load the ABI
with open('./build/contracts/FraudDetection.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']

# Paste your deployed contract address here
contract_address = "0x82F552788797e9608995bef0Ec587B650bc49cAa"

# Connect to the deployed contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Load AI Model
with open('../ai_model/fraud_model.pkl', 'rb') as file:
    model = pickle.load(file)


# Align the sample data with training features
with open('../ai_model/feature_columns.pkl', 'rb') as file:
    feature_columns = pickle.load(file)

# Load the actual dataset
data = pd.read_csv(r'D:/FrudEcommerce/ai_model/dataset.csv', encoding='latin1')

# Prepare the data for prediction (excluding non-numeric columns)
X = data.drop(['Fraud', 'Company Name'], axis=1, errors='ignore')
X = pd.get_dummies(X)
X = X.reindex(columns=feature_columns, fill_value=0)

# Counter for fraudulent transactions
fraud_count = 0

# Loop through and log each transaction
for i, row in X.iterrows():
    sample_data = pd.DataFrame([row], columns=feature_columns)
    is_fraud = model.predict(sample_data)[0]

    # Increment fraud counter if fraud detected
    if is_fraud == 1:
        fraud_count += 1

    # Log the transaction to blockchain
    tx_hash = contract.functions.logTransaction(i + 1, 500, int(is_fraud)).transact({
        'from': web3.eth.accounts[0]
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Transaction {i + 1} logged with Fraud Status: {is_fraud}")

# Display the total number of fraud transactions
print(f"\n🚨 Total Fraudulent Transactions Detected: {fraud_count}")

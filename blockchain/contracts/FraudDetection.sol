// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FraudDetection {
    
    struct Transaction {
        uint256 id;
        uint256 amount;
        uint256 fraudScore;
        bool isFraud;
        uint256 timestamp;
    }

    mapping(uint256 => Transaction) public transactions;
    uint256 public fraudThreshold = 70; // Fraud score above 70 is considered fraudulent.

    event FraudDetected(uint256 indexed transactionId, uint256 fraudScore);
    event TransactionLogged(uint256 indexed transactionId, uint256 amount, bool isFraud);

    // Function to log a transaction with AI-detected fraud score
    function logTransaction(uint256 _id, uint256 _amount, uint256 _fraudScore) public {
        bool isFraud = _fraudScore >= fraudThreshold;
        
        transactions[_id] = Transaction({
            id: _id,
            amount: _amount,
            fraudScore: _fraudScore,
            isFraud: isFraud,
            timestamp: block.timestamp
        });

        if (isFraud) {
            emit FraudDetected(_id, _fraudScore);
        }

        emit TransactionLogged(_id, _amount, isFraud);
    }

    // Function to check if a transaction is fraudulent
    function checkTransaction(uint256 _id) public view returns (bool) {
        return transactions[_id].isFraud;
    }

    // Update the fraud detection threshold
    function updateThreshold(uint256 _newThreshold) public {
        fraudThreshold = _newThreshold;
    }
}

import React, { useState } from "react";
import axios from "axios";
import "./ManualCheckForm.css";
import { logPrediction } from "./blockchain/contract";

function ManualCheckForm() {
  const [input, setInput] = useState({
    transaction_amount: "",
    product_category: "",
    customer_age: "",
    account_age_days: "",
    payment_method: "",
    quantity: "",
    device_used: "",
    transaction_hour: "",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };

  const handlePredict = async () => {
    const values = Object.values(input).map((val) =>
      isNaN(val) ? val : Number(val)
    );

    try {
      const res = await axios.post("http://localhost:5000/predict", {
        input: values,
      });

      console.log("✅ Prediction result from Flask:", res.data);
      setResult(res.data);

      if (res.data?.prediction && res.data?.probability !== undefined) {
        const fraudScore = Math.round(Number(res.data.probability) * 100);
        const id = Math.floor(Math.random() * 1000000); // basic transaction ID
        const amount = Number(input.transaction_amount);

        try {
          await logPrediction(id, amount, fraudScore);
          console.log("✅ Logged to blockchain:", id);
        } catch (err) {
          console.error("❌ Blockchain error:", err);
          alert("Blockchain logging failed.");
        }
      }
    } catch (err) {
      console.error("❌ Prediction API failed:", err);
      alert("Prediction or blockchain logging failed.");
    }
  };

  return (
    <div className="form-container">
      <h2>E-Commerce Fraud Detection</h2>
      <div className="form-grid">
        <div>
          <label>Transaction Amount:</label>
          <input type="number" name="transaction_amount" onChange={handleChange} />
        </div>
        <div>
          <label>Payment Method:</label>
          <select name="payment_method" onChange={handleChange}>
            <option value="">Select</option>
            <option>Credit Card</option>
            <option>Bank Transfer</option>
            <option>Paypal</option>
          </select>
        </div>
        <div>
          <label>Product Category:</label>
          <select name="product_category" onChange={handleChange}>
            <option value="">Select</option>
            <option>Clothing</option>
            <option>Electronics</option>
            <option>Groceries</option>
          </select>
        </div>
        <div>
          <label>Quantity:</label>
          <input type="number" name="quantity" onChange={handleChange} />
        </div>
        <div>
          <label>Customer Age:</label>
          <input type="number" name="customer_age" onChange={handleChange} />
        </div>
        <div>
          <label>Device Used:</label>
          <select name="device_used" onChange={handleChange}>
            <option value="">Select</option>
            <option>Mobile</option>
            <option>Desktop</option>
            <option>Tablet</option>
          </select>
        </div>
        <div>
          <label>Account Age Days:</label>
          <input type="number" name="account_age_days" onChange={handleChange} />
        </div>
        <div>
          <label>Transaction Hour:</label>
          <input type="number" name="transaction_hour" onChange={handleChange} />
        </div>
      </div>

      <button className="predict-btn" onClick={handlePredict}>
        Predict
      </button>

      {result && result.prediction && (
        <div className="result-box">
          <p><strong>Prediction:</strong> {result.prediction}</p>
          {typeof result.probability !== "undefined" && (
            <p><strong>Probability:</strong> {(Number(result.probability) * 100).toFixed(2)}%</p>
          )}
        </div>
      )}
    </div>
  );
}

export default ManualCheckForm;

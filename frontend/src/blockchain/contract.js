import Web3 from "web3";
import FraudDetection from "./FraudDetection.json";

const web3 = new Web3(window.ethereum);
const contractAddress = "0xD6ca66AdF4535FaC90D8Cf62ABc7f4485375c76e"; // your deployed contract
const contract = new web3.eth.Contract(FraudDetection.abi, contractAddress);

export async function logPrediction(id, amount, fraudScore) {
  try {
    await window.ethereum.request({ method: "eth_requestAccounts" });
    const accounts = await web3.eth.getAccounts();

    console.log("🧾 Using account:", accounts[0]);

    await contract.methods
      .logTransaction(id, amount, fraudScore)
      .send({ from: accounts[0], gas: 300000 });

    console.log("✔️ Logged to blockchain.");
  } catch (error) {
    console.error("❌ Blockchain error:", error);
  }
}

import React, { useState, useEffect } from "react";
import axios from "axios";
import "./UploadForm.css";
import { useNavigate } from "react-router-dom";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [filePath, setFilePath] = useState("");
  const [loading, setLoading] = useState(false);
  const [polling, setPolling] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return alert("Please select a file.");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:5000/upload", formData);
      setFilePath(res.data.file_path);
      alert("✅ File uploaded. Starting training...");
      await handleTrain(res.data.file_path);
    } catch (err) {
      console.error(err);
      alert("❌ Upload failed.");
    }
  };

  const handleTrain = async (path) => {
    try {
      setLoading(true);
      await axios.post("http://localhost:5000/train", {
        file_path: path,
      });
      // ⏳ Add a short delay before polling starts
      setTimeout(() => setPolling(true), 1000); // 1s delay
    } catch (err) {
      console.error(err);
      alert("❌ Training request failed.");
      setLoading(false);
    }
  };

  useEffect(() => {
    let interval;
    if (polling) {
      interval = setInterval(async () => {
        try {
          const res = await axios.get("http://localhost:5000/status");
          if (!res.data.training) {
            clearInterval(interval);
            setPolling(false);
            setLoading(false);
            alert("✅ Training completed!");
            navigate("/predict");
          }
        } catch (err) {
          console.error("❌ Polling error:", err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [polling, navigate]);

  return (
    <div className="upload-container">
      <h2>📤 Upload CSV & Train Model</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading || polling}>
        {loading || polling ? "Training..." : "Upload & Train"}
      </button>
      {(loading || polling) && (
        <p style={{ marginTop: "10px", color: "orange", fontWeight: "bold" }}>
          ⏳ Training model... Please wait.
        </p>
      )}
    </div>
  );
}

export default UploadForm;

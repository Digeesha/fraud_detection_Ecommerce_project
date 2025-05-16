import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import DashboardHeader from "./DashboardHeader";
import UploadForm from "./UploadForm";
import ManualCheckForm from "./ManualCheckForm";

function App() {
  return (
    <div>
      <DashboardHeader />
      <div style={{ padding: "20px" }}>
        <Routes>
          <Route path="/" element={<Navigate to="/upload" />} />
          <Route path="/upload" element={<UploadForm />} />
          <Route path="/predict" element={<ManualCheckForm />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;

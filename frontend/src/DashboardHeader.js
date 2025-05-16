import React from "react";
import { NavLink } from "react-router-dom";
import "./DashboardHeader.css";

function DashboardHeader() {
  return (
    <header className="dashboard-header">
      <div className="logo">E-Commerce Fraud Detection</div>
      <nav className="nav-links">
        <NavLink to="/" className={({ isActive }) => isActive ? "active" : ""}>
          Home
        </NavLink>
        <NavLink to="/upload" className={({ isActive }) => isActive ? "active" : ""}>
          Upload
        </NavLink>
        <NavLink to="/predict" className={({ isActive }) => isActive ? "active" : ""}>
          Prediction
        </NavLink>
      </nav>
    </header>
  );
}

export default DashboardHeader;

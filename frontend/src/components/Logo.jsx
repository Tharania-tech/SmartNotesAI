import React from "react";
import "./Logo.css";
export default function Logo({ size = "small", showName = true }) {
  return (
    <div className="brand-logo">

      <img
        src="/smartnotes-icon.png"
        alt="SmartNotes AI"
        className="smartnotes-icon"
      />

      {showName && (
        <div className="brand-text">

          <span className="brand-name">
            SmartNotes
          </span>

          <span className="brand-ai">
            AI
          </span>

        </div>
      )}

    </div>
  );
}
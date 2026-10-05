import React from "react";

const Footer = () => {
  return (
    <footer className="app-footer">
      <div className="app-footer-inner">

        <div className="app-footer-brand">
          <div className="app-footer-logo">
            SN
          </div>

          <div>
            <h3>SmartNotes AI</h3>
            <p>
              Learn smarter. Revise faster. Remember longer.
            </p>
          </div>
        </div>

        <div className="app-footer-links">
          <span>Smart Learning</span>
          <span>AI Notes</span>
          <span>Progress Tracking</span>
          <span>Quiz & Revision</span>
        </div>

      </div>

      <div className="app-footer-bottom">
        <span>
          © {new Date().getFullYear()} SmartNotes AI. All rights reserved.
        </span>

        <span>
          Built for smarter learning
        </span>
      </div>
    </footer>
  );
};

export default Footer;
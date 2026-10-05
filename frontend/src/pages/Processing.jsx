import React, { useEffect } from "react";
import { CheckCircle, LoaderCircle, FileText } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";

export default function Processing() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const noteId = location.state && location.state.noteId;

    if (!noteId) {
      navigate("/upload");
      return;
    }

    const timer = setTimeout(function () {
      navigate("/notes/" + noteId);
    }, 4000);

    return function () {
      clearTimeout(timer);
    };
  }, [navigate, location]);

  return (
    <div className="processing-page">
      <div className="processing-card">

        <div className="processing-icon">
          <FileText size={36} />
        </div>

        <h1>Analyzing Your Notes</h1>

        <p className="processing-subtitle">
          SmartNotes AI is processing your document...
        </p>

        <div className="processing-loader">
          <LoaderCircle size={42} className="spin" />
        </div>

        <div className="processing-steps">

          <div className="processing-step completed">
            <CheckCircle size={20} />
            <span>Document uploaded</span>
          </div>

          <div className="processing-step active">
            <LoaderCircle size={20} className="spin" />
            <span>Extracting and analyzing content</span>
          </div>

          <div className="processing-step">
            <span className="step-number">3</span>
            <span>Generating learning content</span>
          </div>

        </div>

        <div className="processing-progress">
          <div className="processing-progress-bar"></div>
        </div>

        <p className="processing-message">
          Please wait while we prepare your personalized study materials.
        </p>

      </div>
    </div>
  );
}
import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  UploadCloud,
  FileText,
  X,
  Sparkles,
  FileCheck2,
  Brain,
  BookOpen,
  ArrowRight,
  Loader2,
  CheckCircle2,
  Zap
} from "lucide-react";

import AppHeader from "../components/AppHeader";

import { uploadNote } from "../services/notesApi";

export default function UploadNotes() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [title, setTitle] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");

  const validateFile = (file) => {
    if (!file) {
      return false;
    }

    const fileName = file.name.toLowerCase();

    return (
      fileName.endsWith(".pdf") ||
      fileName.endsWith(".docx")
    );
  };

  const selectFile = (file) => {
    setError("");

    if (!file) {
      return;
    }

    if (!validateFile(file)) {
      setSelectedFile(null);
      setError("Please select a PDF or DOCX file.");
      return;
    }

    setSelectedFile(file);

    if (!title.trim()) {
      const generatedTitle = file.name.replace(
        /\.(pdf|docx)$/i,
        ""
      );

      setTitle(generatedTitle);
    }
  };

  const handleFileChange = (event) => {
    const files = event.target.files;

    if (files && files.length > 0) {
      selectFile(files[0]);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();

    setDragActive(false);

    const files = event.dataTransfer.files;

    if (files && files.length > 0) {
      selectFile(files[0]);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    setProgress(0);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const openPicker = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleUpload = async () => {
    setError("");

    if (!selectedFile) {
      setError("Please select your study material.");
      return;
    }

    if (!title.trim()) {
      setError("Please enter a title for your notes.");
      return;
    }

    try {
      setUploading(true);
      setProgress(15);

      const response = await uploadNote(
        selectedFile,
        title.trim()
      );

      setProgress(70);

      const data =
        response && response.data
          ? response.data
          : response;

      const noteId =
        data && data.note_id
          ? data.note_id
          : data && data.noteId
            ? data.noteId
            : data && data.id
              ? data.id
              : data && data._id
                ? data._id
                : "";

      if (!noteId) {
        throw new Error(
          "The note was uploaded, but no note ID was returned."
        );
      }

      setProgress(100);

      setTimeout(() => {
        navigate("/processing", {
          state: {
            noteId: noteId,
            title: title.trim()
          }
        });
      }, 500);

    } catch (err) {
      console.error("Upload error:", err);

      setError(
        err && err.message
          ? err.message
          : "Unable to upload your notes."
      );

      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <div className="upload-page">

      <AppHeader />

      <main className="upload-main">

        <div className="upload-bg-orb upload-bg-orb-one"></div>

        <div className="upload-bg-orb upload-bg-orb-two"></div>

        <section className="upload-hero">

          <div className="upload-badge">
            <Sparkles size={15} />
            AI-Powered Learning
          </div>

          <h1>
            Turn your notes into
            <span> smarter learning</span>
          </h1>

          <p>
            Upload your study material and let SmartNotes AI
            transform it into useful learning resources.
          </p>

        </section>

        <section className="upload-layout">

          {/* LEFT SIDE */}

          <div className="upload-card">

            <div className="upload-card-header">

              <div>
                <h2>
                  Upload your notes
                </h2>

                <p>
                  PDF and DOCX files are supported
                </p>
              </div>

              <div className="upload-header-icon">
                <UploadCloud size={23} />
              </div>

            </div>

            {!selectedFile ? (

              <div
                className={
                  "upload-dropzone " +
                  (
                    dragActive
                      ? "upload-dropzone-active"
                      : ""
                  )
                }
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={openPicker}
              >

                <div className="upload-cloud-icon">
                  <UploadCloud size={34} />
                </div>

                <h3>
                  Drop your study material here
                </h3>

                <p>
                  or{" "}
                  <span>
                    browse from your computer
                  </span>
                </p>

                <div className="upload-format-row">

                  <div className="upload-format-chip">
                    <FileText size={14} />
                    PDF
                  </div>

                  <div className="upload-format-chip">
                    <FileText size={14} />
                    DOCX
                  </div>

                </div>

                <small>
                  Choose the notes you want SmartNotes AI to analyze
                </small>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.docx"
                  hidden
                  onChange={handleFileChange}
                />

              </div>

            ) : (

              <div className="selected-file-box">

                <div className="selected-file-left">

                  <div className="selected-file-icon">
                    <FileCheck2 size={23} />
                  </div>

                  <div className="selected-file-info">

                    <h3>
                      {selectedFile.name}
                    </h3>

                    <p>
                      {(
                        selectedFile.size /
                        (1024 * 1024)
                      ).toFixed(2)}{" "}
                      MB
                    </p>

                  </div>

                </div>

                <button
                  type="button"
                  className="remove-file-button"
                  onClick={removeFile}
                  disabled={uploading}
                >
                  <X size={17} />
                </button>

              </div>

            )}

            <div className="upload-field">

              <label>
                Note title
              </label>

              <input
                type="text"
                value={title}
                onChange={(event) => {
                  setTitle(event.target.value);
                }}
                placeholder="Example: Operating Systems Unit 3"
                disabled={uploading}
              />

            </div>

            {error && (
              <div className="upload-error">
                {error}
              </div>
            )}

            {uploading && (

              <div className="upload-progress-container">

                <div className="upload-progress-heading">

                  <span>
                    Preparing your learning material
                  </span>

                  <strong>
                    {progress}%
                  </strong>

                </div>

                <div className="upload-progress-track">

                  <div
                    className="upload-progress-bar"
                    style={{
                      width: progress + "%"
                    }}
                  ></div>

                </div>

              </div>

            )}

            <button
              type="button"
              className="upload-submit-button"
              onClick={handleUpload}
              disabled={uploading}
            >

              {uploading ? (

                <>
                  <Loader2
                    size={18}
                    className="upload-spin"
                  />

                  Analyzing...
                </>

              ) : (

                <>
                  <Sparkles size={18} />

                  Upload & Analyze

                  <ArrowRight size={18} />
                </>

              )}

            </button>

            <div className="upload-trust-row">

              <div>
                <CheckCircle2 size={15} />
                Easy to use
              </div>

              <div>
                <Zap size={15} />
                AI-powered
              </div>

              <div>
                <FileCheck2 size={15} />
                PDF / DOCX
              </div>

            </div>

          </div>

          {/* RIGHT SIDE */}

          <aside className="upload-info-card">

            <div className="upload-info-title">

              <div className="upload-info-icon">
                <Brain size={20} />
              </div>

              <div>

                <h2>
                  Your learning journey
                </h2>

                <p>
                  SmartNotes AI takes care of the hard work.
                </p>

              </div>

            </div>

            <div className="upload-steps">

              <div className="upload-step">

                <div className="upload-step-number">
                  01
                </div>

                <div>

                  <h3>
                    Upload
                  </h3>

                  <p>
                    Add your lecture notes,
                    textbook material or study PDF.
                  </p>

                </div>

              </div>

              <div className="upload-step">

                <div className="upload-step-number">
                  02
                </div>

                <div>

                  <h3>
                    Analyze
                  </h3>

                  <p>
                    SmartNotes AI identifies
                    important information in your notes.
                  </p>

                </div>

              </div>

              <div className="upload-step">

                <div className="upload-step-number">
                  03
                </div>

                <div>

                  <h3>
                    Learn
                  </h3>

                  <p>
                    Get summaries, concepts,
                    flashcards and quizzes.
                  </p>

                </div>

              </div>

            </div>

            <div className="upload-feature-box">

              <div className="upload-feature">
                <BookOpen size={17} />
                <span>Smart Summary</span>
              </div>

              <div className="upload-feature">
                <Brain size={17} />
                <span>Key Concepts</span>
              </div>

              <div className="upload-feature">
                <FileText size={17} />
                <span>Flashcards</span>
              </div>

              <div className="upload-feature">
                <Sparkles size={17} />
                <span>AI Quiz</span>
              </div>

            </div>

          </aside>

        </section>

        <p className="upload-footer-text">
          SmartNotes AI · Study Smarter, Recall Faster
        </p>

      </main>
      <Footer />
    </div>
  );
}
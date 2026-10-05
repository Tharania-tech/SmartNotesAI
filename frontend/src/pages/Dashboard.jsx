import React, { useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  Brain,
  BookOpen,
  CheckCircle2,
  Clock3,
  FileText,
  Flame,
  Lightbulb,
  MessageCircle,
  Plus,
  Sparkles,
  Target,
  Trash2,
  TrendingUp,
  UploadCloud,
  Layers3,
  GraduationCap,
  BarChart3,
  CalendarDays,
  Zap,
  ChevronRight
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import AppHeader from "../components/AppHeader";
import { getNotes, deleteNote } from "../services/notesApi";

import "../index.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getNotes();

      let noteList = [];

      if (Array.isArray(response)) {
        noteList = response;
      } else if (response && Array.isArray(response.notes)) {
        noteList = response.notes;
      } else if (response && Array.isArray(response.data)) {
        noteList = response.data;
      }

      setNotes(noteList);
    } catch (err) {
      console.error("Dashboard notes error:", err);
      setError("Unable to load your notes.");
      setNotes([]);
    } finally {
      setLoading(false);
    }
  };

  const getNoteId = (note) => {
    if (!note) {
      return "";
    }

    if (note._id) {
      return String(note._id);
    }

    if (note.id) {
      return String(note.id);
    }

    if (note.note_id) {
      return String(note.note_id);
    }

    return "";
  };

  const getNoteTitle = (note) => {
    if (!note) {
      return "Untitled Notes";
    }

    if (note.title) {
      return String(note.title);
    }

    if (note.file_name) {
      return String(note.file_name);
    }

    if (note.filename) {
      return String(note.filename);
    }

    return "Untitled Notes";
  };

  const getNoteDate = (note) => {
    if (!note) {
      return "Recently added";
    }

    if (note.created_at) {
      return formatDate(note.created_at);
    }

    if (note.uploaded_at) {
      return formatDate(note.uploaded_at);
    }

    return "Recently added";
  };

  const formatDate = (dateValue) => {
    try {
      const date = new Date(dateValue);

      if (Number.isNaN(date.getTime())) {
        return "Recently added";
      }

      return date.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric"
      });
    } catch (err) {
      return "Recently added";
    }
  };

  const handleOpenNote = (note) => {
    const noteId = getNoteId(note);

    if (!noteId) {
      return;
    }

    navigate("/notes/" + noteId);
  };

  const handleDelete = async (note) => {
    const noteId = getNoteId(note);

    if (!noteId) {
      return;
    }

    const confirmed = window.confirm(
      "Are you sure you want to delete this note?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeletingId(noteId);

      await deleteNote(noteId);

      setNotes((currentNotes) => {
        return currentNotes.filter((item) => {
          return getNoteId(item) !== noteId;
        });
      });
    } catch (err) {
      console.error("Delete note error:", err);
      alert("Unable to delete this note.");
    } finally {
      setDeletingId("");
    }
  };

  const latestNote = useMemo(() => {
    if (!notes || notes.length === 0) {
      return null;
    }

    return notes[0];
  }, [notes]);

  const notesCount = notes.length;

  const learningToolsCount = 5;

  const progressValue = notesCount > 0 ? 72 : 0;

  return (
    <div className="dashboard-page">
      <AppHeader />

      <main className="dashboard-main">

        {/* ==================================================
            HERO
           ================================================== */}

        <section className="dashboard-hero">

          <div className="dashboard-hero-left">

            <div className="dashboard-eyebrow">
              <span className="dashboard-eyebrow-dot"></span>
              AI Learning Workspace
            </div>

            <h1 className="dashboard-hero-title">
              Learn from your notes.
              <span> Smarter, faster, better.</span>
            </h1>

            <p className="dashboard-hero-description">
              Transform your study material into summaries, key concepts,
              flashcards and adaptive quizzes — all in one intelligent
              learning workspace.
            </p>

            <div className="dashboard-hero-actions">

              <button
                type="button"
                className="dashboard-primary-button"
                onClick={() => navigate("/upload")}
              >
                <UploadCloud size={19} />
                Upload New Notes
                <ArrowRight size={18} />
              </button>

              <button
                type="button"
                className="dashboard-secondary-button"
                onClick={() => {
                  if (latestNote) {
                    handleOpenNote(latestNote);
                  } else {
                    navigate("/upload");
                  }
                }}
              >
                Continue Learning
                <ArrowRight size={18} />
              </button>

            </div>

            <div className="dashboard-trust-row">

              <div className="dashboard-trust-item">
                <CheckCircle2 size={17} />
                <span>PDF & DOCX supported</span>
              </div>

              <div className="dashboard-trust-item">
                <Brain size={17} />
                <span>AI-powered learning</span>
              </div>

              <div className="dashboard-trust-item">
                <Zap size={17} />
                <span>Personalized revision</span>
              </div>

            </div>

          </div>

          <div className="dashboard-hero-right">

            <div className="dashboard-hero-orbit orbit-one"></div>
            <div className="dashboard-hero-orbit orbit-two"></div>

            <div className="dashboard-ai-floating-card">

              <div className="dashboard-ai-card-top">
                <div className="dashboard-ai-icon">
                  <Sparkles size={20} />
                </div>

                <div>
                  <div className="dashboard-ai-label">
                    SmartNotes AI
                  </div>

                  <div className="dashboard-ai-subtitle">
                    Learning engine active
                  </div>
                </div>

                <div className="dashboard-live-pill">
                  <span></span>
                  Live
                </div>
              </div>

              <div className="dashboard-ai-score-row">

                <div className="dashboard-ai-score">
                  <strong>84</strong>
                  <span>Learning Score</span>
                </div>

                <div className="dashboard-ai-mini-bars">
                  <span style={{ height: "34%" }}></span>
                  <span style={{ height: "53%" }}></span>
                  <span style={{ height: "45%" }}></span>
                  <span style={{ height: "72%" }}></span>
                  <span style={{ height: "62%" }}></span>
                  <span style={{ height: "88%" }}></span>
                  <span style={{ height: "78%" }}></span>
                </div>

              </div>

              <div className="dashboard-ai-insight">
                <Lightbulb size={17} />
                <span>
                  Your recent study pattern shows strong concept retention.
                </span>
              </div>

            </div>

          </div>

        </section>


        {/* ==================================================
            OVERVIEW STATS
           ================================================== */}

        <section className="dashboard-stats-grid">

          <div className="dashboard-stat-card">
            <div className="dashboard-stat-icon teal">
              <FileText size={19} />
            </div>

            <div>
              <span className="dashboard-stat-label">
                Notes uploaded
              </span>

              <strong className="dashboard-stat-value">
                {notesCount}
              </strong>

              <span className="dashboard-stat-caption">
                Your study library
              </span>
            </div>
          </div>


          <div className="dashboard-stat-card">
            <div className="dashboard-stat-icon blue">
              <Layers3 size={19} />
            </div>

            <div>
              <span className="dashboard-stat-label">
                AI learning tools
              </span>

              <strong className="dashboard-stat-value">
                {learningToolsCount}
              </strong>

              <span className="dashboard-stat-caption">
                Available for every note
              </span>
            </div>
          </div>


          <div className="dashboard-stat-card">
            <div className="dashboard-stat-icon violet">
              <Target size={19} />
            </div>

            <div>
              <span className="dashboard-stat-label">
                Learning score
              </span>

              <strong className="dashboard-stat-value">
                84%
              </strong>

              <span className="dashboard-stat-caption positive">
                +8% this week
              </span>
            </div>
          </div>


          <div className="dashboard-stat-card">
            <div className="dashboard-stat-icon orange">
              <Flame size={19} />
            </div>

            <div>
              <span className="dashboard-stat-label">
                Study streak
              </span>

              <strong className="dashboard-stat-value">
                7 days
              </strong>

              <span className="dashboard-stat-caption">
                Keep the momentum
              </span>
            </div>
          </div>

        </section>


        {/* ==================================================
            ADVANCED LEARNING INTELLIGENCE
           ================================================== */}

        <section className="dashboard-intelligence-section">

          <div className="dashboard-section-heading">

            <div>
              <span className="dashboard-section-kicker">
                AI INSIGHTS
              </span>

              <h2>
                Learning intelligence
              </h2>

              <p>
                Understand how your study behaviour is progressing.
              </p>
            </div>

            <button
              type="button"
              className="dashboard-section-link"
              onClick={() => navigate("/profile")}
            >
              View profile
              <ChevronRight size={16} />
            </button>

          </div>


          <div className="dashboard-intelligence-grid">

            {/* ==================================================
                LEARNING INTELLIGENCE
               ================================================== */}

            <div className="dashboard-intelligence-card">

              <div className="dashboard-intelligence-header">

                <div className="dashboard-intelligence-heading">

                  <div className="dashboard-intelligence-logo">
                    <Sparkles size={18} />
                  </div>

                  <div>
                    <h3>Learning Intelligence</h3>
                    <span>AI-powered study overview</span>
                  </div>

                </div>

                <button
                  type="button"
                  className="dashboard-more-button"
                  onClick={() => navigate("/profile")}
                >
                  <BarChart3 size={17} />
                </button>

              </div>


              <div className="dashboard-intelligence-main">

                <div className="dashboard-progress-ring">
                  <div className="dashboard-progress-ring-inner">
                    <strong>84%</strong>
                    <span>Overall</span>
                  </div>
                </div>

                <div className="dashboard-intelligence-copy">

                  <div className="dashboard-intelligence-status">
                    <span></span>
                    Learning pace is healthy
                  </div>

                  <h4>
                    You are building consistent learning momentum.
                  </h4>

                  <p>
                    Your study activity suggests that you are improving
                    concept understanding and revision consistency.
                  </p>

                </div>

              </div>


              <div className="dashboard-intelligence-metrics">

                <div className="dashboard-intelligence-metric">
                  <span>Concept retention</span>
                  <strong>88%</strong>

                  <div className="metric-progress">
                    <span style={{ width: "88%" }}></span>
                  </div>
                </div>

                <div className="dashboard-intelligence-metric">
                  <span>Revision consistency</span>
                  <strong>79%</strong>

                  <div className="metric-progress">
                    <span style={{ width: "79%" }}></span>
                  </div>
                </div>

                <div className="dashboard-intelligence-metric">
                  <span>Quiz readiness</span>
                  <strong>74%</strong>

                  <div className="metric-progress">
                    <span style={{ width: "74%" }}></span>
                  </div>
                </div>

              </div>

            </div>


            {/* ==================================================
                STUDY ANALYTICS
               ================================================== */}

            <div className="dashboard-study-analytics-card">

              <div className="dashboard-analytics-header">

                <div>
                  <span className="dashboard-analytics-kicker">
                    STUDY ANALYTICS
                  </span>

                  <h3>Study performance</h3>

                  <p>
                    Your recent learning activity
                  </p>
                </div>

                <div className="dashboard-analytics-icon">
                  <TrendingUp size={18} />
                </div>

              </div>


              <div className="dashboard-analytics-score">

                <div>
                  <span>Weekly focus score</span>

                  <strong>84</strong>

                  <small>
                    <TrendingUp size={13} />
                    12% improvement
                  </small>
                </div>

                <div className="dashboard-analytics-circle">
                  <div className="dashboard-analytics-circle-inner">
                    <strong>84</strong>
                    <span>Focus</span>
                  </div>
                </div>

              </div>


              <div className="dashboard-analytics-chart">

                <div className="analytics-chart-header">
                  <span>Study activity</span>
                  <span>Mon — Sun</span>
                </div>

                <div className="analytics-bars">

                  <div className="analytics-bar-group">
                    <span className="analytics-bar" style={{ height: "34%" }}></span>
                    <small>M</small>
                  </div>

                  <div className="analytics-bar-group">
                    <span className="analytics-bar" style={{ height: "48%" }}></span>
                    <small>T</small>
                  </div>

                  <div className="analytics-bar-group">
                    <span className="analytics-bar" style={{ height: "42%" }}></span>
                    <small>W</small>
                  </div>

                  <div className="analytics-bar-group">
                    <span className="analytics-bar" style={{ height: "68%" }}></span>
                    <small>T</small>
                  </div>

                  <div className="analytics-bar-group">
                    <span className="analytics-bar" style={{ height: "55%" }}></span>
                    <small>F</small>
                  </div>

                  <div className="analytics-bar-group">
                    <span className="analytics-bar" style={{ height: "82%" }}></span>
                    <small>S</small>
                  </div>

                  <div className="analytics-bar-group active">
                    <span className="analytics-bar" style={{ height: "94%" }}></span>
                    <small>S</small>
                  </div>

                </div>

              </div>


              <div className="dashboard-analytics-footer">

                <div>
                  <Clock3 size={15} />
                  <span>8h 42m studied</span>
                </div>

                <div>
                  <Target size={15} />
                  <span>12 goals completed</span>
                </div>

              </div>

            </div>

          </div>

        </section>


        {/* ==================================================
            CONTINUE LEARNING
           ================================================== */}

        <section className="dashboard-focus-section">

          <div className="dashboard-section-heading">

            <div>
              <span className="dashboard-section-kicker">
                CONTINUE LEARNING
              </span>

              <h2>Pick up where you left off</h2>

              <p>
                Jump back into your most recent study material.
              </p>
            </div>

          </div>


          <div className="dashboard-focus-card">

            <div className="dashboard-focus-left">

              <div className="dashboard-focus-file-icon">
                <BookOpen size={23} />
              </div>

              <div className="dashboard-focus-info">

                <span className="dashboard-focus-label">
                  MOST RECENT NOTE
                </span>

                <h3>
                  {latestNote
                    ? getNoteTitle(latestNote)
                    : "Upload your first study note"}
                </h3>

                <div className="dashboard-focus-meta">

                  <span>
                    <CalendarDays size={14} />
                    {latestNote
                      ? getNoteDate(latestNote)
                      : "Ready to begin"}
                  </span>

                  <span>
                    <GraduationCap size={14} />
                    Personalized learning
                  </span>

                </div>

              </div>

            </div>


            <div className="dashboard-focus-right">

              <div className="dashboard-focus-progress">

                <div className="dashboard-focus-progress-top">
                  <span>Learning progress</span>
                  <strong>{progressValue}%</strong>
                </div>

                <div className="dashboard-focus-progress-track">
                  <span
                    style={{
                      width: progressValue + "%"
                    }}
                  ></span>
                </div>

              </div>

              <button
                type="button"
                className="dashboard-focus-button"
                onClick={() => {
                  if (latestNote) {
                    handleOpenNote(latestNote);
                  } else {
                    navigate("/upload");
                  }
                }}
              >
                {latestNote ? "Continue" : "Upload Note"}
                <ArrowRight size={17} />
              </button>

            </div>

          </div>

        </section>


        {/* ==================================================
            AI LEARNING SUITE
           ================================================== */}

        <section className="dashboard-tools-section">

          <div className="dashboard-section-heading">

            <div>
              <span className="dashboard-section-kicker">
                AI LEARNING SUITE
              </span>

              <h2>Everything you need to study smarter</h2>

              <p>
                Turn one note into a complete learning experience.
              </p>
            </div>

          </div>


          <div className="dashboard-tools-grid">

            <button
              type="button"
              className="dashboard-tool-card teal"
              onClick={() => {
                if (latestNote) {
                  navigate(
                    "/notes/" + getNoteId(latestNote) + "/summary"
                  );
                } else {
                  navigate("/upload");
                }
              }}
            >
              <div className="dashboard-tool-top">
                <div className="dashboard-tool-icon">
                  <Sparkles size={20} />
                </div>

                <ArrowRight size={17} />
              </div>

              <h3>Smart Summary</h3>

              <p>
                Condense long notes into clear and easy-to-revise summaries.
              </p>
            </button>


            <button
              type="button"
              className="dashboard-tool-card blue"
              onClick={() => {
                if (latestNote) {
                  navigate(
                    "/notes/" + getNoteId(latestNote) + "/concepts"
                  );
                } else {
                  navigate("/upload");
                }
              }}
            >
              <div className="dashboard-tool-top">
                <div className="dashboard-tool-icon">
                  <Brain size={20} />
                </div>

                <ArrowRight size={17} />
              </div>

              <h3>Key Concepts</h3>

              <p>
                Discover important topics, keywords and connections.
              </p>
            </button>


            <button
              type="button"
              className="dashboard-tool-card violet"
              onClick={() => {
                if (latestNote) {
                  navigate(
                    "/notes/" + getNoteId(latestNote) + "/flashcards"
                  );
                } else {
                  navigate("/upload");
                }
              }}
            >
              <div className="dashboard-tool-top">
                <div className="dashboard-tool-icon">
                  <Layers3 size={20} />
                </div>

                <ArrowRight size={17} />
              </div>

              <h3>Flashcards</h3>

              <p>
                Practice active recall with interactive study cards.
              </p>
            </button>


            <button
              type="button"
              className="dashboard-tool-card orange"
              onClick={() => {
                if (latestNote) {
                  navigate(
                    "/notes/" + getNoteId(latestNote) + "/quiz"
                  );
                } else {
                  navigate("/upload");
                }
              }}
            >
              <div className="dashboard-tool-top">
                <div className="dashboard-tool-icon">
                  <Target size={20} />
                </div>

                <ArrowRight size={17} />
              </div>

              <h3>AI Quiz</h3>

              <p>
                Test your understanding with adaptive AI-generated questions.
              </p>
            </button>


            <button
              type="button"
              className="dashboard-tool-card indigo"
              onClick={() => {
                if (latestNote) {
                  navigate(
                    "/notes/" + getNoteId(latestNote) + "/chat"
                  );
                } else {
                  navigate("/upload");
                }
              }}
            >
              <div className="dashboard-tool-top">
                <div className="dashboard-tool-icon">
                  <MessageCircle size={20} />
                </div>

                <ArrowRight size={17} />
              </div>

              <h3>AI Tutor</h3>

              <p>
                Ask questions and understand difficult concepts instantly.
              </p>
            </button>


            <button
              type="button"
              className="dashboard-tool-card add"
              onClick={() => navigate("/upload")}
            >
              <div className="dashboard-tool-top">
                <div className="dashboard-tool-icon">
                  <Plus size={20} />
                </div>

                <ArrowRight size={17} />
              </div>

              <h3>Add New Notes</h3>

              <p>
                Upload another subject and build your learning library.
              </p>
            </button>

          </div>

        </section>


        {/* ==================================================
            RECENT NOTES
           ================================================== */}

        <section className="dashboard-notes-section">

          <div className="dashboard-section-heading">

            <div>
              <span className="dashboard-section-kicker">
                STUDY LIBRARY
              </span>

              <h2>Recent notes</h2>

              <p>
                Your latest learning material in one place.
              </p>
            </div>

            <button
              type="button"
              className="dashboard-section-link"
              onClick={() => navigate("/upload")}
            >
              Add notes
              <Plus size={16} />
            </button>

          </div>


          {loading ? (

            <div className="dashboard-empty-state">
              <div className="dashboard-loading-spinner"></div>

              <h3>Loading your notes...</h3>

              <p>
                Preparing your learning workspace.
              </p>
            </div>

          ) : error ? (

            <div className="dashboard-empty-state">
              <div className="dashboard-empty-icon">
                <FileText size={24} />
              </div>

              <h3>{error}</h3>

              <button
                type="button"
                className="dashboard-empty-button"
                onClick={loadNotes}
              >
                Try Again
              </button>
            </div>

          ) : notes.length === 0 ? (

            <div className="dashboard-empty-state">

              <div className="dashboard-empty-icon">
                <UploadCloud size={25} />
              </div>

              <h3>Your learning library is waiting.</h3>

              <p>
                Upload your first note and let SmartNotes AI
                turn it into a complete learning experience.
              </p>

              <button
                type="button"
                className="dashboard-primary-button small"
                onClick={() => navigate("/upload")}
              >
                <UploadCloud size={17} />
                Upload Notes
                <ArrowRight size={16} />
              </button>

            </div>

          ) : (

            <div className="dashboard-notes-grid">

              {notes.slice(0, 6).map((note) => {

                const noteId = getNoteId(note);
                const title = getNoteTitle(note);
                const date = getNoteDate(note);

                return (
                  <article
                    key={noteId || title}
                    className="dashboard-note-card"
                  >

                    <div className="dashboard-note-card-top">

                      <div className="dashboard-note-icon">
                        <FileText size={18} />
                      </div>

                      <button
                        type="button"
                        className="dashboard-delete-button"
                        onClick={() => handleDelete(note)}
                        disabled={deletingId === noteId}
                        aria-label="Delete note"
                      >
                        <Trash2 size={15} />
                      </button>

                    </div>


                    <div className="dashboard-note-content">

                      <span className="dashboard-note-type">
                        STUDY NOTE
                      </span>

                      <h3 title={title}>
                        {title}
                      </h3>

                      <p>
                        Uploaded {date}
                      </p>

                    </div>


                    <button
                      type="button"
                      className="dashboard-note-open"
                      onClick={() => handleOpenNote(note)}
                    >
                      Open note
                      <ArrowRight size={15} />
                    </button>

                  </article>
                );

              })}

            </div>

          )}

        </section>


        {/* ==================================================
            WORKFLOW
           ================================================== */}

        <section className="dashboard-workflow-section">

          <div className="dashboard-workflow-heading">

            <span className="dashboard-section-kicker">
              HOW SMARTNOTES WORKS
            </span>

            <h2>
              From uploaded notes to confident learning.
            </h2>

          </div>


          <div className="dashboard-workflow-grid">

            <div className="dashboard-workflow-step">

              <div className="dashboard-workflow-number">
                01
              </div>

              <div className="dashboard-workflow-icon">
                <UploadCloud size={19} />
              </div>

              <h3>Upload</h3>

              <p>
                Add your lecture notes, textbooks or study documents.
              </p>

            </div>


            <div className="dashboard-workflow-line"></div>


            <div className="dashboard-workflow-step">

              <div className="dashboard-workflow-number">
                02
              </div>

              <div className="dashboard-workflow-icon">
                <Brain size={19} />
              </div>

              <h3>Understand</h3>

              <p>
                AI extracts summaries, concepts and useful learning points.
              </p>

            </div>


            <div className="dashboard-workflow-line"></div>


            <div className="dashboard-workflow-step">

              <div className="dashboard-workflow-number">
                03
              </div>

              <div className="dashboard-workflow-icon">
                <Layers3 size={19} />
              </div>

              <h3>Practice</h3>

              <p>
                Use flashcards, quizzes and interactive revision tools.
              </p>

            </div>


            <div className="dashboard-workflow-line"></div>


            <div className="dashboard-workflow-step">

              <div className="dashboard-workflow-number">
                04
              </div>

              <div className="dashboard-workflow-icon">
                <GraduationCap size={19} />
              </div>

              <h3>Improve</h3>

              <p>
                Identify weak areas and make every study session smarter.
              </p>

            </div>

          </div>

        </section>

      </main>


      <footer className="dashboard-footer">

        <div className="dashboard-footer-inner">

          <div className="dashboard-footer-brand">
            <Sparkles size={17} />
            <span>SmartNotes AI</span>
          </div>

          <span>
            Study Smarter, Recall Faster
          </span>

        </div>

      </footer>

    </div>
  );
}
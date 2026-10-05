import React, { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";

import "./index.css";
import Logo from "./components/Logo";
import "./home.css";
import smartNotesLogo from "./assets/logo.png";

// Pages
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import UploadNotes from "./pages/Upload";
import Processing from "./pages/Processing";
import NoteAnalysis from "./pages/NoteAnalysis";
import Summary from "./pages/Summary";
import KeyConcepts from "./pages/KeyConcepts";
import Flashcards from "./pages/Flashcards";
import Quiz from "./pages/Quiz";
import QuizResult from "./pages/QuizResult";
import Chat from "./pages/Chat";
import Profile from "./pages/Profile";
import MyNotes from "./pages/MyNotes";
import Progress from "./pages/Progress";
import WeakTopics from "./pages/WeakTopics";
import LearningQuest from "./pages/LearningQuest";

/* =========================================================
   ICON COMPONENT
   ========================================================= */

function Icon({ name, size = 20, stroke = 1.8 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: stroke,
    strokeLinecap: "round",
    strokeLinejoin: "round",
  };

  switch (name) {
    case "arrow":
      return (
        <svg {...common}>
          <path d="M5 12h14" />
          <path d="m13 6 6 6-6 6" />
        </svg>
      );

    case "book":
      return (
        <svg {...common}>
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z" />
        </svg>
      );

    case "file":
      return (
        <svg {...common}>
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z" />
          <path d="M14 2v6h6" />
          <path d="M8 13h8" />
          <path d="M8 17h6" />
        </svg>
      );

    case "spark":
      return (
        <svg {...common}>
          <path d="m12 3-1.2 4.8L6 9l4.8 1.2L12 15l1.2-4.8L18 9l-4.8-1.2Z" />
          <path d="m19 14-.7 2.3L16 17l2.3.7L19 20l.7-2.3L22 17l-2.3-.7Z" />
        </svg>
      );

    case "card":
      return (
        <svg {...common}>
          <rect x="3" y="4" width="18" height="16" rx="3" />
          <path d="M8 9h8" />
          <path d="M8 13h5" />
        </svg>
      );

    case "quiz":
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="9" />
          <path d="M9.8 9a2.4 2.4 0 1 1 4.1 1.7c-.9.8-1.9 1.2-1.9 2.8" />
          <path d="M12 17h.01" />
        </svg>
      );

    case "chat":
      return (
        <svg {...common}>
          <path d="M20 11.5a7.5 7.5 0 0 1-8 7.5 8.5 8.5 0 0 1-3.2-.6L4 20l1.5-4A7.3 7.3 0 0 1 4.5 12 7.5 7.5 0 0 1 12 4.5a7.5 7.5 0 0 1 8 7Z" />
        </svg>
      );

    case "chart":
      return (
        <svg {...common}>
          <path d="M4 19V5" />
          <path d="M4 19h16" />
          <path d="m7 15 3-4 3 2 5-6" />
        </svg>
      );

    case "upload":
      return (
        <svg {...common}>
          <path d="M12 16V4" />
          <path d="m7 9 5-5 5 5" />
          <path d="M5 20h14" />
        </svg>
      );

    case "check":
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="9" />
          <path d="m8 12 2.5 2.5L16 9" />
        </svg>
      );

    case "target":
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="8" />
          <circle cx="12" cy="12" r="4" />
          <circle cx="12" cy="12" r="1" />
        </svg>
      );

    case "users":
      return (
        <svg {...common}>
          <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
          <circle cx="9" cy="7" r="4" />
          <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
          <path d="M16 3.13a4 4 0 0 1 0 7.75" />
        </svg>
      );

    default:
      return null;
  }
}

/* =========================================================
   HOME PAGE
   ========================================================= */


function ProtectedRoute({ children }) {
  const token = localStorage.getItem("smartnotes-token");
  return token ? children : <Navigate to="/login" replace />;
}

function Home() {
  const navigate = useNavigate();
  const [mobileMenu, setMobileMenu] = useState(false);

  const features = [
    {
      number: "01",
      icon: "spark",
      style: "indigo",
      title: "Smart Summaries",
      text: "Turn long lecture notes into clear, focused summaries with the most important information highlighted.",
    },
    {
      number: "02",
      icon: "book",
      style: "violet",
      title: "Key Concepts",
      text: "Discover important concepts, keywords and topics automatically from your uploaded study materials.",
    },
    {
      number: "03",
      icon: "card",
      style: "amber",
      title: "Flashcards",
      text: "Convert your notes into quick revision cards designed for active recall and faster preparation.",
    },
    {
      number: "04",
      icon: "quiz",
      style: "rose",
      title: "AI Quizzes",
      text: "Generate quizzes from your study material and test your understanding instantly.",
    },
    {
      number: "05",
      icon: "chat",
      style: "purple",
      title: "AI Tutor",
      text: "Ask questions about your notes and get explanations that help you understand difficult concepts.",
    },
    {
      number: "06",
      icon: "chart",
      style: "blue",
      title: "Progress Tracking",
      text: "Track quiz performance, identify weak topics and understand how your learning is improving.",
    },
  ];

  const scrollTo = (id) => {
    setMobileMenu(false);

    const element = document.getElementById(id);

    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  return (
    <div className="modern-home">

      {/* =====================================================
          HEADER
          ===================================================== */}

      <header className="mh-header">
        <div className="mh-header-inner">

          <div className="mh-brand">
  <Logo />
</div>

          <nav className="mh-nav">
            <a href="#features">Features</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#why-smartnotes">Why SmartNotes</a>
          </nav>

          <div className="mh-actions">
            <button
              className="mh-login"
              onClick={() => navigate("/login")}
            >
              Login
            </button>

            <button
              className="mh-signup"
              onClick={() => navigate("/register")}
            >
              Get Started
            </button>
          </div>

          <button
            className="mh-mobile-toggle"
            onClick={() => setMobileMenu(!mobileMenu)}
            aria-label="Toggle navigation"
            aria-expanded={mobileMenu}
          >
            <span />
            <span />
            <span />
          </button>
        </div>

        <div className={`mh-mobile-menu ${mobileMenu ? "open" : ""}`}>
          <button
            className="mh-mobile-link"
            onClick={() => scrollTo("features")}
          >
            Features
          </button>

          <button
            className="mh-mobile-link"
            onClick={() => scrollTo("how-it-works")}
          >
            How It Works
          </button>

          <button
            className="mh-mobile-link"
            onClick={() => scrollTo("why-smartnotes")}
          >
            Why SmartNotes
          </button>

          <div className="mh-mobile-actions">
            <button
              className="mh-login"
              onClick={() => navigate("/login")}
            >
              Login
            </button>

            <button
              className="mh-signup"
              onClick={() => navigate("/register")}
            >
              Get Started
            </button>
          </div>
        </div>
      </header>

      {/* =====================================================
          HERO
          ===================================================== */}

      <section className="mh-hero">
        <div className="mh-hero-inner">

          <div className="mh-hero-left">

            <div className="mh-eyebrow">
              <span className="mh-eyebrow-dot" />
              AI-POWERED LEARNING ASSISTANT
            </div>

            <h1 className="mh-hero-title">
              Study material in.
              <br />
              <span>Smarter learning out.</span>
            </h1>

            <p className="mh-hero-description">
              SmartNotes AI transforms your study materials into
              summaries, key concepts, flashcards, quizzes and
              personalized learning insights — all in one place.
            </p>

            <div className="mh-hero-buttons">

              <button
                className="mh-primary"
                onClick={() => navigate("/register")}
              >
                Start Learning
                <Icon name="arrow" size={14} />
              </button>

              <button
                className="mh-secondary"
                onClick={() => scrollTo("features")}
              >
                Explore Features
              </button>

            </div>

            <div className="mh-trust">
              <span className="mh-trust-check">
                <Icon name="check" size={11} />
              </span>

              Upload notes • Learn • Practice • Improve
            </div>
          </div>

          {/* HERO VISUAL */}

          <div className="mh-hero-right">

            <div className="mh-visual-back" />

            <div className="mh-dashboard">

              <div className="mh-dashboard-top">

                <div className="mh-dots">
                  <span />
                  <span />
                  <span />
                </div>

                <div className="mh-search" />

              </div>

              <div className="mh-dashboard-body">

                <aside className="mh-sidebar">

                  <div className="mh-side-brand">
                    <img
                      src="/logo.png"
                      alt=""
                      onError={(e) => {
                        e.currentTarget.style.display = "none";
                      }}
                    />

                    <div className="mh-side-brand-line" />
                  </div>

                  <div className="mh-side-title">
                    Workspace
                  </div>

                  <div className="mh-side-item active">
                    <span className="mh-side-icon">
                      <Icon name="chart" size={10} />
                    </span>
                    Dashboard
                  </div>

                  <div className="mh-side-item">
                    <span className="mh-side-icon">
                      <Icon name="file" size={10} />
                    </span>
                    My Notes
                  </div>

                  <div className="mh-side-item">
                    <span className="mh-side-icon">
                      <Icon name="upload" size={10} />
                    </span>
                    Upload
                  </div>

                  <div className="mh-side-item">
                    <span className="mh-side-icon">
                      <Icon name="quiz" size={10} />
                    </span>
                    Quizzes
                  </div>

                  <div className="mh-side-item">
                    <span className="mh-side-icon">
                      <Icon name="chart" size={10} />
                    </span>
                    Progress
                  </div>
                </aside>

                <div className="mh-dashboard-content">

                  <div className="mh-dashboard-meta">

                    <div>
                      <div className="mh-small-label">
                        Your learning space
                      </div>

                      <div className="mh-dashboard-heading">
                        Good morning, Student
                      </div>
                    </div>

                    <div className="mh-avatar" />
                  </div>

                  <div className="mh-stat-row">

                    <div className="mh-stat">
                      <div className="mh-stat-label">
                        Notes
                      </div>

                      <div className="mh-stat-value">
                        24
                      </div>

                      <div className="mh-stat-note">
                        +4 this week
                      </div>
                    </div>

                    <div className="mh-stat">
                      <div className="mh-stat-label">
                        Quizzes
                      </div>

                      <div className="mh-stat-value">
                        18
                      </div>

                      <div className="mh-stat-note">
                        82% average
                      </div>
                    </div>

                    <div className="mh-stat">
                      <div className="mh-stat-label">
                        Topics
                      </div>

                      <div className="mh-stat-value">
                        12
                      </div>

                      <div className="mh-stat-note">
                        3 improving
                      </div>
                    </div>

                  </div>

                  <div className="mh-summary">

                    <div className="mh-summary-head">

                      <div className="mh-summary-title">
                        Smart Summary
                      </div>

                      <div className="mh-summary-pill">
                        AI Generated
                      </div>

                    </div>

                    <div className="mh-lines">
                      <span className="one" />
                      <span className="two" />
                      <span className="three" />
                      <span className="four" />
                    </div>

                  </div>

                  <div className="mh-lower">

                    <div className="mh-lower-card">

                      <div className="mh-lower-label">
                        Learning progress
                      </div>

                      <div className="mh-lower-value">
                        82%
                      </div>

                      <div className="mh-lower-bar">
                        <span />
                      </div>

                    </div>

                    <div className="mh-lower-card">

                      <div className="mh-lower-label">
                        Weak topic
                      </div>

                      <div className="mh-lower-value">
                        Networks
                      </div>

                      <div className="mh-lower-bar">
                        <span style={{ width: "58%" }} />
                      </div>

                    </div>

                  </div>
                </div>
              </div>
            </div>

            {/* FLOATING CARD 1 */}

            <div className="mh-floating one">

              <div className="mh-floating-head">
                <span className="mh-floating-icon">
                  <Icon name="spark" size={13} />
                </span>

                AI Summary
              </div>

              <div className="mh-floating-value">
                92%
              </div>

              <div className="mh-floating-note">
                Content understood
              </div>

              <div className="mh-floating-bar">
                <span />
              </div>

            </div>

            {/* FLOATING CARD 2 */}

            <div className="mh-floating two">

              <div className="mh-floating-head">
                <span className="mh-floating-icon">
                  <Icon name="target" size={13} />
                </span>

                Quiz Performance
              </div>

              <div className="mh-floating-value">
                84%
              </div>

              <div className="mh-floating-note">
                Better than your previous score
              </div>

              <div className="mh-floating-bar">
                <span style={{ width: "84%" }} />
              </div>

            </div>

          </div>
        </div>
      </section>

      {/* =====================================================
          VALUE STRIP
          ===================================================== */}

      <section className="mh-value-strip">
        <div className="mh-value-inner">

          <div className="mh-value-item">
            <div className="mh-value-icon">
              <Icon name="upload" size={15} />
            </div>

            <div>
              <strong>Upload Your Notes</strong>
              <span>PDF, documents and study material</span>
            </div>
          </div>

          <div className="mh-value-item">
            <div className="mh-value-icon">
              <Icon name="spark" size={15} />
            </div>

            <div>
              <strong>Let AI Understand</strong>
              <span>Summaries, concepts and questions</span>
            </div>
          </div>

          <div className="mh-value-item">
            <div className="mh-value-icon">
              <Icon name="chart" size={15} />
            </div>

            <div>
              <strong>Track Your Growth</strong>
              <span>Find weak areas and improve</span>
            </div>
          </div>

        </div>
      </section>

      {/* =====================================================
          FEATURES
          ===================================================== */}

      <section
        id="features"
        className="mh-features"
      >
        <div className="mh-container">

          <div className="mh-section-header">

            <div>
              <div className="mh-section-kicker">
                EVERYTHING YOU NEED
              </div>

              <h2 className="mh-section-title">
                One workspace for
                <br />
                smarter study.
              </h2>
            </div>

            <p className="mh-section-description">
              From your first upload to your next quiz,
              SmartNotes AI brings the complete learning
              process into one simple workspace.
            </p>

          </div>

          <div className="mh-feature-grid">

            {features.map((feature) => (
              <article
                className="mh-feature-card"
                key={feature.number}
              >

                <div className="mh-feature-number">
                  {feature.number}
                </div>

                <div
                  className={`mh-feature-icon ${feature.style}`}
                >
                  <Icon
                    name={feature.icon}
                    size={20}
                  />
                </div>

                <h3>
                  {feature.title}
                </h3>

                <p>
                  {feature.text}
                </p>

              </article>
            ))}

          </div>
        </div>
      </section>

      {/* =====================================================
          HOW IT WORKS
          ===================================================== */}

      <section
        id="how-it-works"
        className="mh-flow"
      >
        <div className="mh-container">

          <div className="mh-flow-top">

            <div className="mh-section-kicker">
              HOW IT WORKS
            </div>

            <h2 className="mh-flow-title">
              From notes to
              <br />
              meaningful learning.
            </h2>

            <p className="mh-flow-description">
              SmartNotes AI simplifies the study process
              into three clear steps.
            </p>

          </div>

          <div className="mh-flow-grid">

            <div className="mh-flow-card">

              <div className="mh-flow-number">
                01 / UPLOAD
              </div>

              <div className="mh-flow-icon">
                <Icon name="upload" size={19} />
              </div>

              <h3>
                Upload your notes
              </h3>

              <p>
                Add your lecture notes, PDFs or other
                study materials to your learning workspace.
              </p>

            </div>

            <div className="mh-flow-card">

              <div className="mh-flow-number">
                02 / ANALYZE
              </div>

              <div className="mh-flow-icon">
                <Icon name="spark" size={19} />
              </div>

              <h3>
                Let AI organize them
              </h3>

              <p>
                SmartNotes extracts useful information
                and creates summaries, concepts and practice content.
              </p>

            </div>

            <div className="mh-flow-card">

              <div className="mh-flow-number">
                03 / IMPROVE
              </div>

              <div className="mh-flow-icon">
                <Icon name="target" size={19} />
              </div>

              <h3>
                Practice and improve
              </h3>

              <p>
                Take quizzes, review mistakes, identify weak
                topics and continue practicing.
              </p>

            </div>

          </div>
        </div>
      </section>

      {/* =====================================================
          WHY SMARTNOTES
          ===================================================== */}

      <section
        id="why-smartnotes"
        className="mh-value-section"
      >
        <div className="mh-container">

          <div className="mh-value-layout">

            <div className="mh-value-copy">

              <div className="mh-section-kicker">
                BUILT FOR STUDENTS
              </div>

              <h2>
                Study less randomly.
                <br />
                Learn more intentionally.
              </h2>

              <p>
                SmartNotes AI does more than summarize your
                notes. It connects your study material with
                practice, feedback and progress so you can
                understand where to focus next.
              </p>

              <div className="mh-value-points">

                <div className="mh-value-point">
                  <span className="mh-check">
                    <Icon name="check" size={12} />
                  </span>
                  Understand long study material faster
                </div>

                <div className="mh-value-point">
                  <span className="mh-check">
                    <Icon name="check" size={12} />
                  </span>
                  Practice using AI-generated quizzes
                </div>

                <div className="mh-value-point">
                  <span className="mh-check">
                    <Icon name="check" size={12} />
                  </span>
                  Discover topics that need more attention
                </div>

                <div className="mh-value-point">
                  <span className="mh-check">
                    <Icon name="check" size={12} />
                  </span>
                  Track your learning progress
                </div>

              </div>

            </div>

            <div className="mh-value-panel">

              <div className="mh-panel-top">

                <div className="mh-panel-title">
                  Personalized Learning
                </div>

                <div className="mh-panel-badge">
                  Smart Insights
                </div>

              </div>

              <div className="mh-panel-row">

                <div className="mh-panel-card">

                  <div className="mh-panel-card-icon">
                    <Icon name="file" size={14} />
                  </div>

                  <strong>
                    Summaries
                  </strong>

                  <span>
                    Focus on the important parts of your notes.
                  </span>

                </div>

                <div className="mh-panel-card">

                  <div className="mh-panel-card-icon">
                    <Icon name="quiz" size={14} />
                  </div>

                  <strong>
                    Practice
                  </strong>

                  <span>
                    Test your knowledge through generated quizzes.
                  </span>

                </div>

                <div className="mh-panel-card">

                  <div className="mh-panel-card-icon">
                    <Icon name="target" size={14} />
                  </div>

                  <strong>
                    Weak Topics
                  </strong>

                  <span>
                    Find the areas where more practice is needed.
                  </span>

                </div>

              </div>

              <div className="mh-panel-bottom">

                <div className="mh-panel-bottom-top">

                  <div className="mh-panel-bottom-title">
                    Overall Learning Progress
                  </div>

                  <div className="mh-panel-bottom-score">
                    84%
                  </div>

                </div>

                <div className="mh-panel-bottom-bar">
                  <span />
                </div>

              </div>

            </div>

          </div>
        </div>
      </section>

      {/* =====================================================
          CTA
          ===================================================== */}

      <section className="mh-cta">

        <div className="mh-cta-box">

          <img
            src="/logo.png"
            alt="SmartNotes AI"
            className="mh-cta-logo"
            onError={(e) => {
              e.currentTarget.style.display = "none";
            }}
          />

          <h2>
            Make your notes
            <br />
            work smarter.
          </h2>

          <p>
            Upload your study material and turn it into
            a personalized learning experience with
            SmartNotes AI.
          </p>

          <button
            className="mh-cta-button"
            onClick={() => navigate("/register")}
          >
            Start Learning Free
          </button>

        </div>

      </section>

      {/* =====================================================
          FOOTER
          ===================================================== */}

      <footer className="mh-footer">

        <div className="mh-footer-inner">

          <div className="mh-footer-brand">

            <img
              src="/logo.png"
              alt="SmartNotes AI"
              onError={(e) => {
                e.currentTarget.style.display = "none";
              }}
            />

            <div>
              <strong>
                SmartNotes AI
              </strong>

              <span>
                Intelligent learning assistant
              </span>
            </div>

          </div>

          <div className="mh-footer-copy">
            © {new Date().getFullYear()} SmartNotes AI. All rights reserved.
          </div>

        </div>

      </footer>

    </div>
  );
}

/* =========================================================
   APPLICATION ROUTES
   ========================================================= */

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Home */}
        <Route path="/" element={<Home />} />

        {/* Authentication */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Dashboard */}
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/my-notes" element={<ProtectedRoute><MyNotes /></ProtectedRoute>} />

        {/* Notes */}
        <Route path="/upload" element={<ProtectedRoute><UploadNotes /></ProtectedRoute>} />
        <Route path="/processing" element={<ProtectedRoute><Processing /></ProtectedRoute>} />

        <Route
          path="/notes/:noteId"
          element={<ProtectedRoute><NoteAnalysis /></ProtectedRoute>}
        />

        <Route
          path="/notes/:noteId/summary"
          element={<ProtectedRoute><Summary /></ProtectedRoute>}
        />

        <Route
          path="/notes/:noteId/concepts"
          element={<ProtectedRoute><KeyConcepts /></ProtectedRoute>}
        />

        <Route
          path="/notes/:noteId/flashcards"
          element={<ProtectedRoute><Flashcards /></ProtectedRoute>}
        />

        {/* Quiz */}
        <Route
          path="/notes/:noteId/quiz"
          element={<ProtectedRoute><Quiz /></ProtectedRoute>}
        />

        <Route
          path="/notes/:noteId/quiz-result"
          element={<ProtectedRoute><QuizResult /></ProtectedRoute>}
        />

        {/* Learning */}
        <Route
          path="/weak-topics"
          element={<ProtectedRoute><WeakTopics /></ProtectedRoute>}
        />

        <Route
          path="/learning-quest"
          element={<ProtectedRoute><LearningQuest /></ProtectedRoute>}
        />

        <Route
          path="/notes/:noteId/chat"
          element={<ProtectedRoute><Chat /></ProtectedRoute>}
        />

        <Route
          path="/progress"
          element={<ProtectedRoute><Progress /></ProtectedRoute>}
        />

        {/* Fallback */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
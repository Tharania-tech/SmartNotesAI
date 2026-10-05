import React, { useEffect, useRef, useState } from "react";
import {
  useLocation,
  useNavigate
} from "react-router-dom";

import {
  LayoutDashboard,
  FileText,
  BookOpen,
  ChevronDown,
  BarChart3,
  UploadCloud,
  LogOut,
  CircleUserRound,
  FileText as SummaryIcon,
  Brain,
  Layers3,
  CircleHelp,
  MessageCircle,
  Target,
  Activity,
  Trophy,
  X
} from "lucide-react";

import Logo from "./Logo";

export default function AppHeader() {
  const navigate = useNavigate();
  const location = useLocation();

  const [studyOpen, setStudyOpen] = useState(false);
  const [progressOpen, setProgressOpen] = useState(false);

  const studyRef = useRef(null);
  const progressRef = useRef(null);

  useEffect(function () {
    function handleOutsideClick(event) {
      if (
        studyRef.current &&
        !studyRef.current.contains(event.target)
      ) {
        setStudyOpen(false);
      }

      if (
        progressRef.current &&
        !progressRef.current.contains(event.target)
      ) {
        setProgressOpen(false);
      }
    }

    document.addEventListener("mousedown", handleOutsideClick);

    return function () {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  function closeMenus() {
    setStudyOpen(false);
    setProgressOpen(false);
  }

  function goTo(path) {
    closeMenus();
    navigate(path);
  }

  function handleLogout() {
    localStorage.removeItem("smartnotes-token");
    localStorage.removeItem("smartnotes-user");

    closeMenus();
    navigate("/login");
  }

  const isDashboard = location.pathname === "/dashboard";
  const isMyNotes = location.pathname === "/my-notes";
  const isUpload = location.pathname === "/upload";
  const isProfile = location.pathname === "/profile";

  const studyPaths = [
    "/notes/",
    "/summary",
    "/concepts",
    "/flashcards",
    "/quiz",
    "/chat"
  ];

  let isStudyActive = false;

  for (let i = 0; i < studyPaths.length; i++) {
    if (location.pathname.includes(studyPaths[i])) {
      isStudyActive = true;
      break;
    }
  }

  const isProgressActive =
    location.pathname === "/progress" ||
    location.pathname.includes("/quiz-result");

  return (
    <header className="app-header">

      <div className="app-header-inner">

        {/* LOGO */}
        <button
          type="button"
          className="header-logo-button"
          onClick={function () {
            goTo("/dashboard");
          }}
        >
          <Logo showName={true} />
        </button>

        {/* MAIN NAVIGATION */}
        <nav className="header-nav">

          {/* DASHBOARD */}
          <button
            type="button"
            className={
              isDashboard
                ? "header-nav-link active"
                : "header-nav-link"
            }
            onClick={function () {
              goTo("/dashboard");
            }}
          >
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </button>

          {/* MY NOTES */}
          <button
            type="button"
            className={
              isMyNotes
                ? "header-nav-link active"
                : "header-nav-link"
            }
            onClick={function () {
              goTo("/my-notes");
            }}
          >
            <FileText size={18} />
            <span>My Notes</span>
          </button>

          {/* STUDY DROPDOWN */}
          <div
            className="header-dropdown"
            ref={studyRef}
          >
            <button
              type="button"
              className={
                isStudyActive || studyOpen
                  ? "header-nav-link dropdown-trigger active"
                  : "header-nav-link dropdown-trigger"
              }
              onClick={function () {
                setStudyOpen(!studyOpen);
                setProgressOpen(false);
              }}
            >
              <BookOpen size={19} />
              <span>Study</span>

              <ChevronDown
                size={15}
                className={
                  studyOpen
                    ? "dropdown-chevron rotate"
                    : "dropdown-chevron"
                }
              />
            </button>

            {studyOpen && (
              <div className="header-dropdown-menu study-menu">

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/my-notes");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <SummaryIcon size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      Summary
                    </span>

                    <span className="dropdown-item-description">
                      Read your notes in a simplified form
                    </span>
                  </span>
                </button>

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/my-notes");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <Brain size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      Key Concepts
                    </span>

                    <span className="dropdown-item-description">
                      Discover important concepts and keywords
                    </span>
                  </span>
                </button>

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/my-notes");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <Layers3 size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      Flashcards
                    </span>

                    <span className="dropdown-item-description">
                      Revise topics using interactive cards
                    </span>
                  </span>
                </button>

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/my-notes");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <CircleHelp size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      Quiz
                    </span>

                    <span className="dropdown-item-description">
                      Test your knowledge with AI quizzes
                    </span>
                  </span>
                </button>

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/my-notes");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <MessageCircle size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      AI Tutor
                    </span>

                    <span className="dropdown-item-description">
                      Ask questions and learn interactively
                    </span>
                  </span>
                </button>

              </div>
            )}
          </div>

          {/* PROGRESS DROPDOWN */}
          <div
            className="header-dropdown"
            ref={progressRef}
          >
            <button
              type="button"
              className={
                isProgressActive || progressOpen
                  ? "header-nav-link dropdown-trigger active"
                  : "header-nav-link dropdown-trigger"
              }
              onClick={function () {
                setProgressOpen(!progressOpen);
                setStudyOpen(false);
              }}
            >
              <BarChart3 size={19} />
              <span>Progress</span>

              <ChevronDown
                size={15}
                className={
                  progressOpen
                    ? "dropdown-chevron rotate"
                    : "dropdown-chevron"
                }
              />
            </button>

            {progressOpen && (
              <div className="header-dropdown-menu progress-menu">

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/progress");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <Activity size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      Quiz Performance
                    </span>

                    <span className="dropdown-item-description">
                      Track your quiz scores and attempts
                    </span>
                  </span>
                </button>

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/progress");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <BarChart3 size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      Study Analytics
                    </span>

                    <span className="dropdown-item-description">
                      View your weekly learning activity
                    </span>
                  </span>
                </button>

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/progress");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <Target size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      Topic Progress
                    </span>

                    <span className="dropdown-item-description">
                      Monitor progress across subjects
                    </span>
                  </span>
                </button>

                <button
                  type="button"
                  className="header-dropdown-item"
                  onClick={function () {
                    goTo("/progress");
                  }}
                >
                  <span className="dropdown-item-icon">
                    <Trophy size={17} />
                  </span>

                  <span className="dropdown-item-content">
                    <span className="dropdown-item-title">
                      Achievements
                    </span>

                    <span className="dropdown-item-description">
                      View your learning milestones
                    </span>
                  </span>
                </button>

              </div>
            )}
          </div>

        </nav>

        {/* RIGHT SIDE */}
        <div className="header-right">

          {/* UPLOAD */}
          <button
            type="button"
            className={
              isUpload
                ? "header-upload-button active"
                : "header-upload-button"
            }
            onClick={function () {
              goTo("/upload");
            }}
          >
            <UploadCloud size={18} />
            <span>Upload Notes</span>
          </button>

          {/* PROFILE */}
          <button
            type="button"
            className={
              isProfile
                ? "header-profile-button active"
                : "header-profile-button"
            }
            onClick={function () {
              goTo("/profile");
            }}
          >
            <CircleUserRound size={20} />
            <span>Profile</span>
          </button>

          {/* LOGOUT */}
          <button
            type="button"
            className="header-logout"
            onClick={handleLogout}
          >
            <LogOut size={17} />
            <span>Logout</span>
          </button>

        </div>

      </div>

    </header>
  );
}
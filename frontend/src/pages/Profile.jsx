import React, {
  useState
} from "react";

import {
  Activity,
  Award,
  BarChart3,
  BookOpen,
  Brain,
  CheckCircle2,
  ChevronRight,
  Clock3,
  FileText,
  LogOut,
  Mail,
  Pencil,
  Settings,
  ShieldCheck,
  Sparkles,
  Target,
  Trophy,
  User,
  UploadCloud,
  Zap
} from "lucide-react";

import {
  useNavigate
} from "react-router-dom";

import AppHeader from "../components/AppHeader";


import "./Profile.css";


export default function Profile() {

  const navigate = useNavigate();


  /* =========================================================
     LOAD SAVED USER
     ========================================================= */

  const storedUser =
    localStorage.getItem(
      "smartnotes-user"
    );


  let savedUser = {};


  try {

    if (storedUser) {

      savedUser =
        JSON.parse(
          storedUser
        );

    }

  } catch (error) {

    console.error(
      "Unable to read saved user:",
      error
    );

  }


  /* =========================================================
     USER INFORMATION
     ========================================================= */

  const initialName =
    savedUser.name ||
    savedUser.username ||
    savedUser.full_name ||
    "SmartNotes Learner";


  const initialEmail =
    savedUser.email ||
    savedUser.user_email ||
    "Your email";


  const userRole =
    savedUser.role ||
    "Student";


  /* =========================================================
     PROFILE STATE
     ========================================================= */

  const [profileName, setProfileName] =
    useState(initialName);

  const [profileEmail, setProfileEmail] =
    useState(initialEmail);


  /* =========================================================
     EDIT PROFILE STATE
     ========================================================= */

  const [editOpen, setEditOpen] =
    useState(false);

  const [editName, setEditName] =
    useState(initialName);

  const [editEmail, setEditEmail] =
    useState(initialEmail);


  /* =========================================================
     INITIALS
     ========================================================= */

  function getInitials(name) {

    if (!name) {
      return "SL";
    }


    const parts =
      String(name)
        .trim()
        .split(" ")
        .filter(
          function(item) {
            return item.trim() !== "";
          }
        );


    if (parts.length === 0) {
      return "SL";
    }


    if (parts.length === 1) {

      return parts[0]
        .substring(0, 2)
        .toUpperCase();

    }


    return (
      parts[0].charAt(0) +
      parts[parts.length - 1].charAt(0)
    ).toUpperCase();

  }


  /* =========================================================
     EDIT PROFILE
     ========================================================= */

  function openEditProfile() {

    setEditName(profileName);

    setEditEmail(profileEmail);

    setEditOpen(true);

  }


  function closeEditProfile() {

    setEditOpen(false);

  }


  function handleSaveProfile() {

    const trimmedName =
      editName.trim();


    const trimmedEmail =
      editEmail.trim();


    if (!trimmedName) {

      window.alert(
        "Please enter your name."
      );

      return;

    }


    if (!trimmedEmail) {

      window.alert(
        "Please enter your email address."
      );

      return;

    }


    const updatedUser = {
      ...savedUser,
      name: trimmedName,
      email: trimmedEmail
    };


    localStorage.setItem(
      "smartnotes-user",
      JSON.stringify(updatedUser)
    );


    setProfileName(
      trimmedName
    );

    setProfileEmail(
      trimmedEmail
    );


    setEditOpen(false);

  }


  /* =========================================================
     LOGOUT
     ========================================================= */

  function handleLogout() {

    localStorage.removeItem(
      "smartnotes-token"
    );

    localStorage.removeItem(
      "smartnotes-user"
    );

    navigate("/login");

  }


  /* =========================================================
     NAVIGATION
     ========================================================= */

  function openDashboard() {

    navigate(
      "/dashboard"
    );

  }


  function openMyNotes() {

    navigate(
      "/my-notes"
    );

  }


  function openUpload() {

    navigate(
      "/upload"
    );

  }


  function openProgress() {

    navigate(
      "/progress"
    );

  }


  /* =========================================================
     SCROLL TO PROFILE SECTION
     ========================================================= */

  function scrollToSection(
    sectionId
  ) {

    const section =
      document.getElementById(
        sectionId
      );


    if (section) {

      section.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });

    }

  }


  /* =========================================================
     PAGE
     ========================================================= */

  return (

    <div className="profile-page">


      {/* =====================================================
          GLOBAL APPLICATION HEADER
      ===================================================== */}

      <AppHeader />


      {/* =====================================================
          MAIN PROFILE CONTAINER
      ===================================================== */}

      <main className="profile-container">


        {/* =================================================
            PROFILE HERO
        ================================================= */}

        <section className="profile-hero-new">

          <div className="profile-hero-background"></div>

          <div className="profile-hero-glow profile-hero-glow-one"></div>

          <div className="profile-hero-glow profile-hero-glow-two"></div>


          {/* -------------------------------------------------
              AVATAR
          ------------------------------------------------- */}

          <div className="profile-avatar-block">

            <div className="profile-avatar-ring">

              <div className="profile-avatar">

                {getInitials(profileName)}

              </div>

            </div>


            <span className="profile-online-dot">

              <CheckCircle2 size={12} />

            </span>

          </div>


          {/* -------------------------------------------------
              USER INFORMATION
          ------------------------------------------------- */}

          <div className="profile-hero-user">

            <div className="profile-member-tag">

              <Sparkles size={12} />

              SMARTNOTES MEMBER

            </div>


            <h1>

              Hi, {profileName}

            </h1>


            <p className="profile-hero-role">

              {userRole}

            </p>


            <div className="profile-hero-email">

              <Mail size={14} />

              {profileEmail}

            </div>


            <div className="profile-active-badge">

              <span></span>

              Learning account active

            </div>


            <p className="profile-hero-quote">

              “Small steps every day lead to big results.”

            </p>

          </div>


          {/* -------------------------------------------------
              EDIT PROFILE
          ------------------------------------------------- */}

          <button
            type="button"
            className="profile-hero-edit"
            onClick={openEditProfile}
          >

            <Pencil size={16} />

            Edit Profile

          </button>


        </section>


        {/* =================================================
            PROFILE WORKSPACE
        ================================================= */}

        <section className="profile-workspace">


          {/* =================================================
              PROFILE SIDE NAVIGATION
          ================================================= */}

          <aside className="profile-side-panel">


            <div className="profile-side-title">

              <span>
                PROFILE
              </span>

              <h2>
                My Workspace
              </h2>

            </div>


            {/* OVERVIEW */}

            <button
              type="button"
              className="profile-side-link active"
              onClick={function() {

                scrollToSection(
                  "profile-overview"
                );

              }}
            >

              <User size={17} />

              <span>
                Overview
              </span>

            </button>


            {/* ACCOUNT SETTINGS */}

            <button
              type="button"
              className="profile-side-link"
              onClick={function() {

                scrollToSection(
                  "account-settings"
                );

              }}
            >

              <Settings size={17} />

              <span>
                Account Settings
              </span>

            </button>


            {/* LEARNING PROGRESS */}

            <button
              type="button"
              className="profile-side-link"
              onClick={openProgress}
            >

              <Target size={17} />

              <span>
                Learning Progress
              </span>

            </button>


            {/* STUDY PREFERENCES */}

            <button
              type="button"
              className="profile-side-link"
              onClick={function() {

                scrollToSection(
                  "study-preferences"
                );

              }}
            >

              <Brain size={17} />

              <span>
                Study Preferences
              </span>

            </button>


            {/* ACHIEVEMENTS */}

            <button
              type="button"
              className="profile-side-link"
              onClick={function() {

                scrollToSection(
                  "achievements"
                );

              }}
            >

              <Trophy size={17} />

              <span>
                Achievements
              </span>

            </button>


            {/* ACTIVITY */}

            <button
              type="button"
              className="profile-side-link"
              onClick={function() {

                scrollToSection(
                  "activity-log"
                );

              }}
            >

              <Activity size={17} />

              <span>
                Activity Log
              </span>

            </button>


            {/* -------------------------------------------------
                MOTIVATION CARD
            ------------------------------------------------- */}

            <div className="profile-side-motivation">

              <div className="profile-side-motivation-icon">

                <Zap size={19} />

              </div>


              <strong>

                Better Notes
                <br />
                Bigger Dreams

              </strong>


              <p>

                Your learning journey matters.
                Keep going!

              </p>

            </div>


          </aside>


          {/* =================================================
              MAIN PROFILE CONTENT
          ================================================= */}

          <div className="profile-workspace-content">


            {/* =================================================
                OVERVIEW / SNAPSHOT
            ================================================= */}

            <section
              id="profile-overview"
              className="profile-stat-section"
            >


              <div className="profile-section-heading-new">

                <div>

                  <span>
                    YOUR SNAPSHOT
                  </span>

                  <h2>
                    Learning at a glance
                  </h2>

                </div>


                <button
                  type="button"
                  onClick={openProgress}
                >

                  View Progress

                  <ChevronRight size={15} />

                </button>

              </div>


              <div className="profile-stats-new">


                {/* NOTES */}

                <div className="profile-new-stat-card">

                  <div className="profile-new-stat-icon teal">

                    <FileText size={20} />

                  </div>

                  <div>

                    <span>
                      TOTAL NOTES
                    </span>

                    <strong>
                      5
                    </strong>

                    <small>
                      +2 this week
                    </small>

                  </div>

                </div>


                {/* QUIZZES */}

                <div className="profile-new-stat-card">

                  <div className="profile-new-stat-icon green">

                    <CheckCircle2 size={20} />

                  </div>

                  <div>

                    <span>
                      QUIZZES COMPLETED
                    </span>

                    <strong>
                      3
                    </strong>

                    <small>
                      +1 this week
                    </small>

                  </div>

                </div>


                {/* SCORE */}

                <div className="profile-new-stat-card">

                  <div className="profile-new-stat-icon purple">

                    <Brain size={20} />

                  </div>

                  <div>

                    <span>
                      AVERAGE SCORE
                    </span>

                    <strong>
                      78%
                    </strong>

                    <small>
                      +12% improvement
                    </small>

                  </div>

                </div>


                {/* STUDY TIME */}

                <div className="profile-new-stat-card">

                  <div className="profile-new-stat-icon orange">

                    <Clock3 size={20} />

                  </div>

                  <div>

                    <span>
                      STUDY TIME
                    </span>

                    <strong>
                      12.5h
                    </strong>

                    <small>
                      This month
                    </small>

                  </div>

                </div>


              </div>

            </section>


            {/* =================================================
                LEARNING JOURNEY + OVERALL PROGRESS
            ================================================= */}

            <section className="profile-journey-grid">


              {/* -------------------------------------------------
                  LEARNING JOURNEY
              ------------------------------------------------- */}

              <div className="profile-white-card journey-card">

                <div className="profile-card-top">

                  <div>

                    <span>
                      THIS WEEK
                    </span>

                    <h2>
                      Your Learning Journey
                    </h2>

                    <p>
                      Track your learning activity
                      throughout the week.
                    </p>

                  </div>


                  <div className="profile-card-small-icon">

                    <BarChart3 size={18} />

                  </div>

                </div>


                <div className="profile-chart">


                  <div className="profile-chart-y">

                    <span>
                      100
                    </span>

                    <span>
                      75
                    </span>

                    <span>
                      50
                    </span>

                    <span>
                      25
                    </span>

                    <span>
                      0
                    </span>

                  </div>


                  <div className="profile-chart-main">


                    <div className="profile-chart-line line-one"></div>

                    <div className="profile-chart-line line-two"></div>

                    <div className="profile-chart-line line-three"></div>

                    <div className="profile-chart-line line-four"></div>

                    <div className="profile-chart-line line-five"></div>


                    <div className="profile-chart-bars">


                      <div className="profile-chart-column">

                        <div
                          className="profile-chart-bar"
                          style={{
                            height: "35%"
                          }}
                        ></div>

                        <span>
                          Mon
                        </span>

                      </div>


                      <div className="profile-chart-column">

                        <div
                          className="profile-chart-bar"
                          style={{
                            height: "47%"
                          }}
                        ></div>

                        <span>
                          Tue
                        </span>

                      </div>


                      <div className="profile-chart-column">

                        <div
                          className="profile-chart-bar"
                          style={{
                            height: "57%"
                          }}
                        ></div>

                        <span>
                          Wed
                        </span>

                      </div>


                      <div className="profile-chart-column">

                        <div
                          className="profile-chart-bar"
                          style={{
                            height: "51%"
                          }}
                        ></div>

                        <span>
                          Thu
                        </span>

                      </div>


                      <div className="profile-chart-column">

                        <div
                          className="profile-chart-bar"
                          style={{
                            height: "69%"
                          }}
                        ></div>

                        <span>
                          Fri
                        </span>

                      </div>


                      <div className="profile-chart-column">

                        <div
                          className="profile-chart-bar"
                          style={{
                            height: "60%"
                          }}
                        ></div>

                        <span>
                          Sat
                        </span>

                      </div>


                      <div className="profile-chart-column">

                        <div
                          className="profile-chart-bar highlight"
                          style={{
                            height: "82%"
                          }}
                        ></div>

                        <span>
                          Sun
                        </span>

                      </div>


                    </div>

                  </div>

                </div>

              </div>


              {/* -------------------------------------------------
                  OVERALL PROGRESS
              ------------------------------------------------- */}

              <div className="profile-white-card overall-progress-card">

                <div className="profile-card-top">

                  <div>

                    <span>
                      OVERALL PERFORMANCE
                    </span>

                    <h2>
                      Learning Progress
                    </h2>

                  </div>


                  <div className="profile-card-small-icon">

                    <Target size={18} />

                  </div>

                </div>


                <div className="profile-progress-content">


                  <div className="profile-progress-ring">

                    <div className="profile-progress-ring-inner">

                      <strong>
                        78%
                      </strong>

                      <span>
                        Overall Score
                      </span>

                    </div>

                  </div>


                  <div className="profile-progress-details">


                    {/* RETENTION */}

                    <div className="profile-progress-item">

                      <div>

                        <span>
                          Knowledge Retention
                        </span>

                        <strong>
                          84%
                        </strong>

                      </div>


                      <div className="profile-progress-track">

                        <span
                          style={{
                            width: "84%"
                          }}
                        ></span>

                      </div>

                    </div>


                    {/* READINESS */}

                    <div className="profile-progress-item">

                      <div>

                        <span>
                          Quiz Readiness
                        </span>

                        <strong>
                          76%
                        </strong>

                      </div>


                      <div className="profile-progress-track">

                        <span
                          className="blue"
                          style={{
                            width: "76%"
                          }}
                        ></span>

                      </div>

                    </div>


                    {/* REVISION */}

                    <div className="profile-progress-item">

                      <div>

                        <span>
                          Revision Progress
                        </span>

                        <strong>
                          69%
                        </strong>

                      </div>


                      <div className="profile-progress-track">

                        <span
                          className="purple"
                          style={{
                            width: "69%"
                          }}
                        ></span>

                      </div>

                    </div>


                  </div>

                </div>


                <button
                  type="button"
                  className="profile-progress-button"
                  onClick={openProgress}
                >

                  Explore Progress

                  <ChevronRight size={15} />

                </button>

              </div>


            </section>


            {/* =================================================
                ACTIVITY + ACHIEVEMENTS
            ================================================= */}

            <section className="profile-activity-grid">


              {/* -------------------------------------------------
                  ACTIVITY LOG
              ------------------------------------------------- */}

              <div
                id="activity-log"
                className="profile-white-card activity-card"
              >

                <div className="profile-card-top">

                  <div>

                    <span>
                      RECENT ACTIVITY
                    </span>

                    <h2>
                      What you've been learning
                    </h2>

                  </div>


                  <button
                    type="button"
                    className="profile-view-all"
                  >

                    View All

                  </button>

                </div>


                <div className="profile-activity-list">


                  {/* JAVA QUIZ */}

                  <div className="profile-activity-item">

                    <div className="profile-activity-icon green">

                      <CheckCircle2 size={17} />

                    </div>


                    <div>

                      <strong>
                        Completed Java Quiz
                      </strong>

                      <span>
                        Score: 85% • 2 hours ago
                      </span>

                    </div>


                    <ChevronRight size={16} />

                  </div>


                  {/* DATABASE NOTES */}

                  <div className="profile-activity-item">

                    <div className="profile-activity-icon blue">

                      <FileText size={17} />

                    </div>


                    <div>

                      <strong>
                        Viewed Database Notes
                      </strong>

                      <span>
                        1.2k words • 4 hours ago
                      </span>

                    </div>


                    <ChevronRight size={16} />

                  </div>


                  {/* FLASHCARDS */}

                  <div className="profile-activity-item">

                    <div className="profile-activity-icon purple">

                      <BookOpen size={17} />

                    </div>


                    <div>

                      <strong>
                        Created Flashcards
                      </strong>

                      <span>
                        Database Management • 6 hours ago
                      </span>

                    </div>


                    <ChevronRight size={16} />

                  </div>


                  {/* AI TUTOR */}

                  <div className="profile-activity-item">

                    <div className="profile-activity-icon pink">

                      <Brain size={17} />

                    </div>


                    <div>

                      <strong>
                        Started AI Tutor Session
                      </strong>

                      <span>
                        Java Programming • 1 day ago
                      </span>

                    </div>


                    <ChevronRight size={16} />

                  </div>


                </div>

              </div>


              {/* -------------------------------------------------
                  ACHIEVEMENTS
              ------------------------------------------------- */}

              <div
                id="achievements"
                className="profile-white-card achievements-card"
              >

                <div className="profile-card-top">

                  <div>

                    <span>
                      ACHIEVEMENTS
                    </span>

                    <h2>
                      Your milestones
                    </h2>

                  </div>


                  <Trophy size={19} />

                </div>


                <div className="profile-achievement-grid-new">


                  {/* FIRST NOTE */}

                  <div className="profile-achievement-new earned">

                    <div className="profile-achievement-new-icon">

                      <BookOpen size={20} />

                    </div>


                    <strong>
                      First Note
                    </strong>


                    <span>
                      Upload your first note
                    </span>


                    <small>
                      Earned
                    </small>

                  </div>


                  {/* QUIZ EXPLORER */}

                  <div className="profile-achievement-new earned">

                    <div className="profile-achievement-new-icon purple">

                      <Target size={20} />

                    </div>


                    <strong>
                      Quiz Explorer
                    </strong>


                    <span>
                      Complete your first quiz
                    </span>


                    <small>
                      Earned
                    </small>

                  </div>


                  {/* HIGH PERFORMER */}

                  <div className="profile-achievement-new">

                    <div className="profile-achievement-new-icon orange">

                      <Trophy size={20} />

                    </div>


                    <strong>
                      High Performer
                    </strong>


                    <span>
                      Reach a 90% quiz score
                    </span>


                    <small className="in-progress">
                      In Progress
                    </small>

                  </div>


                  {/* CONSISTENT LEARNER */}

                  <div className="profile-achievement-new">

                    <div className="profile-achievement-new-icon blue">

                      <BarChart3 size={20} />

                    </div>


                    <strong>
                      Consistent Learner
                    </strong>


                    <span>
                      Build a study routine
                    </span>


                    <small className="locked">
                      Locked
                    </small>

                  </div>


                </div>

              </div>


            </section>


            {/* =================================================
                ACCOUNT + STUDY PREFERENCES
            ================================================= */}

            <section className="profile-account-grid">


              {/* -------------------------------------------------
                  ACCOUNT SETTINGS
              ------------------------------------------------- */}

              <div
                id="account-settings"
                className="profile-white-card"
              >

                <div className="profile-card-top">

                  <div>

                    <span>
                      ACCOUNT
                    </span>

                    <h2>
                      Account Information
                    </h2>

                  </div>


                  <button
                    type="button"
                    className="profile-edit-link"
                    onClick={openEditProfile}
                  >

                    <Pencil size={13} />

                    Edit

                  </button>

                </div>


                <div className="profile-account-details">


                  {/* NAME */}

                  <div className="profile-account-detail">

                    <div className="profile-detail-round-icon">

                      <User size={16} />

                    </div>


                    <div>

                      <span>
                        Full Name
                      </span>

                      <strong>
                        {profileName}
                      </strong>

                    </div>

                  </div>


                  {/* EMAIL */}

                  <div className="profile-account-detail">

                    <div className="profile-detail-round-icon">

                      <Mail size={16} />

                    </div>


                    <div>

                      <span>
                        Email Address
                      </span>

                      <strong>
                        {profileEmail}
                      </strong>

                    </div>

                  </div>


                  {/* ROLE */}

                  <div className="profile-account-detail">

                    <div className="profile-detail-round-icon">

                      <Award size={16} />

                    </div>


                    <div>

                      <span>
                        Account Role
                      </span>

                      <strong>
                        {userRole}
                      </strong>

                    </div>

                  </div>


                  {/* STATUS */}

                  <div className="profile-account-detail">

                    <div className="profile-detail-round-icon">

                      <ShieldCheck size={16} />

                    </div>


                    <div>

                      <span>
                        Account Status
                      </span>

                      <strong className="profile-account-active">
                        Active
                      </strong>

                    </div>

                  </div>


                </div>

              </div>


              {/* -------------------------------------------------
                  STUDY PREFERENCES
              ------------------------------------------------- */}

              <div
                id="study-preferences"
                className="profile-white-card"
              >

                <div className="profile-card-top">

                  <div>

                    <span>
                      STUDY PREFERENCES
                    </span>

                    <h2>
                      How you learn best
                    </h2>

                  </div>


                  <Brain size={19} />

                </div>


                <div className="profile-preference-list">


                  {/* DIFFICULTY */}

                  <div className="profile-preference-item">

                    <div className="profile-preference-heading">

                      <span>
                        Preferred Difficulty
                      </span>

                      <strong>
                        Intermediate
                      </strong>

                    </div>


                    <div className="profile-preference-track">

                      <span
                        style={{
                          width: "62%"
                        }}
                      ></span>

                    </div>

                  </div>


                  {/* LEARNING FOCUS */}

                  <div className="profile-preference-item">

                    <div className="profile-preference-heading">

                      <span>
                        Learning Focus
                      </span>

                      <strong>
                        Understanding
                      </strong>

                    </div>


                    <div className="profile-preference-track blue">

                      <span
                        style={{
                          width: "74%"
                        }}
                      ></span>

                    </div>

                  </div>


                  {/* REVISION STYLE */}

                  <div className="profile-preference-item">

                    <div className="profile-preference-heading">

                      <span>
                        Revision Style
                      </span>

                      <strong>
                        Active Recall
                      </strong>

                    </div>


                    <div className="profile-preference-track purple">

                      <span
                        style={{
                          width: "82%"
                        }}
                      ></span>

                    </div>

                  </div>


                </div>


                <div className="profile-learning-tip-new">

                  <Sparkles size={15} />

                  <span>
                    SmartNotes adapts your learning
                    experience around your progress.
                  </span>

                </div>

              </div>


            </section>


            {/* =================================================
                QUICK ACTIONS
            ================================================= */}

            <section className="profile-quick-section">

              <div className="profile-quick-text">

                <span>
                  CONTINUE LEARNING
                </span>


                <h2>
                  Ready to achieve more?
                </h2>


                <p>
                  Explore your notes, practice with quizzes
                  and let AI guide your learning journey.
                </p>

              </div>


              <div className="profile-quick-actions">


                {/* DASHBOARD */}

                <button
                  type="button"
                  onClick={openDashboard}
                >

                  <BookOpen size={18} />

                  <span>
                    Dashboard
                  </span>

                  <ChevronRight size={15} />

                </button>


                {/* MY NOTES */}

                <button
                  type="button"
                  onClick={openMyNotes}
                >

                  <FileText size={18} />

                  <span>
                    My Notes
                  </span>

                  <ChevronRight size={15} />

                </button>


                {/* UPLOAD */}

                <button
                  type="button"
                  onClick={openUpload}
                >

                  <UploadCloud size={18} />

                  <span>
                    Upload Notes
                  </span>

                  <ChevronRight size={15} />

                </button>


                {/* LOGOUT */}

                <button
                  type="button"
                  className="profile-logout-button"
                  onClick={handleLogout}
                >

                  <LogOut size={18} />

                  <span>
                    Logout
                  </span>

                  <ChevronRight size={15} />

                </button>


              </div>

            </section>


            {/* =================================================
                FOOTER
            ================================================= */}

            <footer className="profile-footer-new">


              <div className="profile-footer-brand-new">

                <strong>
                  SmartNotes AI
                </strong>

                <span>
                  Study Smarter, Recall Faster
                </span>

              </div>


              <div className="profile-footer-message">

                <Brain size={15} />

                Your intelligent learning workspace

              </div>


            </footer>


          </div>

        </section>


      </main>


      {/* =====================================================
          EDIT PROFILE MODAL
      ===================================================== */}

      {editOpen && (

        <div className="profile-modal-overlay">

          <div className="profile-edit-modal">


            {/* MODAL HEADER */}

            <div className="profile-edit-modal-header">

              <div>

                <span>
                  ACCOUNT SETTINGS
                </span>

                <h2>
                  Edit Profile
                </h2>

                <p>
                  Update your SmartNotes account information.
                </p>

              </div>


              <button
                type="button"
                className="profile-modal-close"
                onClick={closeEditProfile}
              >
                ×
              </button>

            </div>


            {/* FORM */}

            <div className="profile-edit-form">


              {/* NAME */}

              <label>
                Full Name
              </label>


              <input
                type="text"
                value={editName}
                onChange={function(event) {

                  setEditName(
                    event.target.value
                  );

                }}
                placeholder="Enter your full name"
              />


              {/* EMAIL */}

              <label>
                Email Address
              </label>


              <input
                type="email"
                value={editEmail}
                onChange={function(event) {

                  setEditEmail(
                    event.target.value
                  );

                }}
                placeholder="Enter your email address"
              />


              {/* ROLE */}

              <label>
                Account Role
              </label>


              <input
                type="text"
                value={userRole}
                disabled
              />


            </div>


            {/* MODAL BUTTONS */}

            <div className="profile-edit-modal-actions">


              <button
                type="button"
                className="profile-cancel-button"
                onClick={closeEditProfile}
              >

                Cancel

              </button>


              <button
                type="button"
                className="profile-save-button"
                onClick={handleSaveProfile}
              >

                Save Changes

              </button>


            </div>


          </div>

        </div>

      )}

    <Footer />
    </div>

  );

}
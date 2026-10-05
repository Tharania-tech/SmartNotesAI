import React from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";

import {
  BookOpen,
  Brain,
  Sparkles,
  FileText,
  Layers3,
  MessageCircle,
  ArrowRight,
  ChevronRight,
  Clock3,
  Target,
  CheckCircle2,
  Lightbulb,
  BarChart3
} from "lucide-react";

import AppHeader from "../components/AppHeader";

export default function NoteAnalysis() {
  const navigate = useNavigate();
  const location = useLocation();
  const params = useParams();

  const noteId = params.noteId;

  const noteTitle =
    location &&
    location.state &&
    location.state.title
      ? location.state.title
      : "Your Study Notes";

  const openSummary = () => {
    navigate("/notes/" + noteId + "/summary");
  };

  const openConcepts = () => {
    navigate("/notes/" + noteId + "/concepts");
  };

  const openFlashcards = () => {
    navigate("/notes/" + noteId + "/flashcards");
  };

  const openQuiz = () => {
    navigate("/notes/" + noteId + "/quiz");
  };

  const openTutor = () => {
    navigate("/notes/" + noteId + "/chat");
  };

  return (
    <div className="analysis-page">

      <AppHeader />

      <main className="analysis-main">

        {/* =====================================================
            TOP BAR
            ===================================================== */}

        <div className="analysis-topbar">

          <button
            type="button"
            className="analysis-back-button"
            onClick={() => navigate("/dashboard")}
          >
            <ChevronRight
              size={16}
              className="analysis-back-icon"
            />
            Dashboard
          </button>

          <div className="analysis-topbar-status">
            <CheckCircle2 size={15} />
            Notes analyzed successfully
          </div>

        </div>

        {/* =====================================================
            HERO
            ===================================================== */}

        <section className="analysis-hero">

          <div className="analysis-hero-content">

            <div className="analysis-badge">
              <Sparkles size={14} />
              SMART LEARNING HUB
            </div>

            <h1>
              Your notes are
              <span> ready to learn.</span>
            </h1>

            <p>
              SmartNotes AI has transformed your study material
              into different learning experiences. Choose how
              you want to study.
            </p>

          </div>

        </section>

        {/* =====================================================
            NOTE CARD
            ===================================================== */}

        <section className="analysis-note-card">

          <div className="analysis-note-card-left">

            <div className="analysis-note-large-icon">
              <FileText size={25} />
            </div>

            <div className="analysis-note-details">

              <span>
                CURRENT NOTE
              </span>

              <h2>
                {noteTitle}
              </h2>

              <div className="analysis-note-meta">

                <div>
                  <CheckCircle2 size={13} />
                  Processed
                </div>

                <div>
                  <Clock3 size={13} />
                  Ready to study
                </div>

              </div>

            </div>

          </div>

          <div className="analysis-note-badge">
            <Sparkles size={14} />
            AI Ready
          </div>

        </section>

        {/* =====================================================
            SECTION TITLE
            ===================================================== */}

        <section className="analysis-section-heading">

          <div>

            <span>
              LEARNING TOOLS
            </span>

            <h2>
              Choose your learning experience
            </h2>

          </div>

          <p>
            Start with a summary or explore interactive
            ways to understand and revise your notes.
          </p>

        </section>

        {/* =====================================================
            LEARNING CARDS
            ===================================================== */}

        <section className="analysis-grid">

          {/* SUMMARY */}

          <button
            type="button"
            className="analysis-learning-card analysis-summary-card"
            onClick={openSummary}
          >

            <div className="analysis-card-header">

              <div className="analysis-card-icon">
                <BookOpen size={23} />
              </div>

              <span className="analysis-card-number">
                01
              </span>

            </div>

            <div className="analysis-card-content">

              <h3>
                Smart Summary
              </h3>

              <p>
                Convert lengthy notes into a clear,
                concise summary that is easier to read
                and revise.
              </p>

            </div>

            <div className="analysis-card-footer">

              <span>
                Understand quickly
              </span>

              <div className="analysis-card-arrow">
                <ArrowRight size={17} />
              </div>

            </div>

          </button>

          {/* CONCEPTS */}

          <button
            type="button"
            className="analysis-learning-card analysis-concepts-card"
            onClick={openConcepts}
          >

            <div className="analysis-card-header">

              <div className="analysis-card-icon">
                <Brain size={23} />
              </div>

              <span className="analysis-card-number">
                02
              </span>

            </div>

            <div className="analysis-card-content">

              <h3>
                Key Concepts
              </h3>

              <p>
                Discover the important concepts and
                topics hidden inside your study material.
              </p>

            </div>

            <div className="analysis-card-footer">

              <span>
                Discover key ideas
              </span>

              <div className="analysis-card-arrow">
                <ArrowRight size={17} />
              </div>

            </div>

          </button>

          {/* FLASHCARDS */}

          <button
            type="button"
            className="analysis-learning-card analysis-flashcard-card"
            onClick={openFlashcards}
          >

            <div className="analysis-card-header">

              <div className="analysis-card-icon">
                <Layers3 size={23} />
              </div>

              <span className="analysis-card-number">
                03
              </span>

            </div>

            <div className="analysis-card-content">

              <h3>
                Interactive Flashcards
              </h3>

              <p>
                Revise important information using
                quick question-and-answer flashcards.
              </p>

            </div>

            <div className="analysis-card-footer">

              <span>
                Practice active recall
              </span>

              <div className="analysis-card-arrow">
                <ArrowRight size={17} />
              </div>

            </div>

          </button>

          {/* QUIZ */}

          <button
            type="button"
            className="analysis-learning-card analysis-quiz-card"
            onClick={openQuiz}
          >

            <div className="analysis-card-header">

              <div className="analysis-card-icon">
                <Target size={23} />
              </div>

              <span className="analysis-card-number">
                04
              </span>

            </div>

            <div className="analysis-card-content">

              <div className="analysis-recommended-label">
                Recommended
              </div>

              <h3>
                AI Quiz
              </h3>

              <p>
                Test your understanding with questions
                generated from your own study material.
              </p>

            </div>

            <div className="analysis-card-footer">

              <span>
                Test your knowledge
              </span>

              <div className="analysis-card-arrow">
                <ArrowRight size={17} />
              </div>

            </div>

          </button>

          {/* AI TUTOR */}

          <button
            type="button"
            className="analysis-learning-card analysis-tutor-card"
            onClick={openTutor}
          >

            <div className="analysis-card-header">

              <div className="analysis-card-icon">
                <MessageCircle size={23} />
              </div>

              <span className="analysis-card-number">
                05
              </span>

            </div>

            <div className="analysis-card-content">

              <h3>
                AI Tutor
              </h3>

              <p>
                Ask questions about your notes and
                understand difficult topics with guidance.
              </p>

            </div>

            <div className="analysis-card-footer">

              <span>
                Ask and understand
              </span>

              <div className="analysis-card-arrow">
                <ArrowRight size={17} />
              </div>

            </div>

          </button>

        </section>

        {/* =====================================================
            STUDY FLOW
            ===================================================== */}

        <section className="analysis-study-flow">

          <div className="analysis-study-flow-heading">

            <div className="analysis-flow-icon">
              <BarChart3 size={20} />
            </div>

            <div>
              <span>
                SMART STUDY FLOW
              </span>

              <h2>
                A simple way to learn
              </h2>
            </div>

          </div>

          <div className="analysis-flow-grid">

            <div className="analysis-flow-item">

              <div className="analysis-flow-number">
                1
              </div>

              <div>
                <h3>
                  Understand
                </h3>

                <p>
                  Start with the smart summary and
                  key concepts.
                </p>
              </div>

            </div>

            <div className="analysis-flow-item">

              <div className="analysis-flow-number">
                2
              </div>

              <div>
                <h3>
                  Revise
                </h3>

                <p>
                  Use interactive flashcards to
                  strengthen recall.
                </p>
              </div>

            </div>

            <div className="analysis-flow-item">

              <div className="analysis-flow-number">
                3
              </div>

              <div>
                <h3>
                  Test
                </h3>

                <p>
                  Complete the AI quiz and identify
                  areas that need more practice.
                </p>
              </div>

            </div>

          </div>

        </section>

        {/* =====================================================
            TIP
            ===================================================== */}

        <section className="analysis-tip">

          <div className="analysis-tip-icon">
            <Lightbulb size={19} />
          </div>

          <div>

            <strong>
              Study smarter, not harder
            </strong>

            <p>
              Start with the summary, move to flashcards,
              then take the quiz to check your understanding.
            </p>

          </div>

        </section>

        {/* =====================================================
            FOOTER
            ===================================================== */}

        <div className="analysis-footer">
          SmartNotes AI · Study Smarter, Recall Faster
        </div>

      </main>

    </div>
  );
}
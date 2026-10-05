import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  ArrowLeft,
  ArrowRight,
  Brain,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  FileText,
  Lightbulb,
  RotateCcw,
  Sparkles,
  Layers3
} from "lucide-react";

import AppHeader from "../components/AppHeader";
import { generateFlashcards } from "../services/notesApi";

export default function Flashcards() {
  const navigate = useNavigate();
  const params = useParams();

  const noteId = params.noteId;

  const [flashcards, setFlashcards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadFlashcards = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await generateFlashcards(noteId);

      const data =
        response && response.data
          ? response.data
          : response;

      let cards = [];

      if (
        data &&
        Array.isArray(data.flashcards)
      ) {
        cards = data.flashcards;
      }

      const normalizedCards = cards
        .map(function (card) {
          if (!card || typeof card !== "object") {
            return null;
          }

          const question =
            card.question ||
            card.front ||
            card.prompt ||
            card.term ||
            "";

          const answer =
            card.answer ||
            card.back ||
            card.definition ||
            card.explanation ||
            "";

          const concept =
            card.concept ||
            card.topic ||
            card.subject ||
            "General";

          return {
            question: String(question).trim(),
            answer: String(answer).trim(),
            concept: String(concept).trim()
          };
        })
        .filter(function (card) {
          return (
            card &&
            card.question &&
            card.answer
          );
        });

      if (normalizedCards.length === 0) {
        throw new Error(
          "No flashcards were returned by the server."
        );
      }

      setFlashcards(normalizedCards);
      setCurrentIndex(0);
      setFlipped(false);

    } catch (err) {
      console.error(
        "Flashcards error:",
        err
      );

      setError(
        err && err.message
          ? err.message
          : "Unable to generate flashcards."
      );

    } finally {
      setLoading(false);
    }
  };

  useEffect(function () {
    if (noteId) {
      loadFlashcards();
    } else {
      setError("Note ID is missing.");
      setLoading(false);
    }
  }, [noteId]);

  const totalCards = flashcards.length;

  const currentCard =
    totalCards > 0
      ? flashcards[currentIndex]
      : null;

  const progress =
    totalCards > 0
      ? ((currentIndex + 1) / totalCards) * 100
      : 0;

  const goNext = () => {
    if (totalCards === 0) {
      return;
    }

    if (currentIndex < totalCards - 1) {
      setCurrentIndex(currentIndex + 1);
      setFlipped(false);
    }
  };

  const goPrevious = () => {
    if (currentIndex <= 0) {
      return;
    }

    setCurrentIndex(currentIndex - 1);
    setFlipped(false);
  };

  const restartCards = () => {
    setCurrentIndex(0);
    setFlipped(false);
  };

  const flipCard = () => {
    setFlipped(!flipped);
  };

  return (
    <div className="flashcards-page">

      <AppHeader />

      <main className="flashcards-main">

        {/* =================================================
            TOP NAVIGATION
            ================================================= */}

        <div className="flashcards-topbar">

          <button
            type="button"
            className="flashcards-back-button"
            onClick={function () {
              navigate(
                "/notes/" + noteId
              );
            }}
          >
            <ArrowLeft size={16} />
            Learning Hub
          </button>

          <div className="flashcards-status">
            <CheckCircle2 size={14} />
            Active Recall Mode
          </div>

        </div>

        {/* =================================================
            HERO
            ================================================= */}

        <section className="flashcards-hero">

          <div className="flashcards-hero-icon">
            <Layers3 size={27} />
          </div>

          <div className="flashcards-badge">
            <Sparkles size={13} />
            SMART FLASHCARDS
          </div>

          <h1>
            Learn it.
            <span> Remember it.</span>
          </h1>

          <p>
            Test yourself before revealing the answer.
            Active recall helps you focus on what you truly
            remember.
          </p>

        </section>

        {!loading && !error && currentCard && (

          <>

            {/* =================================================
                PROGRESS
                ================================================= */}

            <section className="flashcards-progress-section">

              <div className="flashcards-progress-top">

                <div>

                  <span>
                    YOUR PROGRESS
                  </span>

                  <strong>
                    Card {currentIndex + 1} of {totalCards}
                  </strong>

                </div>

                <span className="flashcards-progress-percent">
                  {Math.round(progress)}%
                </span>

              </div>

              <div className="flashcards-progress-track">

                <div
                  className="flashcards-progress-bar"
                  style={{
                    width: progress + "%"
                  }}
                ></div>

              </div>

            </section>

            {/* =================================================
                FLASHCARD
                ================================================= */}

            <section className="flashcards-stage">

              <div
                className={
                  "flashcard-study " +
                  (
                    flipped
                      ? "flashcard-study-flipped"
                      : ""
                  )
                }
                onClick={flipCard}
              >

                {!flipped ? (

                  <div className="flashcard-face flashcard-front">

                    <div className="flashcard-face-top">

                      <div className="flashcard-type">
                        QUESTION
                      </div>

                      <div className="flashcard-concept-pill">
                        <Brain size={12} />
                        {currentCard.concept}
                      </div>

                    </div>

                    <div className="flashcard-center">

                      <div className="flashcard-question-icon">
                        <FileText size={25} />
                      </div>

                      <div className="flashcard-question-label">
                        THINK ABOUT IT
                      </div>

                      <h2>
                        {currentCard.question}
                      </h2>

                    </div>

                    <div className="flashcard-flip-hint">

                      <RotateCcw size={14} />

                      <span>
                        Click the card to reveal the answer
                      </span>

                    </div>

                  </div>

                ) : (

                  <div className="flashcard-face flashcard-back">

                    <div className="flashcard-face-top">

                      <div className="flashcard-type flashcard-answer-type">
                        ANSWER
                      </div>

                      <div className="flashcard-concept-pill">
                        <CheckCircle2 size={12} />
                        Revealed
                      </div>

                    </div>

                    <div className="flashcard-center">

                      <div className="flashcard-answer-icon">
                        <CheckCircle2 size={25} />
                      </div>

                      <div className="flashcard-answer-label">
                        CORRECT ANSWER
                      </div>

                      <p>
                        {currentCard.answer}
                      </p>

                    </div>

                    <div className="flashcard-flip-hint">

                      <RotateCcw size={14} />

                      <span>
                        Click to view the question again
                      </span>

                    </div>

                  </div>

                )}

              </div>

            </section>

            {/* =================================================
                CONTROLS
                ================================================= */}

            <section className="flashcards-controls">

              <button
                type="button"
                className="flashcard-control-button"
                onClick={goPrevious}
                disabled={currentIndex === 0}
              >
                <ChevronLeft size={18} />
                Previous
              </button>

              <button
                type="button"
                className="flashcard-control-button flashcard-flip-button"
                onClick={flipCard}
              >
                <RotateCcw size={16} />
                {flipped
                  ? "View Question"
                  : "Show Answer"}
              </button>

              <button
                type="button"
                className="flashcard-control-button flashcard-next-button"
                onClick={goNext}
                disabled={
                  currentIndex === totalCards - 1
                }
              >
                Next
                <ChevronRight size={18} />
              </button>

            </section>

            {/* =================================================
                EXTRA INFO
                ================================================= */}

            <section className="flashcards-info-row">

              <div className="flashcards-info-card">

                <div className="flashcards-info-icon">
                  <Brain size={17} />
                </div>

                <div>
                  <span>
                    CURRENT TOPIC
                  </span>

                  <strong>
                    {currentCard.concept}
                  </strong>
                </div>

              </div>

              <button
                type="button"
                className="flashcards-restart-button"
                onClick={restartCards}
              >
                <RotateCcw size={15} />
                Restart
              </button>

            </section>

            {/* =================================================
                STUDY TIP
                ================================================= */}

            <section className="flashcards-tip">

              <div className="flashcards-tip-icon">
                <Lightbulb size={18} />
              </div>

              <div>

                <span>
                  SMART STUDY TIP
                </span>

                <p>
                  Try answering the question in your mind
                  before flipping the card. That small pause
                  turns reading into active recall.
                </p>

              </div>

            </section>

          </>

        )}

        {/* =================================================
            LOADING
            ================================================= */}

        {loading && (

          <section className="flashcards-loading">

            <div className="flashcards-loading-icon">
              <Brain size={27} />
            </div>

            <div className="flashcards-loading-badge">
              <Sparkles size={12} />
              AI GENERATING
            </div>

            <h2>
              Building your flashcards...
            </h2>

            <p>
              SmartNotes AI is turning the important
              ideas from your notes into revision cards.
            </p>

            <div className="flashcards-loading-stack">

              <span></span>
              <span></span>
              <span></span>

            </div>

          </section>

        )}

        {/* =================================================
            ERROR
            ================================================= */}

        {!loading && error && (

          <section className="flashcards-error">

            <div className="flashcards-error-icon">
              <FileText size={22} />
            </div>

            <h2>
              We couldn't create your flashcards
            </h2>

            <p>
              {error}
            </p>

            <button
              type="button"
              onClick={loadFlashcards}
            >
              Try Again
              <ArrowRight size={15} />
            </button>

          </section>

        )}

        {/* =================================================
            BOTTOM NAV
            ================================================= */}

        {!loading && !error && (

          <div className="flashcards-bottom-nav">

            <button
              type="button"
              onClick={function () {
                navigate(
                  "/notes/" +
                  noteId +
                  "/summary"
                );
              }}
            >
              <FileText size={15} />
              Summary
            </button>

            <button
              type="button"
              className="flashcards-bottom-primary"
              onClick={function () {
                navigate(
                  "/notes/" +
                  noteId +
                  "/quiz"
                );
              }}
            >
              <TargetIcon />
              Take AI Quiz
            </button>

          </div>

        )}

        <div className="flashcards-footer">
          SmartNotes AI · Study Smarter, Recall Faster
        </div>

      </main>

    </div>
  );
}

/* Small local icon component so the page stays self-contained */

function TargetIcon() {
  return (
    <svg
      width="15"
      height="15"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10"></circle>
      <circle cx="12" cy="12" r="6"></circle>
      <circle cx="12" cy="12" r="2"></circle>
    </svg>
  );
}
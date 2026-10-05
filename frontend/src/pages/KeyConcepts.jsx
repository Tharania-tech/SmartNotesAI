import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  ArrowLeft,
  ArrowRight,
  Brain,
  CheckCircle2,
  FileText,
  Search,
  Sparkles,
  Target,
  Lightbulb,
  Layers3
} from "lucide-react";

import AppHeader from "../components/AppHeader";

import { getConcepts } from "../services/notesApi";

export default function KeyConcepts() {
  const navigate = useNavigate();
  const params = useParams();

  const noteId = params.noteId;

  const [concepts, setConcepts] = useState([]);
  const [searchText, setSearchText] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadConcepts() {
    try {
      setLoading(true);
      setError("");

      const response = await getConcepts(noteId);

      const data =
        response && response.data
          ? response.data
          : response;

      let extractedConcepts = [];

      if (
        data &&
        Array.isArray(data.keywords)
      ) {
        extractedConcepts = data.keywords;
      } else if (
        data &&
        Array.isArray(data.concepts)
      ) {
        extractedConcepts = data.concepts;
      }

      const normalizedConcepts = extractedConcepts
        .map(function (item) {
          if (typeof item === "string") {
            return item;
          }

          if (
            item &&
            typeof item === "object"
          ) {
            return (
              item.concept ||
              item.keyword ||
              item.name ||
              ""
            );
          }

          return "";
        })
        .filter(function (item) {
          return item.trim() !== "";
        });

      setConcepts(normalizedConcepts);

    } catch (err) {
      console.error(
        "Key concepts error:",
        err
      );

      setError(
        err && err.message
          ? err.message
          : "Unable to load key concepts."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(function () {
    if (noteId) {
      loadConcepts();
    } else {
      setError("Note ID is missing.");
      setLoading(false);
    }
  }, [noteId]);

  const filteredConcepts = useMemo(
    function () {
      const query = searchText
        .trim()
        .toLowerCase();

      if (!query) {
        return concepts;
      }

      return concepts.filter(
        function (concept) {
          return concept
            .toLowerCase()
            .includes(query);
        }
      );
    },
    [concepts, searchText]
  );

  return (
    <div className="concepts-page">

      <AppHeader />

      <main className="concepts-main">

        {/* Top navigation */}

        <div className="concepts-topbar">

          <button
            type="button"
            className="concepts-back-button"
            onClick={function () {
              navigate(
                "/notes/" + noteId
              );
            }}
          >
            <ArrowLeft size={16} />
            Back to Learning Hub
          </button>

          <div className="concepts-status">
            <CheckCircle2 size={14} />
            AI analysis complete
          </div>

        </div>

        {/* Hero */}

        <section className="concepts-hero">

          <div className="concepts-hero-icon">
            <Brain size={28} />
          </div>

          <div className="concepts-hero-badge">
            <Sparkles size={13} />
            KNOWLEDGE MAP
          </div>

          <h1>
            The ideas that matter
            <span> most.</span>
          </h1>

          <p>
            SmartNotes AI identified the main concepts
            from your study material so you can focus
            on what is important.
          </p>

        </section>

        {/* Overview */}

        <section className="concepts-overview">

          <div className="concepts-note-info">

            <div className="concepts-note-icon">
              <FileText size={20} />
            </div>

            <div>
              <span>
                ANALYZED NOTE
              </span>

              <h2>
                Your uploaded study material
              </h2>
            </div>

          </div>

          <div className="concepts-count-box">

            <strong>
              {concepts.length}
            </strong>

            <span>
              Key Concepts
            </span>

          </div>

          <div className="concepts-quality">

            <div className="concepts-quality-icon">
              <Target size={16} />
            </div>

            <div>
              <strong>
                Focused learning
              </strong>

              <span>
                Revise the highlighted ideas first
              </span>
            </div>

          </div>

        </section>

        {/* Main concepts section */}

        <section className="concepts-content">

          <div className="concepts-content-header">

            <div>

              <span className="concepts-section-label">
                IMPORTANT TOPICS
              </span>

              <h2>
                Explore your key concepts
              </h2>

              <p>
                Use these concepts as a quick revision
                checklist for your notes.
              </p>

            </div>

            <div className="concepts-search">

              <Search size={16} />

              <input
                type="text"
                value={searchText}
                onChange={function (event) {
                  setSearchText(
                    event.target.value
                  );
                }}
                placeholder="Search concepts..."
              />

            </div>

          </div>

          {loading && (

            <div className="concepts-loading">

              <div className="concepts-loading-icon">
                <Brain size={25} />
              </div>

              <h3>
                Discovering key concepts...
              </h3>

              <p>
                SmartNotes AI is identifying the
                important topics in your notes.
              </p>

              <div className="concepts-loading-grid">

                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>

              </div>

            </div>

          )}

          {!loading && error && (

            <div className="concepts-error">
              {error}
            </div>

          )}

          {!loading &&
            !error &&
            filteredConcepts.length === 0 && (

              <div className="concepts-empty">

                <div className="concepts-empty-icon">
                  <Search size={24} />
                </div>

                <h3>
                  No concepts found
                </h3>

                <p>
                  Try a different search term.
                </p>

              </div>

            )}

          {!loading &&
            !error &&
            filteredConcepts.length > 0 && (

              <div className="concepts-grid">

                {filteredConcepts.map(
                  function (concept, index) {

                    return (
                      <div
                        className="concept-explorer-card"
                        key={
                          concept + "-" + index
                        }
                      >

                        <div className="concept-card-top">

                          <div
                            className={
                              "concept-rank rank-" +
                              ((index % 4) + 1)
                            }
                          >
                            {String(
                              index + 1
                            ).padStart(2, "0")}
                          </div>

                          <div className="concept-card-spark">
                            <Sparkles size={14} />
                          </div>

                        </div>

                        <div className="concept-card-body">

                          <div className="concept-card-mini-label">
                            KEY IDEA
                          </div>

                          <h3>
                            {concept}
                          </h3>

                          <p>
                            Important topic identified
                            from your study material.
                          </p>

                        </div>

                        <div className="concept-card-bottom">

                          <span>
                            Review this topic
                          </span>

                          <div className="concept-card-arrow">
                            <ArrowRight size={15} />
                          </div>

                        </div>

                      </div>
                    );
                  }
                )}

              </div>

            )}

        </section>

        {/* Study tip */}

        {!loading &&
          !error &&
          concepts.length > 0 && (

            <section className="concepts-study-tip">

              <div className="concepts-tip-icon">
                <Lightbulb size={20} />
              </div>

              <div>

                <span>
                  SMART STUDY TIP
                </span>

                <h3>
                  Learn the big ideas before the details.
                </h3>

                <p>
                  Start with these key concepts, then use
                  the Summary, Flashcards and AI Quiz to
                  strengthen your understanding.
                </p>

              </div>

              <button
                type="button"
                onClick={function () {
                  navigate(
                    "/notes/" +
                    noteId +
                    "/flashcards"
                  );
                }}
              >
                Practice with Flashcards
                <ArrowRight size={15} />
              </button>

            </section>

          )}

        {/* Bottom navigation */}

        <section className="concepts-bottom-nav">

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
            <FileText size={16} />
            Summary
          </button>

          <button
            type="button"
            className="concepts-bottom-primary"
            onClick={function () {
              navigate(
                "/notes/" +
                noteId +
                "/quiz"
              );
            }}
          >
            <Target size={16} />
            Take AI Quiz
          </button>

          <button
            type="button"
            onClick={function () {
              navigate(
                "/notes/" +
                noteId +
                "/flashcards"
              );
            }}
          >
            <Layers3 size={16} />
            Flashcards
          </button>

        </section>

        <div className="concepts-footer">
          SmartNotes AI · Study Smarter, Recall Faster
        </div>

      </main>
      <Footer />
    </div>
  );
}
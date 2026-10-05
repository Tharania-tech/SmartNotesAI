import React, { useEffect, useRef, useState } from "react";
import {
  BookOpen,
  Copy,
  Check,
  Sparkles,
  RefreshCw,
  Clock3,
  FileText,
  Lightbulb,
  ArrowLeft,
  AlertCircle,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import AppHeader from "../components/AppHeader";

import { generateSummary } from "../services/notesApi";

import "./Summary.css";

export default function Summary() {
  const navigate = useNavigate();
  const { noteId } = useParams();

  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState("");

  // Prevent duplicate request during React StrictMode
  const firstRequestDone = useRef(false);

  /* =========================================================
     EXTRACT SUMMARY FROM API RESPONSE
  ========================================================= */

  const extractSummary = (response) => {
    console.log("FULL SUMMARY RESPONSE:", response);

    // Axios response
    const data =
      response?.data !== undefined
        ? response.data
        : response;

    console.log("SUMMARY RESPONSE DATA:", data);

    if (!data) {
      return "";
    }

    // Direct string response
    if (typeof data === "string") {
      return data.trim();
    }

    // Normal backend response
    if (typeof data.summary === "string") {
      return data.summary.trim();
    }

    // Alternative response name
    if (typeof data.summary_text === "string") {
      return data.summary_text.trim();
    }

    // Alternative response name
    if (typeof data.text === "string") {
      return data.text.trim();
    }

    // Nested response
    if (
      data.data &&
      typeof data.data.summary === "string"
    ) {
      return data.data.summary.trim();
    }

    return "";
  };

  /* =========================================================
     EXTRACT ERROR MESSAGE
  ========================================================= */

  const extractErrorMessage = (err) => {
    console.error("FULL SUMMARY ERROR:", err);

    // Axios error response
    if (err?.response?.data) {
      const serverData = err.response.data;

      // Server returned plain text
      if (typeof serverData === "string") {
        return serverData;
      }

      // Common backend error formats
      if (serverData.message) {
        return serverData.message;
      }

      if (serverData.error) {
        return serverData.error;
      }

      if (serverData.detail) {
        return serverData.detail;
      }
    }

    // JavaScript / Axios error
    if (err?.message) {
      return err.message;
    }

    return "Unable to generate the summary.";
  };

  /* =========================================================
     LOAD SUMMARY
  ========================================================= */

  const loadSummary = async (isRegenerate = false) => {
    if (!noteId) {
      setError("Note ID is missing.");
      setLoading(false);
      setRegenerating(false);
      return;
    }

    try {
      // Clear previous error
      setError("");

      if (isRegenerate) {
        setRegenerating(true);
      } else {
        setLoading(true);
      }

      console.log("=================================");
      console.log("STARTING SUMMARY REQUEST");
      console.log("Note ID:", noteId);
      console.log("=================================");

      const response = await generateSummary(
        noteId,
        "medium"
      );

      console.log("SUMMARY API COMPLETED");
      console.log("Response:", response);

      const summaryText = extractSummary(response);

      // Backend completed but returned no summary
      if (!summaryText) {
        throw new Error(
          "The server completed the request but did not return any summary text."
        );
      }

      // Success
      setSummary(summaryText);
      setError("");

    } catch (err) {
      const message = extractErrorMessage(err);

      setError(message);

      console.error(
        "Summary generation failed:",
        err
      );

    } finally {
      setLoading(false);
      setRegenerating(false);
    }
  };

  /* =========================================================
     INITIAL LOAD
  ========================================================= */

  useEffect(() => {
    if (!noteId) {
      setError("Note ID is missing.");
      setLoading(false);
      return;
    }

    /*
      React StrictMode can execute effects twice
      during development.

      This prevents the first automatic request
      from being sent twice.
    */

    if (firstRequestDone.current) {
      return;
    }

    firstRequestDone.current = true;

    loadSummary(false);

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [noteId]);

  /* =========================================================
     COPY SUMMARY
  ========================================================= */

  const handleCopy = async () => {
    if (!summary) {
      return;
    }

    try {
      await navigator.clipboard.writeText(summary);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 1800);

    } catch (err) {
      console.error("Copy error:", err);

      /*
        Fallback for browsers where
        navigator.clipboard is unavailable.
      */

      try {
        const textarea =
          document.createElement("textarea");

        textarea.value = summary;

        document.body.appendChild(textarea);

        textarea.select();

        document.execCommand("copy");

        document.body.removeChild(textarea);

        setCopied(true);

        setTimeout(() => {
          setCopied(false);
        }, 1800);

      } catch (fallbackError) {
        console.error(
          "Fallback copy failed:",
          fallbackError
        );
      }
    }
  };

  /* =========================================================
     REGENERATE
  ========================================================= */

  const handleRegenerate = async () => {
    if (regenerating || loading) {
      return;
    }

    await loadSummary(true);
  };

  /* =========================================================
     WORD COUNT
  ========================================================= */

  const wordCount = summary
    ? summary
        .trim()
        .split(/\s+/)
        .filter(Boolean)
        .length
    : 0;

  /* =========================================================
     ESTIMATED READ TIME
  ========================================================= */

  const estimatedReadTime =
    wordCount > 0
      ? Math.max(
          1,
          Math.ceil(wordCount / 200)
        )
      : 0;

  /* =========================================================
     UI
  ========================================================= */

  return (
    <div className="summary-page">

      {/* HEADER */}
      <AppHeader />

      <main className="summary-main">

        {/* BACKGROUND DECORATION */}

        <div className="summary-bg-orb summary-bg-orb-one" />

        <div className="summary-bg-orb summary-bg-orb-two" />

        <div className="summary-container">

          {/* =================================================
              BACK BUTTON
          ================================================= */}

          <button
            type="button"
            className="summary-back-button"
            onClick={() => navigate(-1)}
          >
            <ArrowLeft size={17} />

            Back
          </button>


          {/* =================================================
              PAGE HEADER
          ================================================= */}

          <section className="summary-heading">

            <div className="summary-heading-icon">
              <BookOpen size={25} />
            </div>

            <div>

              <div className="summary-ai-badge">
                <Sparkles size={13} />

                AI Generated
              </div>

              <h1>
                Your notes, simplified
              </h1>

              <p>
                SmartNotes AI has transformed your
                study material into an easy-to-review
                summary.
              </p>

            </div>

          </section>


          {/* =================================================
              MAIN SUMMARY CARD

              IMPORTANT:
              The card remains visible even when
              summary generation fails.
          ================================================= */}

          <section className="summary-content-card">

            {/* =================================================
                CARD HEADER
            ================================================= */}

            <div className="summary-card-top">

              <div>

                <div className="summary-label">
                  <Sparkles size={14} />

                  SMART SUMMARY
                </div>

                <h2>
                  Key ideas from your notes
                </h2>

              </div>


              {/* Regenerate button in card header */}

              {!loading &&
                !error &&
                summary && (

                  <button
                    type="button"
                    className="summary-regenerate-button"
                    onClick={handleRegenerate}
                    disabled={regenerating}
                  >

                    <RefreshCw
                      size={16}
                      className={
                        regenerating
                          ? "summary-spin"
                          : ""
                      }
                    />

                    {regenerating
                      ? "Generating..."
                      : "Regenerate"}

                  </button>

                )}

            </div>


            {/* =================================================
                ERROR STATE
            ================================================= */}

            {error ? (

              <div className="summary-error-state">

                <div className="summary-error-icon">
                  <AlertCircle size={28} />
                </div>

                <h3>
                  Unable to generate summary
                </h3>

                <p>
                  {error}
                </p>

                <button
                  type="button"
                  className="summary-error-retry"
                  onClick={() =>
                    loadSummary(false)
                  }
                  disabled={loading}
                >

                  <RefreshCw
                    size={16}
                    className={
                      loading
                        ? "summary-spin"
                        : ""
                    }
                  />

                  {loading
                    ? "Trying Again..."
                    : "Try Again"}

                </button>

              </div>

            ) : loading ? (

              /* =================================================
                  LOADING STATE
              ================================================= */

              <div className="summary-loading">

                <div className="summary-loading-icon">

                  <Sparkles size={25} />

                </div>

                <h3>
                  Creating your smart summary...
                </h3>

                <p>
                  SmartNotes AI is reading your
                  notes and identifying the most
                  important ideas.
                </p>

                <div className="summary-loading-lines">

                  <span />
                  <span />
                  <span />
                  <span />

                </div>

                <div className="summary-loading-note">

                  This may take some time for
                  large notes.

                </div>

              </div>

            ) : (

              /* =================================================
                  SUCCESS STATE
              ================================================= */

              <>

                {/* =================================================
                    STATS
                ================================================= */}

                <div className="summary-stats">

                  {/* WORDS */}

                  <div className="summary-stat">

                    <FileText size={17} />

                    <div>

                      <strong>
                        {wordCount}
                      </strong>

                      <span>
                        Words
                      </span>

                    </div>

                  </div>


                  {/* READ TIME */}

                  <div className="summary-stat">

                    <Clock3 size={17} />

                    <div>

                      <strong>
                        {estimatedReadTime}
                      </strong>

                      <span>
                        Min read
                      </span>

                    </div>

                  </div>


                  {/* REVISION */}

                  <div className="summary-stat">

                    <Lightbulb size={17} />

                    <div>

                      <strong>
                        Easy
                      </strong>

                      <span>
                        Revision
                      </span>

                    </div>

                  </div>

                </div>


                {/* =================================================
                    SUMMARY TEXT
                ================================================= */}

                <div className="summary-text-box">

                  {summary
                    .split(/\n+/)
                    .map(
                      (
                        paragraph,
                        index
                      ) => {

                        const cleanParagraph =
                          paragraph.trim();

                        if (
                          !cleanParagraph
                        ) {
                          return null;
                        }

                        return (

                          <p key={index}>
                            {cleanParagraph}
                          </p>

                        );

                      }
                    )}

                </div>


                {/* =================================================
                    ACTION BUTTONS
                ================================================= */}

                <div className="summary-actions">

                  {/* COPY */}

                  <button
                    type="button"
                    className="summary-copy-button"
                    onClick={handleCopy}
                    disabled={!summary}
                  >

                    {copied ? (

                      <>
                        <Check size={17} />

                        Copied
                      </>

                    ) : (

                      <>
                        <Copy size={17} />

                        Copy Summary
                      </>

                    )}

                  </button>


                  {/* REGENERATE */}

                  <button
                    type="button"
                    className="summary-primary-button"
                    onClick={handleRegenerate}
                    disabled={regenerating}
                  >

                    <RefreshCw
                      size={17}
                      className={
                        regenerating
                          ? "summary-spin"
                          : ""
                      }
                    />

                    {regenerating
                      ? "Generating..."
                      : "Regenerate Summary"}

                  </button>

                </div>

              </>

            )}

          </section>


          {/* =================================================
              STUDY TIP
          ================================================= */}

          {!loading &&
            summary &&
            !error && (

              <section className="summary-tip-card">

                <div className="summary-tip-icon">

                  <Lightbulb size={20} />

                </div>

                <div>

                  <h3>
                    Study tip
                  </h3>

                  <p>
                    Read the summary once, then
                    use the key concepts and
                    flashcards to strengthen
                    your memory.
                  </p>

                </div>

              </section>

            )}


          {/* =================================================
              FOOTER
          ================================================= */}

          <div className="summary-bottom-text">

            Study smarter. Recall faster.

          </div>

        </div>

      </main>
      <Footer />
    </div>
  );
}


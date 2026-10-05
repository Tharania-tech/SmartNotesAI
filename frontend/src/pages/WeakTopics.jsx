import React from "react";
import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  Brain,
  CheckCircle2,
  Lightbulb,
  Target,
  Trophy
} from "lucide-react";

import {
  useLocation,
  useNavigate
} from "react-router-dom";

import AppHeader from "../components/AppHeader";

import "./WeakTopics.css";


export default function WeakTopics() {

  const navigate = useNavigate();
  const location = useLocation();

  const state = location.state || {};

  const noteId =
    state.noteId ||
    "";

  const result =
    state.result ||
    {};

  const quiz =
    state.quiz ||
    result.quiz ||
    [];

  const answers =
    state.answers ||
    result.answers ||
    {};


  /* =========================================================
     FIND USER ANSWER
     ========================================================= */

  function getUserAnswer(
    answerData,
    index
  ) {

    if (!answerData) {
      return "";
    }


    const oneBasedKey =
      String(index + 1);


    const zeroBasedKey =
      String(index);


    if (
      answerData[oneBasedKey] !==
        undefined &&
      answerData[oneBasedKey] !== null
    ) {

      return String(
        answerData[oneBasedKey]
      )
        .trim()
        .toUpperCase();

    }


    if (
      answerData[zeroBasedKey] !==
        undefined &&
      answerData[zeroBasedKey] !== null
    ) {

      return String(
        answerData[zeroBasedKey]
      )
        .trim()
        .toUpperCase();

    }


    return "";

  }


  /* =========================================================
     BUILD TOPIC ANALYSIS
     ========================================================= */

  function buildTopicAnalysis() {

    const topicMap = {};


    if (
      !Array.isArray(quiz)
    ) {

      return [];

    }


    quiz.forEach(
      function(
        question,
        index
      ) {

        const concept =
          question &&
          question.concept
            ? String(
                question.concept
              ).trim()
            : "General Topic";


        const correctAnswer =
          question &&
          (
            question.correct_answer ||
            question.correctAnswer
          )
            ? String(
                question.correct_answer ||
                question.correctAnswer
              )
                .trim()
                .toUpperCase()
            : "";


        const userAnswer =
          getUserAnswer(
            answers,
            index
          );


        if (
          !topicMap[concept]
        ) {

          topicMap[concept] = {
            concept: concept,
            total: 0,
            correct: 0
          };

        }


        topicMap[concept].total += 1;


        if (
          userAnswer &&
          correctAnswer &&
          userAnswer === correctAnswer
        ) {

          topicMap[concept].correct += 1;

        }

      }
    );


    const topics =
      Object.keys(
        topicMap
      ).map(
        function(key) {

          const item =
            topicMap[key];


          const accuracy =
            item.total > 0
              ? Math.round(
                  (
                    item.correct /
                    item.total
                  ) * 100
                )
              : 0;


          let status =
            "Strong";


          if (
            accuracy < 60
          ) {

            status =
              "Weak";

          } else if (
            accuracy < 80
          ) {

            status =
              "Needs Practice";

          }


          return {
            concept:
              item.concept,

            total:
              item.total,

            correct:
              item.correct,

            accuracy:
              accuracy,

            status:
              status
          };

        }
      );


    topics.sort(
      function(a, b) {
        return (
          a.accuracy -
          b.accuracy
        );
      }
    );


    return topics;

  }


  const calculatedTopics =
    buildTopicAnalysis();


  /* =========================================================
     GET BACKEND WEAK TOPICS
     ========================================================= */

  const backendWeakTopics =
    Array.isArray(
      result.weak_topics
    )
      ? result.weak_topics
      : [];


  /* =========================================================
     FINAL TOPICS
     ========================================================= */

  let weakTopics = [];


  if (
    calculatedTopics.length > 0
  ) {

    weakTopics =
      calculatedTopics.filter(
        function(item) {

          return (
            item.accuracy < 60
          );

        }
      );

  }


  /* ---------------------------------------------------------
     FALLBACK TO BACKEND DATA
     --------------------------------------------------------- */

  if (
    weakTopics.length === 0 &&
    backendWeakTopics.length > 0
  ) {

    weakTopics =
      backendWeakTopics.map(
        function(item) {

          let concept = "";


          if (
            item &&
            typeof item === "object"
          ) {

            concept =
              item.concept ||
              item.topic ||
              item.name ||
              "";

          } else {

            concept =
              String(item);

          }


          return {
            concept:
              concept ||
              "Weak Topic",

            total: 0,

            correct: 0,

            accuracy:
              item &&
              typeof item === "object" &&
              item.accuracy !== undefined
                ? Number(
                    item.accuracy
                  )
                : null,

            status:
              "Weak"
          };

        }
      );

  }


  /* =========================================================
     COUNTS
     ========================================================= */

  const weakCount =
    weakTopics.length;


  const allTopics =
    calculatedTopics.length;


  const strongCount =
    calculatedTopics.filter(
      function(item) {

        return (
          item.accuracy >= 80
        );

      }
    ).length;


  const practiceCount =
    calculatedTopics.filter(
      function(item) {

        return (
          item.accuracy >= 60 &&
          item.accuracy < 80
        );

      }
    ).length;


  /* =========================================================
     NAVIGATION
     ========================================================= */

  function handleBack() {

    if (noteId) {

      navigate(
        "/notes/" +
        noteId +
        "/quiz-result",
        {
          state: {
            noteId: noteId,
            quiz: quiz,
            answers: answers,
            result: result
          }
        }
      );

      return;

    }


    navigate(
      "/dashboard"
    );

  }


  function startLearningQuest() {

    navigate(
      "/learning-quest",
      {
        state: {
          noteId: noteId,
          weakTopics: weakTopics,
          quiz: quiz,
          result: result
        }
      }
    );

  }


  /* =========================================================
     PAGE
     ========================================================= */

  return (

    <div className="weak-topics-page">

      <AppHeader />


      <main className="weak-topics-container">


        {/* ===================================================
            TOP BAR
        =================================================== */}

        <div className="weak-topics-topbar">

          <button
            type="button"
            className="weak-topics-back"
            onClick={handleBack}
          >

            <ArrowLeft size={16} />

            Quiz Result

          </button>


          <span className="weak-topics-status">

            <Brain size={14} />

            AI Learning Analysis

          </span>

        </div>


        {/* ===================================================
            HERO
        =================================================== */}

        <section className="weak-topics-hero">

          <div className="weak-topics-hero-icon">

            <Target size={28} />

          </div>


          <div className="weak-topics-hero-content">

            <span>
              PERSONALIZED ANALYSIS
            </span>

            <h1>
              Let's strengthen your weak topics.
            </h1>

            <p>
              SmartNotes analyzed your quiz answers
              to identify the topics that need more
              practice.
            </p>

          </div>


          <div className="weak-topics-hero-badge">

            <strong>
              {weakCount}
            </strong>

            <span>
              Weak Topics
            </span>

          </div>

        </section>


        {/* ===================================================
            SUMMARY CARDS
        =================================================== */}

        <section className="weak-topics-summary">

          <div className="weak-summary-card weak">

            <div className="weak-summary-icon">
              <AlertTriangle size={19} />
            </div>

            <div>

              <span>
                WEAK TOPICS
              </span>

              <strong>
                {weakCount}
              </strong>

              <small>
                Need more attention
              </small>

            </div>

          </div>


          <div className="weak-summary-card practice">

            <div className="weak-summary-icon">
              <Lightbulb size={19} />
            </div>

            <div>

              <span>
                NEEDS PRACTICE
              </span>

              <strong>
                {practiceCount}
              </strong>

              <small>
                Almost there
              </small>

            </div>

          </div>


          <div className="weak-summary-card strong">

            <div className="weak-summary-icon">
              <CheckCircle2 size={19} />
            </div>

            <div>

              <span>
                STRONG TOPICS
              </span>

              <strong>
                {strongCount}
              </strong>

              <small>
                Good understanding
              </small>

            </div>

          </div>


          <div className="weak-summary-card total">

            <div className="weak-summary-icon">
              <Brain size={19} />
            </div>

            <div>

              <span>
                TOPICS ANALYZED
              </span>

              <strong>
                {allTopics}
              </strong>

              <small>
                From this quiz
              </small>

            </div>

          </div>

        </section>


        {/* ===================================================
            WEAK TOPICS
        =================================================== */}

        <section className="weak-topics-card">

          <div className="weak-topics-card-heading">

            <div>

              <span>
                FOCUS AREAS
              </span>

              <h2>
                Topics that need your attention
              </h2>

              <p>
                These topics showed lower accuracy in
                your quiz performance.
              </p>

            </div>


            <div className="weak-heading-icon">

              <AlertTriangle size={20} />

            </div>

          </div>


          {weakTopics.length > 0 ? (

            <div className="weak-topic-list">

              {weakTopics.map(
                function(
                  topic,
                  index
                ) {

                  return (

                    <div
                      className="weak-topic-item"
                      key={index}
                    >

                      <div className="weak-topic-number">

                        {index + 1}

                      </div>


                      <div className="weak-topic-main">

                        <div className="weak-topic-title-row">

                          <strong>
                            {topic.concept}
                          </strong>


                          <span className="weak-topic-badge">
                            {topic.status}
                          </span>

                        </div>


                        <div className="weak-topic-progress-row">

                          <div className="weak-topic-track">

                            <span
                              style={{
                                width:
                                  (
                                    topic.accuracy === null
                                      ? 25
                                      : Math.max(
                                          topic.accuracy,
                                          8
                                        )
                                  ) + "%"
                              }}
                            ></span>

                          </div>


                          <strong className="weak-topic-score">

                            {topic.accuracy === null
                              ? "Needs Review"
                              : topic.accuracy + "%"}

                          </strong>

                        </div>


                        {topic.total > 0 && (

                          <span className="weak-topic-meta">

                            {topic.correct}
                            {" "}
                            correct out of
                            {" "}
                            {topic.total}
                            {" "}
                            questions

                          </span>

                        )}

                      </div>


                      <div className="weak-topic-arrow">

                        <ArrowRight size={17} />

                      </div>

                    </div>

                  );

                }
              )}

            </div>

          ) : (

            <div className="weak-topics-empty">

              <div className="weak-empty-icon">

                <Trophy size={28} />

              </div>


              <h3>
                No weak topics detected
              </h3>


              <p>
                Great work! Your current quiz performance
                did not reveal any topic below the weak-topic
                threshold.
              </p>

            </div>

          )}

        </section>


        {/* ===================================================
            QUEST CTA
        =================================================== */}

        {weakTopics.length > 0 && (

          <section className="weak-topics-quest">

            <div className="weak-quest-icon">

              <Trophy size={24} />

            </div>


            <div className="weak-quest-content">

              <span>
                NEXT STEP
              </span>

              <h2>
                Turn your weak topics into a quest.
              </h2>

              <p>
                Create personalized missions to revise,
                practice and improve these topics.
              </p>

            </div>


            <button
              type="button"
              className="weak-quest-button"
              onClick={startLearningQuest}
            >

              Start Learning Quest

              <ArrowRight size={17} />

            </button>

          </section>

        )}


        {/* ===================================================
            STUDY TIP
        =================================================== */}

        <section className="weak-topics-tip">

          <div className="weak-tip-icon">

            <Lightbulb size={18} />

          </div>


          <div>

            <strong>
              Smart Study Tip
            </strong>

            <p>
              Focus on one weak topic at a time.
              Revise it, practice it, and then test
              yourself again.
            </p>

          </div>

        </section>


      </main>
      <Footer />
    </div>

  );

}
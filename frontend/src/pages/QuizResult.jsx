import React from "react";

import {
  useLocation,
  useNavigate
} from "react-router-dom";

import {
  ArrowLeft,
  ArrowRight,
  Award,
  BookOpen,
  Brain,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  CircleAlert,
  FileText,
  RotateCcw,
  Sparkles,
  Target,
  XCircle,
  Zap
} from "lucide-react";

import AppHeader from "../components/AppHeader";


export default function QuizResult() {

  const navigate = useNavigate();

  const location = useLocation();

  const state = location.state || {};


  // =========================================================
  // RESULT DATA
  // =========================================================

  const result =
    state.result || {};


  const noteId =
    state.noteId ||
    "";


  /*
    Prefer the quiz passed from Quiz.jsx.
    This is important because Quiz.jsx contains
    the normalized options and correct_answer.

    Backend result.quiz is used only as fallback.
  */

  const quiz =
    Array.isArray(state.quiz)
      ? state.quiz
      : Array.isArray(result.quiz)
        ? result.quiz
        : [];


  /*
    Prefer answers passed from Quiz.jsx.
    Backend answers is used only as fallback.
  */

  const answers =
    state.answers &&
    typeof state.answers === "object"
      ? state.answers
      : result.answers &&
        typeof result.answers === "object"
        ? result.answers
        : {};


  // =========================================================
  // SCORE
  // =========================================================

  let score =
    Number(
      result.score_percentage !== undefined
        ? result.score_percentage
        : result.score !== undefined
          ? result.score
          : 0
    );


  if (Number.isNaN(score)) {
    score = 0;
  }


  // =========================================================
  // TOTAL QUESTIONS
  // =========================================================

  const totalQuestions =
    quiz.length ||
    Number(
      result.total_questions ||
      result.question_count ||
      0
    );


  // =========================================================
  // GET USER ANSWER
  // =========================================================

  function getUserAnswer(
    answerData,
    index
  ) {

    if (
      !answerData ||
      typeof answerData !== "object"
    ) {

      return "";

    }


    /*
      IMPORTANT:

      Quiz.jsx stores answers as:

      Question 1 -> answers["1"]
      Question 2 -> answers["2"]
      Question 3 -> answers["3"]

      So the result page must first check
      index + 1.
    */

    const questionNumber =
      index + 1;


    const oneBasedKey =
      String(
        questionNumber
      );


    if (
      answerData[oneBasedKey] !== undefined &&
      answerData[oneBasedKey] !== null
    ) {

      const value =
        String(
          answerData[oneBasedKey]
        )
          .trim()
          .toUpperCase();


      if (value !== "") {
        return value;
      }

    }


    /*
      Support numeric keys too.
    */

    if (
      answerData[questionNumber] !== undefined &&
      answerData[questionNumber] !== null
    ) {

      const value =
        String(
          answerData[questionNumber]
        )
          .trim()
          .toUpperCase();


      if (value !== "") {
        return value;
      }

    }


    /*
      Older quiz versions may have stored
      answers using zero-based indexes.

      Use this only as a fallback.
    */

    const zeroBasedKey =
      String(index);


    if (
      answerData[zeroBasedKey] !== undefined &&
      answerData[zeroBasedKey] !== null
    ) {

      const value =
        String(
          answerData[zeroBasedKey]
        )
          .trim()
          .toUpperCase();


      if (value !== "") {
        return value;
      }

    }


    if (
      answerData[index] !== undefined &&
      answerData[index] !== null
    ) {

      const value =
        String(
          answerData[index]
        )
          .trim()
          .toUpperCase();


      if (value !== "") {
        return value;
      }

    }


    return "";

  }


  // =========================================================
  // GET OPTIONS IN ONE STANDARD FORMAT
  // =========================================================

  function getNormalizedOptions(
    question
  ) {

    if (!question) {
      return [];
    }


    const options =
      question.options;


    /*
      FORMAT 1:

      [
        {
          letter: "A",
          text: "..."
        }
      ]
    */

    if (Array.isArray(options)) {

      return options.map(
        function (
          option,
          index
        ) {

          let text = "";


          if (
            option &&
            typeof option === "object"
          ) {

            text =
              option.text ||
              option.value ||
              option.answer ||
              option.label ||
              "";

          } else {

            text =
              option || "";

          }


          return {

            letter:
              String.fromCharCode(
                65 + index
              ),

            text:
              String(
                text
              ).trim(),

            number:
              index + 1

          };

        }
      );

    }


    /*
      FORMAT 2:

      {
        A: "...",
        B: "...",
        C: "...",
        D: "..."
      }
    */

    if (
      options &&
      typeof options === "object"
    ) {

      const letters = [
        "A",
        "B",
        "C",
        "D"
      ];


      return letters.map(
        function (
          letter,
          index
        ) {

          let value =
            options[letter];


          /*
            Support lowercase keys.
          */

          if (
            value === undefined ||
            value === null
          ) {

            value =
              options[
                letter.toLowerCase()
              ];

          }


          /*
            Support object values.
          */

          if (
            value &&
            typeof value === "object"
          ) {

            value =
              value.text ||
              value.value ||
              value.answer ||
              value.label ||
              "";

          }


          return {

            letter:
              letter,

            text:
              String(
                value === undefined ||
                value === null
                  ? ""
                  : value
              ).trim(),

            number:
              index + 1

          };

        }
      );

    }


    return [];

  }


  // =========================================================
  // GET CORRECT ANSWER
  // =========================================================

  function getCorrectAnswer(
    question,
    index
  ) {

    if (!question) {
      return "";
    }


    let correctAnswer =
      question.correct_answer;


    if (
      correctAnswer === undefined ||
      correctAnswer === null ||
      String(
        correctAnswer
      ).trim() === ""
    ) {

      correctAnswer =
        question.correctAnswer;

    }


    /*
      Direct answer from quiz question.
    */

    if (
      correctAnswer !== undefined &&
      correctAnswer !== null &&
      String(
        correctAnswer
      ).trim() !== ""
    ) {

      const normalized =
        String(
          correctAnswer
        )
          .trim()
          .toUpperCase();


      /*
        A/B/C/D
      */

      if (
        ["A", "B", "C", "D"].includes(
          normalized
        )
      ) {

        return normalized;

      }


      /*
        If correct_answer contains
        the full option text, find its letter.
      */

      const options =
        getNormalizedOptions(
          question
        );


      for (
        let i = 0;
        i < options.length;
        i++
      ) {

        if (
          options[i].text &&
          options[i].text
            .trim()
            .toLowerCase() ===
            normalized.toLowerCase()
        ) {

          return options[i].letter;

        }

      }

    }


    /*
      Backend fallback.
    */

    const possibleResults = [
      result.question_results,
      result.questionResults,
      result.results,
      result.review
    ];


    for (
      let collectionIndex = 0;
      collectionIndex <
      possibleResults.length;
      collectionIndex++
    ) {

      const collection =
        possibleResults[
          collectionIndex
        ];


      if (
        !Array.isArray(collection)
      ) {

        continue;

      }


      const item =
        collection[index];


      if (
        !item ||
        typeof item !== "object"
      ) {

        continue;

      }


      let backendAnswer =
        item.correct_answer;


      if (
        backendAnswer === undefined ||
        backendAnswer === null
      ) {

        backendAnswer =
          item.correctAnswer;

      }


      if (
        backendAnswer !== undefined &&
        backendAnswer !== null
      ) {

        const normalized =
          String(
            backendAnswer
          )
            .trim()
            .toUpperCase();


        if (
          ["A", "B", "C", "D"].includes(
            normalized
          )
        ) {

          return normalized;

        }

      }

    }


    return "";

  }


  // =========================================================
  // GET OPTION TEXT
  // =========================================================

  function getOptionText(
    question,
    letter
  ) {

    if (
      !question ||
      !letter
    ) {

      return "";

    }


    const normalizedLetter =
      String(
        letter
      )
        .trim()
        .toUpperCase();


    const options =
      getNormalizedOptions(
        question
      );


    for (
      let i = 0;
      i < options.length;
      i++
    ) {

      if (
        options[i].letter ===
        normalizedLetter
      ) {

        return options[i].text;

      }

    }


    return "";

  }


  // =========================================================
  // OPTION DISPLAY
  // =========================================================

  function getOptionDisplay(
    question,
    letter
  ) {

    if (!letter) {

      return "Not answered";

    }


    const normalizedLetter =
      String(
        letter
      )
        .trim()
        .toUpperCase();


    const optionText =
      getOptionText(
        question,
        normalizedLetter
      );


    if (!optionText) {

      return normalizedLetter;

    }


    return (
      normalizedLetter +
      ". " +
      optionText
    );

  }


  // =========================================================
  // CORRECT COUNT
  // =========================================================

  function calculateCorrectAnswers(
    questions,
    userAnswers
  ) {

    let count = 0;


    if (
      !Array.isArray(
        questions
      )
    ) {

      return 0;

    }


    questions.forEach(
      function (
        question,
        index
      ) {

        const userAnswer =
          getUserAnswer(
            userAnswers,
            index
          );


        const correctAnswer =
          getCorrectAnswer(
            question,
            index
          );


        if (
          userAnswer &&
          correctAnswer &&
          userAnswer ===
            correctAnswer
        ) {

          count += 1;

        }

      }
    );


    return count;

  }


  // =========================================================
  // CORRECT ANSWERS
  // =========================================================

  const correctAnswers =
    result.correct_answers !== undefined
      ? Number(
          result.correct_answers
        )
      : calculateCorrectAnswers(
          quiz,
          answers
        );


  // =========================================================
  // ANSWERED QUESTIONS
  // =========================================================

  /*
    DO NOT use Object.keys(answers).length.

    Quiz.jsx can contain:

    {
      "1": "A",
      "2": "B",
      "3": "",
      "4": "C",
      "5": ""
    }

    Object.keys() would return 5,
    even though only 3 are answered.

    We count only non-empty answers.
  */

  let answeredQuestions = 0;


  for (
    let i = 0;
    i < totalQuestions;
    i++
  ) {

    const userAnswer =
      getUserAnswer(
        answers,
        i
      );


    if (
      userAnswer
    ) {

      answeredQuestions++;

    }

  }


  const unansweredQuestions =
    Math.max(
      0,
      totalQuestions -
        answeredQuestions
    );


  // =========================================================
  // WRONG ANSWERS
  // =========================================================

  const wrongAnswers =
    result.wrong_answers !== undefined
      ? Number(
          result.wrong_answers
        )
      : Math.max(
          0,
          answeredQuestions -
            correctAnswers
        );


  // =========================================================
  // WEAK TOPICS
  // =========================================================

  const weakTopics =
    result.weak_topics ||
    result.weak_concepts ||
    [];


  // =========================================================
  // NEXT QUIZ
  // =========================================================

  const nextQuiz =
    result.next_quiz ||
    null;


  // =========================================================
  // EXPANDED QUESTION
  // =========================================================

  const [
    expandedQuestion,
    setExpandedQuestion
  ] = React.useState(null);


  // =========================================================
  // RESULT MESSAGE
  // =========================================================

  function getResultMessage() {

    if (score >= 90) {

      return "Outstanding performance!";

    }


    if (score >= 75) {

      return "Great job! You understand this topic well.";

    }


    if (score >= 50) {

      return "Good attempt. A little more revision will help.";

    }


    return "Keep practicing. Your next attempt can be better.";

  }


  // =========================================================
  // RESULT SUBTITLE
  // =========================================================

  function getResultSubtitle() {

    if (score >= 90) {

      return "Excellent understanding and strong recall.";

    }


    if (score >= 75) {

      return "You have built a strong understanding of the notes.";

    }


    if (score >= 50) {

      return "You have a good foundation. Review the weak areas.";

    }


    return "Review the key concepts and try the quiz again.";

  }


  // =========================================================
  // SCORE CLASS
  // =========================================================

  function getScoreClass() {

    if (score >= 75) {

      return "quiz-result-score-good";

    }


    if (score >= 50) {

      return "quiz-result-score-medium";

    }


    return "quiz-result-score-low";

  }


  // =========================================================
  // WEAK TOPIC
  // =========================================================

  function normalizeWeakTopic(
    item
  ) {

    if (
      typeof item === "string"
    ) {

      return item;

    }


    if (
      item &&
      typeof item === "object"
    ) {

      return (
        item.concept ||
        item.topic ||
        item.name ||
        item.title ||
        "Important topic"
      );

    }


    return "Important topic";

  }


  // =========================================================
  // RETRY
  // =========================================================

  function handleRetry() {

    if (!noteId) {

      navigate(
        "/dashboard"
      );

      return;

    }


    navigate(
      "/notes/" +
      noteId +
      "/quiz"
    );

  }


  // =========================================================
  // FLASHCARDS
  // =========================================================

  function handleFlashcards() {

    if (!noteId) {

      navigate(
        "/dashboard"
      );

      return;

    }


    navigate(
      "/notes/" +
      noteId +
      "/flashcards"
    );

  }


  // =========================================================
  // SUMMARY
  // =========================================================

  function handleSummary() {

    if (!noteId) {

      navigate(
        "/dashboard"
      );

      return;

    }


    navigate(
      "/notes/" +
      noteId +
      "/summary"
    );

  }


  // =========================================================
  // LEARNING HUB
  // =========================================================

  function handleLearningHub() {

    if (!noteId) {

      navigate(
        "/dashboard"
      );

      return;

    }


    navigate(
      "/notes/" +
      noteId
    );

  }


  // =========================================================
  // PAGE
  // =========================================================

  return (

    <div className="quiz-result-page">

      <AppHeader />


      <main className="quiz-result-main">


        {/* -------------------------------------------------
            TOP BAR
        ------------------------------------------------- */}

        <div className="quiz-result-topbar">

          <button
            type="button"
            className="quiz-result-back"
            onClick={
              handleLearningHub
            }
          >

            <ArrowLeft
              size={18}
            />

            Learning Hub

          </button>


          <div className="quiz-result-status">

            <Sparkles
              size={15}
            />

            Quiz Completed

          </div>

        </div>


        {/* -------------------------------------------------
            HERO RESULT
        ------------------------------------------------- */}

        <section className="quiz-result-hero">

          <div className="quiz-result-hero-content">

            <div className="quiz-result-trophy">

              <Award
                size={30}
              />

            </div>


            <div>

              <div className="quiz-result-eyebrow">

                YOUR PERFORMANCE

              </div>


              <h1>

                {getResultMessage()}

              </h1>


              <p>

                {getResultSubtitle()}

              </p>

            </div>

          </div>


          <div className="quiz-result-score-wrap">

            <div
              className={
                "quiz-result-score-ring " +
                getScoreClass()
              }
            >

              <div className="quiz-result-score-inner">

                <strong>

                  {Math.round(score)}%

                </strong>


                <span>

                  Score

                </span>

              </div>

            </div>

          </div>

        </section>


        {/* -------------------------------------------------
            QUICK STATS
        ------------------------------------------------- */}

        <section className="quiz-result-stats">


          <div className="quiz-result-stat">

            <div className="quiz-result-stat-icon correct">

              <CheckCircle2
                size={20}
              />

            </div>


            <div>

              <strong>

                {correctAnswers}

              </strong>


              <span>

                Correct

              </span>

            </div>

          </div>


          <div className="quiz-result-stat">

            <div className="quiz-result-stat-icon wrong">

              <XCircle
                size={20}
              />

            </div>


            <div>

              <strong>

                {wrongAnswers}

              </strong>


              <span>

                Wrong

              </span>

            </div>

          </div>


          <div className="quiz-result-stat">

            <div className="quiz-result-stat-icon unanswered">

              <CircleAlert
                size={20}
              />

            </div>


            <div>

              <strong>

                {unansweredQuestions}

              </strong>


              <span>

                Unanswered

              </span>

            </div>

          </div>


          <div className="quiz-result-stat">

            <div className="quiz-result-stat-icon total">

              <Target
                size={20}
              />

            </div>


            <div>

              <strong>

                {totalQuestions}

              </strong>


              <span>

                Total Questions

              </span>

            </div>

          </div>

        </section>


        {/* -------------------------------------------------
            PERFORMANCE MESSAGE
        ------------------------------------------------- */}

        <section className="quiz-result-performance">

          <div className="quiz-result-section-heading">

            <div>

              <span className="quiz-result-mini-label">

                PERFORMANCE

              </span>


              <h2>

                Your quiz overview

              </h2>

            </div>

          </div>


          <div className="quiz-result-progress-box">

            <div className="quiz-result-progress-header">

              <span>

                Overall accuracy

              </span>


              <strong>

                {Math.round(score)}%

              </strong>

            </div>


            <div className="quiz-result-progress-track">

              <div
                className="quiz-result-progress-fill"
                style={{
                  width:
                    Math.min(
                      100,
                      Math.max(
                        0,
                        score
                      )
                    ) +
                    "%"
                }}
              />

            </div>


            <div className="quiz-result-progress-footer">

              <span>

                {correctAnswers}
                {" correct answers"}

              </span>


              <span>

                {totalQuestions}
                {" questions"}

              </span>

            </div>

          </div>

        </section>


        {/* -------------------------------------------------
            WEAK TOPICS
        ------------------------------------------------- */}

        {weakTopics.length > 0 && (

          <section className="quiz-result-weak-section">

            <div className="quiz-result-section-heading">

              <div>

                <span className="quiz-result-mini-label">

                  PERSONALIZED INSIGHT

                </span>


                <h2>

                  Topics to review

                </h2>

              </div>


              <div className="quiz-result-ai-pill">

                <Brain
                  size={15}
                />

                AI Analysis

              </div>

            </div>


            <div className="quiz-result-weak-card">

              <div className="quiz-result-weak-intro">

                <div className="quiz-result-weak-icon">

                  <Target
                    size={22}
                  />

                </div>


                <div>

                  <h3>

                    Focus your next study session

                  </h3>


                  <p>

                    These topics need a little more
                    attention based on your quiz answers.

                  </p>

                </div>

              </div>


              <div className="quiz-result-topic-list">

                {weakTopics.map(
                  function (
                    item,
                    index
                  ) {

                    return (

                      <div
                        className="quiz-result-topic"
                        key={index}
                      >

                        <span className="quiz-result-topic-number">

                          {index + 1}

                        </span>


                        <span>

                          {normalizeWeakTopic(
                            item
                          )}

                        </span>


                        <ArrowRight
                          size={16}
                        />

                      </div>

                    );

                  }
                )}

              </div>

            </div>

          </section>

        )}


        {/* -------------------------------------------------
            NEXT QUIZ
        ------------------------------------------------- */}

        {nextQuiz && (

          <section className="quiz-result-next-section">

            <div className="quiz-result-next-card">

              <div className="quiz-result-next-icon">

                <Zap
                  size={24}
                />

              </div>


              <div className="quiz-result-next-content">

                <span className="quiz-result-mini-label">

                  ADAPTIVE LEARNING

                </span>


                <h2>

                  Your next quiz is ready

                </h2>


                <p>

                  SmartNotes AI has prepared the next
                  learning step based on your performance.

                </p>


                <div className="quiz-result-next-meta">

                  {nextQuiz.level && (

                    <span>

                      <Brain
                        size={14}
                      />

                      {
                        String(
                          nextQuiz.level
                        )
                          .charAt(0)
                          .toUpperCase() +
                        String(
                          nextQuiz.level
                        ).slice(1)
                      }

                    </span>

                  )}


                  {nextQuiz.question_count && (

                    <span>

                      <FileText
                        size={14}
                      />

                      {nextQuiz.question_count}
                      {" Questions"}

                    </span>

                  )}

                </div>

              </div>


              <button
                type="button"
                className="quiz-result-next-button"
                onClick={
                  handleRetry
                }
              >

                Continue Learning

                <ArrowRight
                  size={17}
                />

              </button>
              <button
  type="button"
  className="quiz-result-next-button"
  onClick={function () {

    navigate(
      "/weak-topics",
      {
        state: {
          noteId: noteId,
          quiz: quiz,
          answers: answers,
          result: result
        }
      }
    );

  }}
>
  View Weak Topics
  <ArrowRight size={17} />
</button>

            </div>

          </section>

        )}


        {/* -------------------------------------------------
            QUESTION REVIEW
        ------------------------------------------------- */}

        {quiz.length > 0 && (

          <section className="quiz-result-review-section">

            <div className="quiz-result-section-heading">

              <div>

                <span className="quiz-result-mini-label">

                  REVIEW

                </span>


                <h2>

                  Review your answers

                </h2>

              </div>


              <span className="quiz-result-review-count">

                {quiz.length}
                {" Questions"}

              </span>

            </div>


            <div className="quiz-result-question-list">

              {quiz.map(
                function (
                  question,
                  index
                ) {

                  /*
                    IMPORTANT:

                    Use index + 1 to find the
                    submitted answer.
                  */

                  const userAnswer =
                    getUserAnswer(
                      answers,
                      index
                    );


                  const correctAnswer =
                    getCorrectAnswer(
                      question,
                      index
                    );


                  const isCorrect =
                    Boolean(
                      userAnswer &&
                      correctAnswer &&
                      userAnswer ===
                        correctAnswer
                    );


                  const isExpanded =
                    expandedQuestion ===
                    index;


                  /*
                    Convert both array and object
                    options into A/B/C/D format.
                  */

                  const normalizedOptions =
                    getNormalizedOptions(
                      question
                    );


                  return (

                    <div
                      className={
                        "quiz-result-question " +
                        (
                          isCorrect
                            ? "quiz-result-question-correct"
                            : "quiz-result-question-wrong"
                        )
                      }
                      key={index}
                    >


                      {/* =================================
                          QUESTION HEADER
                          ================================= */}

                      <button
                        type="button"
                        className="quiz-result-question-header"
                        onClick={
                          function () {

                            if (
                              isExpanded
                            ) {

                              setExpandedQuestion(
                                null
                              );

                            } else {

                              setExpandedQuestion(
                                index
                              );

                            }

                          }
                        }
                      >

                        <div className="quiz-result-question-left">

                          <span className="quiz-result-question-number">

                            {index + 1}

                          </span>


                          <div>

                            <span className="quiz-result-question-label">

                              {
                                isCorrect
                                  ? "Correct"
                                  : userAnswer
                                    ? "Needs Review"
                                    : "Not Answered"
                              }

                            </span>


                            <strong>

                              {
                                question.question ||
                                "Question " +
                                (index + 1)
                              }

                            </strong>

                          </div>

                        </div>


                        <div className="quiz-result-question-right">

                          {isCorrect ? (

                            <CheckCircle2
                              size={21}
                              className="result-correct-icon"
                            />

                          ) : (

                            <XCircle
                              size={21}
                              className="result-wrong-icon"
                            />

                          )}


                          {isExpanded ? (

                            <ChevronUp
                              size={18}
                            />

                          ) : (

                            <ChevronDown
                              size={18}
                            />

                          )}

                        </div>

                      </button>


                      {/* =================================
                          QUESTION BODY
                          ================================= */}

                      {isExpanded && (

                        <div className="quiz-result-question-body">


                          {/* =================================
                              ALL OPTIONS
                              ================================= */}

                          <div className="quiz-result-options">


                            {normalizedOptions.map(
                              function (
                                option,
                                optionIndex
                              ) {

                                const letter =
                                  option.letter;


                                const optionText =
                                  option.text;


                                const isSelected =
                                  userAnswer ===
                                  letter;


                                const isAnswer =
                                  correctAnswer ===
                                  letter;


                                let optionClass =
                                  "quiz-result-option";


                                if (
                                  isAnswer
                                ) {

                                  optionClass +=
                                    " quiz-result-option-correct";

                                }


                                if (
                                  isSelected &&
                                  !isAnswer
                                ) {

                                  optionClass +=
                                    " quiz-result-option-wrong";

                                }


                                return (

                                  <div
                                    className={
                                      optionClass
                                    }
                                    key={
                                      letter
                                    }
                                  >


                                    {/* Letter */}

                                    <span className="quiz-result-option-letter">

                                      {letter}

                                    </span>


                                    {/* COMPLETE OPTION */}

                                    <div className="quiz-result-option-text">
                                      <span
                                        style={{
                                          display:
                                            "block"
                                        }}
                                      >

                                        {
                                          optionText ||
                                          "Option text unavailable"
                                        }

                                      </span>

                                    </div>


                                    {/* STATUS */}

                                    {isAnswer && (

                                      <span className="quiz-result-option-badge">

                                        Correct Answer

                                      </span>

                                    )}


                                    {isSelected &&
                                      !isAnswer && (

                                      <span className="quiz-result-option-badge wrong-badge">

                                        Your Answer

                                      </span>

                                    )}

                                  </div>

                                );

                              }
                            )}


                          </div>


                          {/* =================================
                              ANSWER SUMMARY
                              ================================= */}

                          <div className="quiz-result-answer-summary">


                            {/* USER ANSWER */}

                            <div>

                              <span>

                                Your answer

                              </span>


                              <strong
                                className={
                                  isCorrect
                                    ? "answer-green"
                                    : userAnswer
                                      ? "answer-red"
                                      : "answer-red"
                                }
                              >

                                {
                                  userAnswer
                                    ? getOptionDisplay(
                                        question,
                                        userAnswer
                                      )
                                    : "Not answered"
                                }

                              </strong>

                            </div>


                            {/* CORRECT ANSWER */}

                            <div>

                              <span>

                                Correct answer

                              </span>


                              <strong className="answer-green">

                                {
                                  correctAnswer
                                    ? getOptionDisplay(
                                        question,
                                        correctAnswer
                                      )
                                    : "Answer unavailable"
                                }

                              </strong>

                            </div>

                          </div>


                          {/* =================================
                              EXPLANATION
                              ================================= */}

                          {question.explanation && (

                            <div className="quiz-result-explanation">

                              <Sparkles
                                size={17}
                              />


                              <div>

                                <strong>

                                  Explanation

                                </strong>


                                <p>

                                  {question.explanation}

                                </p>

                              </div>

                            </div>

                          )}

                        </div>

                      )}

                    </div>

                  );

                }
              )}

            </div>

          </section>

        )}


        {/* -------------------------------------------------
            STUDY RECOMMENDATION
        ------------------------------------------------- */}

        <section className="quiz-result-study-section">

          <div className="quiz-result-study-card">

            <div className="quiz-result-study-icon">

              <BookOpen
                size={25}
              />

            </div>


            <div className="quiz-result-study-content">

              <span className="quiz-result-mini-label">

                SMART STUDY TIP

              </span>


              <h3>

                {
                  score >= 75
                    ? "Keep your momentum going"
                    : "Strengthen your weak concepts first"
                }

              </h3>


              <p>

                {
                  score >= 75
                    ? "You are doing well. Use flashcards and a short summary review to strengthen recall."
                    : "Review the important concepts, practice with flashcards, and then retake the quiz."
                }

              </p>

            </div>


            <button
              type="button"
              className="quiz-result-study-button"
              onClick={
                handleFlashcards
              }
            >

              Review Flashcards

              <ArrowRight
                size={17}
              />

            </button>

          </div>

        </section>


        {/* -------------------------------------------------
            ACTION BUTTONS
        ------------------------------------------------- */}

        <section className="quiz-result-actions">

          <button
            type="button"
            className="quiz-result-action primary"
            onClick={
              handleRetry
            }
          >

            <RotateCcw
              size={17}
            />

            Retake Quiz

          </button>


          <button
            type="button"
            className="quiz-result-action secondary"
            onClick={
              handleFlashcards
            }
          >

            <BookOpen
              size={17}
            />

            Study Flashcards

          </button>


          <button
            type="button"
            className="quiz-result-action secondary"
            onClick={
              handleSummary
            }
          >

            <FileText
              size={17}
            />

            View Summary

          </button>

        </section>


        {/* -------------------------------------------------
            FOOTER NAV
        ------------------------------------------------- */}

        <div className="quiz-result-footer-nav">

          <button
            type="button"
            onClick={
              handleLearningHub
            }
          >

            <ArrowLeft
              size={16}
            />

            Back to Learning Hub

          </button>


          <span>

            SmartNotes AI • Study Smarter, Recall Faster

          </span>

        </div>

      </main>
      <Footer />
    </div>

  );

}
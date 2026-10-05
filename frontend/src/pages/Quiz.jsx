import React, {
  useEffect,
  useMemo,
  useState
} from "react";

import {
  useNavigate,
  useParams
} from "react-router-dom";

import {
  ArrowLeft,
  ArrowRight,
  Brain,
  Check,
  CheckCircle2,
  Clock3,
  FileText,
  Flag,
  HelpCircle,
  Target,
  Trophy,
  XCircle
} from "lucide-react";

import AppHeader from "../components/AppHeader";

import {
  generateQuiz,
  submitQuiz
} from "../services/notesApi";


function Quiz() {

  const navigate = useNavigate();

  const params = useParams();

  const noteId = params.noteId;


  // =========================================================
  // QUIZ DATA
  // =========================================================

  const [quiz, setQuiz] =
    useState([]);

  const [answers, setAnswers] =
    useState({});

  const [currentIndex, setCurrentIndex] =
    useState(0);


  // =========================================================
  // STATES
  // =========================================================

  const [loading, setLoading] =
    useState(false);

  const [generating, setGenerating] =
    useState(false);

  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] =
    useState("");


  // =========================================================
  // QUIZ PREFERENCES
  // =========================================================

  const [quizStarted, setQuizStarted] =
    useState(false);

  const [difficulty, setDifficulty] =
    useState("intermediate");

  const [questionCount, setQuestionCount] =
    useState(10);


  // =========================================================
  // TIMER
  // =========================================================

  const [timeLeft, setTimeLeft] =
    useState(0);


  // =========================================================
  // CHECK NOTE ID
  // =========================================================

  useEffect(
    function () {

      if (!noteId) {

        setError(
          "Note ID is missing."
        );

      }

    },
    [noteId]
  );


  // =========================================================
  // NORMALIZE OPTION VALUE
  // =========================================================

  function normalizeOptionValue(
    value
  ) {

    if (
      value === null ||
      value === undefined
    ) {
      return "";
    }


    if (
      typeof value === "object"
    ) {

      return String(
        value.text ||
        value.value ||
        value.answer ||
        value.label ||
        ""
      ).trim();

    }


    return String(
      value
    ).trim();

  }


  // =========================================================
  // NORMALIZE CORRECT ANSWER
  // =========================================================

  function normalizeCorrectAnswer(
    item,
    normalizedOptions
  ) {

    if (!item) {
      return "";
    }


    let answer =
      item.correct_answer;


    if (
      answer === undefined ||
      answer === null ||
      String(answer).trim() === ""
    ) {

      answer =
        item.correctAnswer;

    }


    if (
      answer === undefined ||
      answer === null
    ) {

      return "";

    }


    const cleanAnswer =
      String(answer)
        .trim()
        .toUpperCase();


    // Direct letter

    if (
      ["A", "B", "C", "D"].includes(
        cleanAnswer
      )
    ) {

      return cleanAnswer;

    }


    // Sometimes the backend/model may return
    // the full option text instead of the letter.

    for (
      let i = 0;
      i < normalizedOptions.length;
      i++
    ) {

      const option =
        normalizedOptions[i];


      if (
        option.text &&
        option.text.trim().toLowerCase() ===
          cleanAnswer.toLowerCase()
      ) {

        return option.letter;

      }

    }


    return "";

  }


  // =========================================================
  // GENERATE QUIZ
  // =========================================================

  async function handleGenerateQuiz() {

    if (!noteId) {

      setError(
        "Note ID is missing."
      );

      return;
    }


    try {

      setGenerating(true);

      setLoading(true);

      setError("");


      console.log(
        "========================================"
      );

      console.log(
        "GENERATING QUIZ"
      );

      console.log(
        "Note ID:",
        noteId
      );

      console.log(
        "Difficulty:",
        difficulty
      );

      console.log(
        "Question Count:",
        questionCount
      );

      console.log(
        "========================================"
      );


      // -----------------------------------------------------
      // CALL BACKEND
      // -----------------------------------------------------

      const response =
        await generateQuiz(
          noteId,
          difficulty,
          questionCount
        );


      console.log(
        "QUIZ API RESPONSE:",
        response
      );


      /*
        notesApi.js returns response.data directly.
      */

      const data =
        response || {};


      const generatedQuiz =
        data &&
        Array.isArray(data.quiz)
          ? data.quiz
          : [];


      if (
        generatedQuiz.length === 0
      ) {

        throw new Error(
          "No quiz questions were generated. Please try again."
        );

      }


      // =====================================================
      // NORMALIZE QUESTIONS
      // =====================================================

      const normalizedQuiz =
        generatedQuiz.map(
          function (item) {

            const options =
              item &&
              item.options
                ? item.options
                : {};


            let normalizedOptions =
              [];


            // ------------------------------------------------
            // ARRAY OPTIONS
            // ------------------------------------------------

            if (
              Array.isArray(options)
            ) {

              normalizedOptions =
                options.map(
                  function (
                    option,
                    index
                  ) {

                    return {

                      letter:
                        String.fromCharCode(
                          65 + index
                        ),

                      text:
                        normalizeOptionValue(
                          option
                        )

                    };

                  }
                );

            }


            // ------------------------------------------------
            // OBJECT OPTIONS
            // ------------------------------------------------

            else if (
              options &&
              typeof options ===
                "object"
            ) {

              const letters = [
                "A",
                "B",
                "C",
                "D"
              ];


              letters.forEach(
                function (letter) {

                  let value =
                    options[letter];


                  if (
                    value === undefined
                  ) {

                    value =
                      options[
                        letter.toLowerCase()
                      ];

                  }


                  if (
                    value !== undefined &&
                    value !== null
                  ) {

                    normalizedOptions.push({

                      letter:
                        letter,

                      text:
                        normalizeOptionValue(
                          value
                        )

                    });

                  }

                }
              );

            }


            // ------------------------------------------------
            // CORRECT ANSWER
            // ------------------------------------------------

            const correctAnswer =
              normalizeCorrectAnswer(
                item,
                normalizedOptions
              );


            // ------------------------------------------------
            // EXPLANATION
            // ------------------------------------------------

            const explanation =
              item &&
              item.explanation
                ? String(
                    item.explanation
                  ).trim()
                : "";


            // ------------------------------------------------
            // CONCEPT
            // ------------------------------------------------

            const concept =
              item &&
              item.concept
                ? String(
                    item.concept
                  ).trim()
                : "General";


            // ------------------------------------------------
            // DIFFICULTY
            // ------------------------------------------------

            let itemDifficulty =
              difficulty;


            if (
              item &&
              item.difficulty
            ) {

              itemDifficulty =
                String(
                  item.difficulty
                ).trim();

            }


            // ------------------------------------------------
            // RETURN COMPLETE QUESTION
            // ------------------------------------------------

            return {

              question:
                item &&
                item.question
                  ? String(
                      item.question
                    ).trim()
                  : "Question",


              options:
                normalizedOptions,


              correct_answer:
                correctAnswer,


              explanation:
                explanation,


              concept:
                concept,


              difficulty:
                itemDifficulty

            };

          }
        );


      if (
        normalizedQuiz.length === 0
      ) {

        throw new Error(
          "Quiz questions could not be processed."
        );

      }


      // -----------------------------------------------------
      // Validate questions
      // -----------------------------------------------------

      for (
        let i = 0;
        i < normalizedQuiz.length;
        i++
      ) {

        const question =
          normalizedQuiz[i];


        if (
          !question.question
        ) {

          throw new Error(
            "A quiz question is missing."
          );

        }


        if (
          !Array.isArray(
            question.options
          ) ||
          question.options.length <
            4
        ) {

          throw new Error(
            "A quiz question does not contain four options."
          );

        }

      }


      // =====================================================
      // RESET QUIZ
      // =====================================================

      setQuiz(
        normalizedQuiz
      );


      /*
        Start with an empty answer for every question.

        Example:

        {
          "1": "",
          "2": "",
          "3": "",
          "4": ""
        }

        When the student chooses B for Question 1:

        {
          "1": "B",
          "2": "",
          "3": "",
          "4": ""
        }

        This gives the result page a reliable
        one-based structure.
      */

      const initialAnswers = {};


      for (
        let i = 0;
        i < normalizedQuiz.length;
        i++
      ) {

        initialAnswers[
          String(i + 1)
        ] = "";

      }


      setAnswers(
        initialAnswers
      );


      setCurrentIndex(0);


      // =====================================================
      // TIMER
      // =====================================================

      const totalSeconds =
        Math.max(
          60,
          Math.round(
            normalizedQuiz.length *
            1.5 *
            60
          )
        );


      setTimeLeft(
        totalSeconds
      );


      setQuizStarted(
        true
      );


      console.log(
        "QUIZ READY:"
      );

      console.log(
        normalizedQuiz
      );

      console.log(
        "INITIAL ANSWERS:"
      );

      console.log(
        initialAnswers
      );


    } catch (err) {

      console.error(
        "Quiz generation error:",
        err
      );


      setError(
        err &&
        err.message
          ? err.message
          : "Unable to generate the quiz."
      );


    } finally {

      setGenerating(false);

      setLoading(false);

    }

  }


  // =========================================================
  // TIMER
  // =========================================================

  useEffect(
    function () {

      if (
        !quizStarted ||
        loading ||
        submitting ||
        timeLeft <= 0
      ) {

        return;

      }


      const timer =
        setInterval(
          function () {

            setTimeLeft(
              function (previous) {

                if (
                  previous <= 1
                ) {

                  return 0;

                }


                return previous - 1;

              }
            );

          },
          1000
        );


      return function () {

        clearInterval(
          timer
        );

      };

    },
    [
      quizStarted,
      loading,
      submitting,
      timeLeft
    ]
  );


  // =========================================================
  // QUIZ INFORMATION
  // =========================================================

  const currentQuestion =
    quiz[currentIndex];


  /*
    Only count answers that actually
    contain a letter.

    Empty strings are NOT counted.
  */

  const answeredCount =
    Object.keys(answers)
      .filter(
        function (key) {

          return (
            answers[key] !== undefined &&
            answers[key] !== null &&
            String(
              answers[key]
            ).trim() !== ""
          );

        }
      )
      .length;


  const unansweredCount =
    Math.max(
      0,
      quiz.length -
        answeredCount
    );


  const quizProgress =
    quiz.length > 0
      ? (
          (currentIndex + 1) /
          quiz.length
        ) * 100
      : 0;


  const overallProgress =
    quiz.length > 0
      ? (
          answeredCount /
          quiz.length
        ) * 100
      : 0;


  // =========================================================
  // TIMER FORMAT
  // =========================================================

  const formattedTime =
    useMemo(
      function () {

        const minutes =
          Math.floor(
            timeLeft / 60
          );


        const seconds =
          timeLeft % 60;


        return (
          String(
            minutes
          ).padStart(
            2,
            "0"
          ) +
          ":" +
          String(
            seconds
          ).padStart(
            2,
            "0"
          )
        );

      },
      [timeLeft]
    );


  // =========================================================
  // SELECT ANSWER
  // =========================================================

  function selectAnswer(
    letter
  ) {

    const questionNumber =
      String(
        currentIndex + 1
      );


    const selectedLetter =
      String(
        letter || ""
      )
        .trim()
        .toUpperCase();


    setAnswers(
      function (previous) {

        return {

          ...previous,

          [questionNumber]:
            selectedLetter

        };

      }
    );

  }


  // =========================================================
  // NEXT
  // =========================================================

  function goNext() {

    if (
      currentIndex <
      quiz.length - 1
    ) {

      setCurrentIndex(
        currentIndex + 1
      );

    }

  }


  // =========================================================
  // PREVIOUS
  // =========================================================

  function goPrevious() {

    if (
      currentIndex > 0
    ) {

      setCurrentIndex(
        currentIndex - 1
      );

    }

  }


  // =========================================================
  // QUESTION NAVIGATOR
  // =========================================================

  function goToQuestion(
    index
  ) {

    setCurrentIndex(
      index
    );

  }


  // =========================================================
  // SUBMIT QUIZ
  // =========================================================

  async function handleSubmit() {

    if (
      quiz.length === 0
    ) {

      return;

    }


    /*
      Calculate unanswered using
      actual non-empty values.
    */

    const unanswered =
      quiz.length -
      Object.keys(answers)
        .filter(
          function (key) {

            return (
              answers[key] !== undefined &&
              answers[key] !== null &&
              String(
                answers[key]
              ).trim() !== ""
            );

          }
        )
        .length;


    if (
      unanswered > 0
    ) {

      const confirmed =
        window.confirm(
          "You have " +
          unanswered +
          " unanswered question" +
          (
            unanswered === 1
              ? ""
              : "s"
          ) +
          ". Do you want to submit anyway?"
        );


      if (!confirmed) {

        return;

      }

    }


    try {

      setSubmitting(
        true
      );

      setError("");


      console.log(
        "========================================"
      );

      console.log(
        "SUBMITTING QUIZ"
      );

      console.log(
        "Note ID:",
        noteId
      );

      console.log(
        "Answers:",
        answers
      );

      console.log(
        "========================================"
      );


      /*
        Build a clean answers object.

        Every question gets a key.

        Example:

        {
          "1": "A",
          "2": "C",
          "3": "B",
          "4": "",
          "5": "D"
        }

        Therefore the result page can reliably determine
        which questions were answered.
      */

      const submittedAnswers = {};


      for (
        let i = 0;
        i < quiz.length;
        i++
      ) {

        const key =
          String(i + 1);


        let value =
          answers[key];


        if (
          value === undefined ||
          value === null
        ) {

          value = "";

        }


        submittedAnswers[key] =
          String(
            value
          )
            .trim()
            .toUpperCase();

      }


      console.log(
        "CLEAN SUBMITTED ANSWERS:",
        submittedAnswers
      );


      // -----------------------------------------------------
      // CALL BACKEND
      // -----------------------------------------------------

      const response =
        await submitQuiz(
          noteId,
          submittedAnswers
        );


      console.log(
        "Quiz submission response:",
        response
      );


      if (
        !response
      ) {

        throw new Error(
          "No response received from the server."
        );

      }


      /*
        notesApi.js returns response.data directly.

        Therefore:

        response.result

        is the correct path.
      */

      let result =
        response.result;


      /*
        Fallback for backend versions
        that return the result itself.
      */

      if (
        !result &&
        response.score_percentage !==
          undefined
      ) {

        result =
          response;

      }


      if (
        !result
      ) {

        console.error(
          "Invalid quiz result response:",
          response
        );


        throw new Error(
          "Quiz result was not received from the server."
        );

      }


      console.log(
        "Quiz result:",
        result
      );


      // =====================================================
      // NAVIGATE TO RESULT PAGE
      // =====================================================

      navigate(
        "/notes/" +
        noteId +
        "/quiz-result",
        {
          state: {

            noteId:
              noteId,

            quiz:
              quiz,

            answers:
              submittedAnswers,

            result:
              result

          }

        }
      );


    } catch (err) {

      console.error(
        "Submit quiz error:",
        err
      );


      setError(
        err &&
        err.message
          ? err.message
          : "Unable to submit the quiz."
      );


    } finally {

      setSubmitting(
        false
      );

    }

  }


  // =========================================================
  // ERROR BEFORE QUIZ
  // =========================================================

  if (
    error &&
    !quizStarted &&
    !generating
  ) {

    return (

      <div className="quiz-page">

        <AppHeader />


        <main className="quiz-main">

          <section className="quiz-error-card">

            <div className="quiz-error-icon">

              <XCircle
                size={25}
              />

            </div>


            <h1>
              Quiz unavailable
            </h1>


            <p>
              {error}
            </p>


            <div className="quiz-error-actions">

              <button
                type="button"
                onClick={
                  function () {

                    setError("");

                  }
                }
              >

                Try Again

              </button>


              <button
                type="button"
                className="quiz-secondary-action"
                onClick={
                  function () {

                    navigate(
                      "/notes/" +
                      noteId
                    );

                  }
                }
              >

                Back to Learning Hub

              </button>

            </div>

          </section>

        </main>

      </div>

    );

  }


  // =========================================================
  // PREFERENCE SCREEN
  // =========================================================

  if (
    !quizStarted &&
    !loading &&
    !generating
  ) {

    return (

      <div className="quiz-page">

        <AppHeader />


        <main className="quiz-main">


          <div className="quiz-topbar">

            <button
              type="button"
              className="quiz-back-button"
              onClick={
                function () {

                  navigate(
                    "/notes/" +
                    noteId
                  );

                }
              }
            >

              <ArrowLeft
                size={16}
              />

              Learning Hub

            </button>


            <div className="quiz-top-status">

              <Target
                size={14}
              />

              Personalized Quiz

            </div>

          </div>


          <section className="quiz-intro">

            <div className="quiz-intro-icon">

              <Brain
                size={26}
              />

            </div>


            <div className="quiz-intro-text">

              <div className="quiz-intro-badge">

                PERSONALIZED ASSESSMENT

              </div>


              <h1>
                Create your quiz.
              </h1>


              <p>

                Choose the difficulty and
                number of questions based
                on your learning preference.

              </p>

            </div>

          </section>


          <section className="quiz-question-panel">


            {/* =================================================
                STEP 1
            ================================================= */}

            <div className="quiz-question-top">

              <div>

                <span className="quiz-question-label">

                  STEP 1

                </span>


                <strong>

                  Choose difficulty

                </strong>

              </div>

            </div>


            <p
              style={{
                margin:
                  "12px 0 15px",

                color:
                  "#8799a2",

                fontSize:
                  "10px",

                lineHeight:
                  "1.5"
              }}
            >

              Select the level that
              matches your confidence
              and learning goal.

            </p>


            <div className="quiz-options">


              {/* BEGINNER */}

              <button
                type="button"
                className={
                  "quiz-answer-option " +
                  (
                    difficulty ===
                    "beginner"
                      ? "quiz-answer-option-selected"
                      : ""
                  )
                }
                onClick={
                  function () {

                    setDifficulty(
                      "beginner"
                    );

                  }
                }
              >

                <span
                  className={
                    "quiz-option-letter " +
                    (
                      difficulty ===
                      "beginner"
                        ? "quiz-option-letter-selected"
                        : ""
                    )
                  }
                >

                  B

                </span>


                <span className="quiz-option-text">

                  <strong>
                    Beginner
                  </strong>

                  <br />

                  Basic concepts,
                  definitions and
                  direct questions.

                </span>


                {difficulty ===
                "beginner" ? (

                  <span className="quiz-option-check quiz-option-check-visible">

                    <CheckCircle2
                      size={18}
                    />

                  </span>

                ) : null}

              </button>


              {/* INTERMEDIATE */}

              <button
                type="button"
                className={
                  "quiz-answer-option " +
                  (
                    difficulty ===
                    "intermediate"
                      ? "quiz-answer-option-selected"
                      : ""
                  )
                }
                onClick={
                  function () {

                    setDifficulty(
                      "intermediate"
                    );

                  }
                }
              >

                <span
                  className={
                    "quiz-option-letter " +
                    (
                      difficulty ===
                      "intermediate"
                        ? "quiz-option-letter-selected"
                        : ""
                    )
                  }
                >

                  I

                </span>


                <span className="quiz-option-text">

                  <strong>
                    Intermediate
                  </strong>

                  <br />

                  Understanding,
                  comparison and
                  basic application.

                </span>


                {difficulty ===
                "intermediate" ? (

                  <span className="quiz-option-check quiz-option-check-visible">

                    <CheckCircle2
                      size={18}
                    />

                  </span>

                ) : null}

              </button>


              {/* ADVANCED */}

              <button
                type="button"
                className={
                  "quiz-answer-option " +
                  (
                    difficulty ===
                    "advanced"
                      ? "quiz-answer-option-selected"
                      : ""
                  )
                }
                onClick={
                  function () {

                    setDifficulty(
                      "advanced"
                    );

                  }
                }
              >

                <span
                  className={
                    "quiz-option-letter " +
                    (
                      difficulty ===
                      "advanced"
                        ? "quiz-option-letter-selected"
                        : ""
                    )
                  }
                >

                  A

                </span>


                <span className="quiz-option-text">

                  <strong>
                    Advanced
                  </strong>

                  <br />

                  Reasoning,
                  analysis and
                  challenging application.

                </span>


                {difficulty ===
                "advanced" ? (

                  <span className="quiz-option-check quiz-option-check-visible">

                    <CheckCircle2
                      size={18}
                    />

                  </span>

                ) : null}

              </button>

            </div>


            {/* =================================================
                STEP 2
            ================================================= */}

            <div
              style={{
                marginTop:
                  "28px"
              }}
            >

              <div className="quiz-question-top">

                <div>

                  <span className="quiz-question-label">

                    STEP 2

                  </span>


                  <strong>

                    Number of questions

                  </strong>

                </div>

              </div>


              <p
                style={{
                  margin:
                    "10px 0 13px",

                  color:
                    "#8799a2",

                  fontSize:
                    "10px"
                }}
              >

                Choose how many questions
                you want to answer.

              </p>


              <div
                style={{
                  display:
                    "grid",

                  gridTemplateColumns:
                    "repeat(4, 1fr)",

                  gap:
                    "8px"
                }}
              >

                {[5, 10, 15, 20].map(
                  function (
                    count
                  ) {

                    return (

                      <button
                        type="button"
                        key={count}
                        className={
                          "quiz-number-button " +
                          (
                            questionCount ===
                            count
                              ? "quiz-number-active"
                              : ""
                          )
                        }
                        onClick={
                          function () {

                            setQuestionCount(
                              count
                            );

                          }
                        }
                      >

                        {count}

                      </button>

                    );

                  }
                )}

              </div>

            </div>


            {/* =================================================
                SUMMARY
            ================================================= */}

            <div
              className="quiz-submit-summary"
              style={{
                marginTop:
                  "22px"
              }}
            >

              <div>

                <span>
                  YOUR SELECTION
                </span>


                <h3>

                  {
                    difficulty
                      .charAt(0)
                      .toUpperCase() +
                    difficulty.slice(1)
                  }

                  {" · "}

                  {questionCount}

                  {" "}

                  Questions

                </h3>

              </div>


              <CheckCircle2
                size={20}
              />

            </div>


            {/* =================================================
                GENERATE BUTTON
            ================================================= */}

            <button
              type="button"
              className="quiz-navigation-next"
              style={{
                width:
                  "100%",

                marginLeft:
                  "0",

                marginTop:
                  "12px",

                minHeight:
                  "48px"
              }}
              onClick={
                handleGenerateQuiz
              }
              disabled={
                generating
              }
            >

              {generating
                ? "Creating Your Quiz..."
                : "Generate Quiz"}


              {generating ? (

                <Clock3
                  size={17}
                />

              ) : (

                <ArrowRight
                  size={17}
                />

              )}

            </button>


          </section>


          <div className="quiz-footer">

            SmartNotes AI ·
            Study Smarter,
            Recall Faster

          </div>

        </main>

      </div>

    );

  }


  // =========================================================
  // GENERATING
  // =========================================================

  if (
    loading &&
    !quizStarted
  ) {

    return (

      <div className="quiz-page">

        <AppHeader />


        <main className="quiz-main">

          <section className="quiz-loading-card">

            <div className="quiz-loading-icon">

              <Brain
                size={28}
              />

            </div>


            <div className="quiz-loading-badge">

              AI ASSESSMENT

            </div>


            <h1>
              Preparing your quiz...
            </h1>


            <p>

              SmartNotes AI is creating

              {" "}

              {questionCount}

              {" "}

              {
                difficulty
                  .charAt(0)
                  .toUpperCase() +
                difficulty.slice(1)
              }

              {" "}
              questions from your
              study material.

            </p>


            <div className="quiz-loading-lines">

              <span></span>
              <span></span>
              <span></span>
              <span></span>

            </div>

          </section>

        </main>

      </div>

    );

  }


  // =========================================================
  // SAFETY CHECK
  // =========================================================

  if (
    !currentQuestion
  ) {

    return (

      <div className="quiz-page">

        <AppHeader />


        <main className="quiz-main">

          <section className="quiz-error-card">

            <div className="quiz-error-icon">

              <XCircle
                size={25}
              />

            </div>


            <h1>
              Quiz unavailable
            </h1>


            <p>
              The generated quiz could
              not be displayed.
            </p>


            <div className="quiz-error-actions">

              <button
                type="button"
                onClick={
                  function () {

                    setQuizStarted(
                      false
                    );

                    setQuiz([]);

                    setAnswers({});

                  }
                }
              >

                Create Again

              </button>


              <button
                type="button"
                className="quiz-secondary-action"
                onClick={
                  function () {

                    navigate(
                      "/notes/" +
                      noteId
                    );

                  }
                }
              >

                Back to Learning Hub

              </button>

            </div>

          </section>

        </main>

      </div>

    );

  }


  // =========================================================
  // ACTUAL QUIZ
  // =========================================================

  const currentAnswer =
    answers[
      String(
        currentIndex + 1
      )
    ] || "";


  return (

    <div className="quiz-page">

      <AppHeader />


      <main className="quiz-main">


        {/* =================================================
            TOP BAR
        ================================================= */}

        <div className="quiz-topbar">

          <button
            type="button"
            className="quiz-back-button"
            onClick={
              function () {

                navigate(
                  "/notes/" +
                  noteId
                );

              }
            }
          >

            <ArrowLeft
              size={16}
            />

            Learning Hub

          </button>


          <div className="quiz-top-status">

            <Target
              size={14}
            />

            {
              difficulty
                .charAt(0)
                .toUpperCase() +
              difficulty.slice(1)
            }

            {" · "}

            {quiz.length}

            {" "}

            Questions

          </div>

        </div>


        {/* =================================================
            INTRO
        ================================================= */}

        <section className="quiz-intro">

          <div className="quiz-intro-icon">

            <Trophy
              size={25}
            />

          </div>


          <div className="quiz-intro-text">

            <div className="quiz-intro-badge">

              AI GENERATED QUIZ

            </div>


            <h1>
              Test what you know.
            </h1>


            <p>

              Answer each question based
              on the study material you
              uploaded.

            </p>

          </div>

        </section>


        {/* =================================================
            STATS
        ================================================= */}

        <section className="quiz-stats-bar">


          <div className="quiz-stat">

            <div className="quiz-stat-icon">

              <FileText
                size={15}
              />

            </div>


            <div>

              <span>
                QUESTIONS
              </span>

              <strong>
                {quiz.length}
              </strong>

            </div>

          </div>


          <div className="quiz-stat">

            <div className="quiz-stat-icon">

              <CheckCircle2
                size={15}
              />

            </div>


            <div>

              <span>
                ANSWERED
              </span>

              <strong>
                {answeredCount}
              </strong>

            </div>

          </div>


          <div className="quiz-stat">

            <div className="quiz-stat-icon">

              <HelpCircle
                size={15}
              />

            </div>


            <div>

              <span>
                REMAINING
              </span>

              <strong>
                {unansweredCount}
              </strong>

            </div>

          </div>


          <div
            className={
              "quiz-stat quiz-timer-stat " +
              (
                timeLeft <= 60
                  ? "quiz-timer-warning"
                  : ""
              )
            }
          >

            <div className="quiz-stat-icon">

              <Clock3
                size={15}
              />

            </div>


            <div>

              <span>
                TIME
              </span>

              <strong>
                {formattedTime}
              </strong>

            </div>

          </div>


        </section>


        {/* =================================================
            OVERALL PROGRESS
        ================================================= */}

        <section className="quiz-overall-progress">

          <div className="quiz-progress-label">

            <span>
              QUIZ PROGRESS
            </span>


            <strong>

              {
                Math.round(
                  overallProgress
                )
              }

              %

            </strong>

          </div>


          <div className="quiz-progress-track">

            <div
              className="quiz-progress-bar"
              style={{
                width:
                  overallProgress +
                  "%"
              }}
            ></div>

          </div>

        </section>


        {/* =================================================
            LAYOUT
        ================================================= */}

        <div className="quiz-layout">


          {/* =================================================
              QUESTION PANEL
          ================================================= */}

          <section className="quiz-question-panel">


            <div className="quiz-question-top">

              <div>

                <span className="quiz-question-label">

                  QUESTION

                </span>


                <strong>

                  {currentIndex + 1}

                  <span>

                    {" "}

                    / {quiz.length}

                  </span>

                </strong>

              </div>


              <div className="quiz-question-tags">

                <span className="quiz-concept-tag">

                  <Brain
                    size={11}
                  />

                  {currentQuestion.concept}

                </span>


                <span className="quiz-difficulty-tag">

                  {currentQuestion.difficulty}

                </span>

              </div>

            </div>


            {/* =================================================
                QUESTION PROGRESS
            ================================================= */}

            <div className="quiz-question-progress">

              <div
                style={{
                  width:
                    quizProgress +
                    "%"
                }}
              ></div>

            </div>


            {/* =================================================
                QUESTION
            ================================================= */}

            <h2 className="quiz-question-text">

              {
                currentQuestion.question
                  .replace(
                    /^#+\s*/,
                    ""
                  )
              }

            </h2>


            {/* =================================================
                INSTRUCTION
            ================================================= */}

            <div className="quiz-answer-instruction">

              <HelpCircle
                size={14}
              />

              Choose the best answer

            </div>


            {/* =================================================
                OPTIONS
            ================================================= */}

            <div className="quiz-options">

              {currentQuestion.options.map(
                function (
                  option
                ) {

                  const selected =
                    currentAnswer ===
                    option.letter;


                  return (

                    <button
                      type="button"
                      key={
                        option.letter
                      }
                      className={
                        "quiz-answer-option " +
                        (
                          selected
                            ? "quiz-answer-option-selected"
                            : ""
                        )
                      }
                      onClick={
                        function () {

                          selectAnswer(
                            option.letter
                          );

                        }
                      }
                    >

                      <span
                        className={
                          "quiz-option-letter " +
                          (
                            selected
                              ? "quiz-option-letter-selected"
                              : ""
                          )
                        }
                      >

                        {
                          option.letter
                        }

                      </span>


                      <span className="quiz-option-text">

                        {
                          option.text
                        }

                      </span>


                      <span
                        className={
                          "quiz-option-check " +
                          (
                            selected
                              ? "quiz-option-check-visible"
                              : ""
                          )
                        }
                      >

                        <CheckCircle2
                          size={18}
                        />

                      </span>

                    </button>

                  );

                }
              )}

            </div>


            {/* =================================================
                NAVIGATION
            ================================================= */}

            <div className="quiz-question-navigation">


              <button
                type="button"
                className="quiz-navigation-secondary"
                onClick={
                  goPrevious
                }
                disabled={
                  currentIndex === 0
                }
              >

                <ArrowLeft
                  size={16}
                />

                Previous

              </button>


              {currentIndex <
              quiz.length - 1 ? (

                <button
                  type="button"
                  className="quiz-navigation-next"
                  onClick={
                    goNext
                  }
                >

                  Next Question

                  <ArrowRight
                    size={16}
                  />

                </button>

              ) : (

                <button
                  type="button"
                  className="quiz-navigation-submit"
                  onClick={
                    handleSubmit
                  }
                  disabled={
                    submitting
                  }
                >

                  {
                    submitting
                      ? "Submitting..."
                      : "Submit Quiz"
                  }


                  <Trophy
                    size={16}
                  />

                </button>

              )}

            </div>

          </section>


          {/* =================================================
              QUESTION NAVIGATOR
          ================================================= */}

          <aside className="quiz-navigator">


            <div className="quiz-navigator-header">

              <div>

                <span>
                  QUESTIONS
                </span>


                <h2>
                  Your progress
                </h2>

              </div>


              <Flag
                size={18}
              />

            </div>


            <div className="quiz-navigator-grid">

              {quiz.map(
                function (
                  _,
                  index
                ) {

                  const number =
                    index + 1;


                  const answer =
                    answers[
                      String(number)
                    ];


                  const answered =
                    answer !== undefined &&
                    answer !== null &&
                    String(
                      answer
                    ).trim() !== "";


                  const active =
                    currentIndex ===
                    index;


                  return (

                    <button
                      type="button"
                      key={number}
                      className={
                        "quiz-number-button " +
                        (
                          active
                            ? "quiz-number-active "
                            : ""
                        ) +
                        (
                          answered
                            ? "quiz-number-answered"
                            : ""
                        )
                      }
                      onClick={
                        function () {

                          goToQuestion(
                            index
                          );

                        }
                      }
                    >

                      {number}

                    </button>

                  );

                }
              )}

            </div>


            <div className="quiz-navigator-legend">

              <div>

                <span className="legend-dot legend-active"></span>

                Current

              </div>


              <div>

                <span className="legend-dot legend-answered"></span>

                Answered

              </div>


              <div>

                <span className="legend-dot legend-pending"></span>

                Pending

              </div>

            </div>


            <div className="quiz-navigator-tip">

              <Target
                size={16}
              />

              <p>

                Don't rush.
                Read every option
                carefully before
                choosing.

              </p>

            </div>

          </aside>

        </div>


        {/* =================================================
            SUBMIT SUMMARY
        ================================================= */}

        <section className="quiz-submit-summary">

          <div>

            <span>
              READY TO FINISH?
            </span>


            <h3>

              {answeredCount}

              {" of "}

              {quiz.length}

              {" questions answered"}

            </h3>

          </div>


          <button
            type="button"
            onClick={
              handleSubmit
            }
            disabled={
              submitting
            }
          >

            {
              submitting
                ? "Submitting..."
                : "Submit Quiz"
            }


            <ArrowRight
              size={16}
            />

          </button>

        </section>


        {/* =================================================
            INLINE ERROR
        ================================================= */}

        {error && (

          <div
            className="quiz-inline-error"
            style={{
              marginTop:
                "15px"
            }}
          >

            <XCircle
              size={16}
            />

            {error}

          </div>

        )}


        <div className="quiz-footer">

          SmartNotes AI ·
          Study Smarter,
          Recall Faster

        </div>

      </main>

    </div>

  );

}


export default Quiz;
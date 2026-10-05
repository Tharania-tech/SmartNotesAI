import React, {
  useEffect,
  useRef,
  useState
} from "react";

import {
  ArrowLeft,
  BookOpen,
  Bot,
  Brain,
  Check,
  Copy,
  Loader2,
  MessageCircle,
  RotateCcw,
  Send,
  Sparkles,
  User,
  X
} from "lucide-react";

import {
  useNavigate,
  useParams
} from "react-router-dom";

import AppHeader from "../components/AppHeader";
import { chatWithNote } from "../services/notesApi";


export default function Chat() {

  const navigate = useNavigate();

  const { noteId } = useParams();

  const messagesEndRef = useRef(null);

  const inputRef = useRef(null);

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [copiedIndex, setCopiedIndex] = useState(null);


  // =======================================================
  // SCROLL TO BOTTOM
  // =======================================================

  useEffect(
    function () {

      if (messagesEndRef.current) {

        messagesEndRef.current.scrollIntoView({
          behavior: "smooth"
        });

      }

    },
    [messages]
  );


  // =======================================================
  // FOCUS INPUT
  // =======================================================

  useEffect(
    function () {

      if (inputRef.current) {

        inputRef.current.focus();

      }

    },
    []
  );


  // =======================================================
  // EXTRACT RESPONSE DATA
  // =======================================================

  function getResponseData(response) {

    if (!response) {
      return {};
    }

    /*
      Your notesApi.js returns:

      response.data

      Therefore Chat.jsx receives:

      {
        message: "...",
        note_id: "...",
        question: "...",
        answer: "...",
        relevant_context: [...]
      }

      So the answer is directly:

      response.answer
    */

    if (
      typeof response === "object" &&
      response.answer !== undefined
    ) {
      return response;
    }


    /*
      This is an additional fallback in case
      axios data is returned directly later.
    */

    if (
      response.data &&
      typeof response.data === "object"
    ) {
      return response.data;
    }


    return {};
  }


  // =======================================================
  // CLEAN ANSWER
  // =======================================================

  function cleanAnswer(answer) {

    if (
      answer === null ||
      answer === undefined
    ) {
      return "";
    }

    let text = String(answer);

    text = text.replace(
      /\r\n/g,
      "\n"
    );

    text = text.replace(
      /\n{3,}/g,
      "\n\n"
    );

    return text.trim();
  }


  // =======================================================
  // ASK QUESTION
  // =======================================================

  async function handleSendQuestion(event) {

    if (event) {
      event.preventDefault();
    }


    const trimmedQuestion =
      question.trim();


    if (!trimmedQuestion) {
      return;
    }


    if (loading) {
      return;
    }


    if (!noteId) {

      setError(
        "Note ID is missing."
      );

      return;
    }


    // Clear previous error

    setError("");


    // -----------------------------------------------------
    // ADD USER MESSAGE
    // -----------------------------------------------------

    const userMessage = {
      role: "user",
      content: trimmedQuestion
    };


    setMessages(
      function (previousMessages) {

        return [
          ...previousMessages,
          userMessage
        ];

      }
    );


    // Clear input

    setQuestion("");

    setLoading(true);


    try {

      console.log(
        "========================================"
      );

      console.log(
        "SMARTNOTES AI FRONTEND CHAT"
      );

      console.log(
        "Question:",
        trimmedQuestion
      );


      // ---------------------------------------------------
      // CALL BACKEND
      // ---------------------------------------------------

      const response =
        await chatWithNote(
          noteId,
          trimmedQuestion
        );


      console.log(
        "FULL CHAT RESPONSE:",
        response
      );


      // ---------------------------------------------------
      // GET RESPONSE DATA
      // ---------------------------------------------------

      const data =
        getResponseData(
          response
        );


      console.log(
        "CHAT RESPONSE DATA:",
        data
      );


      // ---------------------------------------------------
      // GET GENERATED ANSWER
      // ---------------------------------------------------

      let answer = "";


      if (
        data &&
        typeof data.answer === "string"
      ) {

        answer =
          cleanAnswer(
            data.answer
          );

      }


      // ---------------------------------------------------
      // EXTRA FALLBACK
      // ---------------------------------------------------

      if (
        !answer &&
        response &&
        typeof response.answer === "string"
      ) {

        answer =
          cleanAnswer(
            response.answer
          );

      }


      // ---------------------------------------------------
      // HANDLE EMPTY ANSWER
      // ---------------------------------------------------

      if (!answer) {

        answer =
          "I could not generate an answer from your uploaded notes.";

      }


      // ---------------------------------------------------
      // GET RELEVANT CONTEXT
      // ---------------------------------------------------

      let context = "";


      if (
        data &&
        data.relevant_context
      ) {

        if (
          Array.isArray(
            data.relevant_context
          )
        ) {

          context =
            data.relevant_context.join(
              "\n\n"
            );

        } else {

          context =
            String(
              data.relevant_context
            );

        }

      }


      // ---------------------------------------------------
      // CREATE AI MESSAGE
      // ---------------------------------------------------

      const assistantMessage = {
        role: "assistant",
        content: answer,
        relevantContext: context
      };


      // ---------------------------------------------------
      // DISPLAY AI ANSWER
      // ---------------------------------------------------

      setMessages(
        function (previousMessages) {

          return [
            ...previousMessages,
            assistantMessage
          ];

        }
      );


      console.log(
        "Answer successfully received from backend."
      );

      console.log(
        "Answer length:",
        answer.length
      );

      console.log(
        "========================================"
      );


    } catch (error) {

      console.error(
        "Chat error:",
        error
      );


      let message =
        "Unable to connect to the AI tutor.";


      if (
        error &&
        error.message
      ) {

        message =
          error.message;

      }


      setError(
        message
      );


      // ---------------------------------------------------
      // DISPLAY FRIENDLY ERROR MESSAGE
      // ---------------------------------------------------

      setMessages(
        function (previousMessages) {

          return [
            ...previousMessages,
            {
              role: "assistant",
              content:
                "I couldn't generate an answer right now. Please try asking the question again."
            }
          ];

        }
      );


    } finally {

      setLoading(false);


      setTimeout(
        function () {

          if (inputRef.current) {

            inputRef.current.focus();

          }

        },
        100
      );

    }

  }


  // =======================================================
  // ENTER KEY
  // =======================================================

  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      handleSendQuestion(
        event
      );

    }

  }


  // =======================================================
  // COPY ANSWER
  // =======================================================

  async function handleCopy(
    text,
    index
  ) {

    try {

      await navigator.clipboard.writeText(
        text
      );


      setCopiedIndex(
        index
      );


      setTimeout(
        function () {

          setCopiedIndex(
            null
          );

        },
        1600
      );


    } catch (error) {

      console.error(
        "Copy error:",
        error
      );

    }

  }


  // =======================================================
  // QUICK QUESTION
  // =======================================================

  function handleQuickQuestion(
    text
  ) {

    setQuestion(
      text
    );


    setTimeout(
      function () {

        if (inputRef.current) {

          inputRef.current.focus();

        }

      },
      50
    );

  }


  // =======================================================
  // CLEAR CHAT
  // =======================================================

  function handleClearChat() {

    setMessages([]);

    setError("");

    setQuestion("");


    setTimeout(
      function () {

        if (inputRef.current) {

          inputRef.current.focus();

        }

      },
      100
    );

  }


  // =======================================================
  // BACK
  // =======================================================

  function handleBack() {

    navigate(
      "/notes/" + noteId
    );

  }


  // =======================================================
  // QUICK QUESTIONS
  // =======================================================

  const quickQuestions = [
    "Explain this topic in simple words.",
    "What are the most important concepts?",
    "Give me an example.",
    "What should I remember for an exam?"
  ];


  // =======================================================
  // RENDER
  // =======================================================

  return (

    <div className="chat-page">

      <AppHeader />


      <main className="chat-main">

        {/* =================================================
            TOP BAR
        ================================================= */}

        <div className="chat-topbar">

          <button
            type="button"
            className="chat-back-button"
            onClick={
              handleBack
            }
          >

            <ArrowLeft size={18} />

            Learning Hub

          </button>


          <div className="chat-top-status">

            <span className="chat-live-dot"></span>

            AI Tutor

          </div>

        </div>


        {/* =================================================
            WELCOME HERO
        ================================================= */}

        {messages.length === 0 && (

          <section className="chat-welcome">

            <div className="chat-welcome-icon">

              <div className="chat-welcome-icon-glow"></div>

              <Brain size={31} />

            </div>


            <div className="chat-welcome-badge">

              <Sparkles size={14} />

              SmartNotes AI Tutor

            </div>


            <h1>
              Ask your notes anything.
            </h1>


            <p>
              Learn from your uploaded notes with
              an AI tutor that explains concepts,
              answers questions, and helps you revise.
            </p>

          </section>

        )}


        {/* =================================================
            CHAT CONTAINER
        ================================================= */}

        <section className="chat-card">


          {/* =================================================
              CHAT HEADER
          ================================================= */}

          <div className="chat-card-header">

            <div className="chat-card-header-left">

              <div className="chat-bot-avatar">

                <Bot size={19} />

              </div>


              <div>

                <h2>
                  SmartNotes Tutor
                </h2>


                <span>
                  Answers based on your uploaded notes
                </span>

              </div>

            </div>


            {messages.length > 0 && (

              <button
                type="button"
                className="chat-clear-button"
                onClick={
                  handleClearChat
                }
              >

                <RotateCcw size={15} />

                New Chat

              </button>

            )}

          </div>


          {/* =================================================
              QUICK QUESTIONS
          ================================================= */}

          {messages.length === 0 && (

            <div className="chat-quick-section">

              <span className="chat-quick-label">

                Try asking

              </span>


              <div className="chat-quick-list">

                {quickQuestions.map(
                  function (item, index) {

                    return (

                      <button
                        type="button"
                        className="chat-quick-question"
                        key={index}
                        onClick={
                          function () {

                            handleQuickQuestion(
                              item
                            );

                          }
                        }
                      >

                        <MessageCircle size={14} />

                        {item}

                      </button>

                    );

                  }
                )}

              </div>

            </div>

          )}


          {/* =================================================
              MESSAGES
          ================================================= */}

          <div className="chat-messages">

            {messages.map(
              function (message, index) {

                const isUser =
                  message.role === "user";


                return (

                  <div
                    className={
                      "chat-message-row " +
                      (
                        isUser
                          ? "chat-message-user"
                          : "chat-message-assistant"
                      )
                    }
                    key={index}
                  >


                    {!isUser && (

                      <div className="chat-message-avatar assistant-avatar">

                        <Bot size={16} />

                      </div>

                    )}


                    <div className="chat-message-content">


                      <div
                        className={
                          isUser
                            ? "chat-message-bubble user-bubble"
                            : "chat-message-bubble assistant-bubble"
                        }
                      >

                        <div className="chat-message-text">

                          {message.content}

                        </div>

                      </div>


                      {!isUser && (

                        <div className="chat-message-actions">

                          <button
                            type="button"
                            onClick={
                              function () {

                                handleCopy(
                                  message.content,
                                  index
                                );

                              }
                            }
                          >

                            {copiedIndex === index ? (

                              <>

                                <Check size={13} />

                                Copied

                              </>

                            ) : (

                              <>

                                <Copy size={13} />

                                Copy

                              </>

                            )}

                          </button>

                        </div>

                      )}

                    </div>


                    {isUser && (

                      <div className="chat-message-avatar user-avatar">

                        <User size={16} />

                      </div>

                    )}

                  </div>

                );

              }
            )}


            {/* =================================================
                AI THINKING
            ================================================= */}

            {loading && (

              <div className="chat-message-row chat-message-assistant">

                <div className="chat-message-avatar assistant-avatar">

                  <Bot size={16} />

                </div>


                <div className="chat-message-content">

                  <div className="chat-message-bubble assistant-bubble">

                    <div className="chat-thinking">

                      <span>
                        Thinking
                      </span>

                      <span className="chat-thinking-dot"></span>

                      <span className="chat-thinking-dot"></span>

                      <span className="chat-thinking-dot"></span>

                    </div>

                  </div>

                </div>

              </div>

            )}


            <div
              ref={messagesEndRef}
              className="chat-scroll-anchor"
            />

          </div>


          {/* =================================================
              ERROR
          ================================================= */}

          {error && (

            <div className="chat-error">

              <div className="chat-error-icon">

                <X size={15} />

              </div>


              <span>
                {error}
              </span>

            </div>

          )}


          {/* =================================================
              INPUT
          ================================================= */}

          <form
            className="chat-input-area"
            onSubmit={
              handleSendQuestion
            }
          >

            <textarea
              ref={inputRef}
              value={question}
              onChange={
                function (event) {

                  setQuestion(
                    event.target.value
                  );

                }
              }
              onKeyDown={
                handleKeyDown
              }
              placeholder="Ask something about your notes..."
              rows={1}
              disabled={loading}
            />


            <button
              type="submit"
              className="chat-send-button"
              disabled={
                loading ||
                !question.trim()
              }
            >

              {loading ? (

                <Loader2
                  size={19}
                  className="chat-spinner"
                />

              ) : (

                <Send size={19} />

              )}

            </button>

          </form>


          <div className="chat-input-hint">

            <span>
              Press Enter to send
            </span>

            <span>
              Shift + Enter for a new line
            </span>

          </div>

        </section>


        {/* =================================================
            STUDY SUPPORT
        ================================================= */}

        <section className="chat-support">


          <div className="chat-support-item">

            <div className="chat-support-icon">

              <BookOpen size={18} />

            </div>


            <div>

              <strong>
                Based on your notes
              </strong>

              <span>
                Ask questions directly from the uploaded material.
              </span>

            </div>

          </div>


          <div className="chat-support-item">

            <div className="chat-support-icon">

              <Sparkles size={18} />

            </div>


            <div>

              <strong>
                Learn in simple language
              </strong>

              <span>
                Ask the tutor to simplify difficult concepts.
              </span>

            </div>

          </div>


          <div className="chat-support-item">

            <div className="chat-support-icon">

              <Brain size={18} />

            </div>


            <div>

              <strong>
                Prepare for exams
              </strong>

              <span>
                Ask for important points, examples, and revision help.
              </span>

            </div>

          </div>


        </section>


        {/* =================================================
            FOOTER
        ================================================= */}

        <div className="chat-footer">

          <span>
            SmartNotes AI
          </span>

          <span>
            Study Smarter, Recall Faster
          </span>

        </div>


      </main>

    </div>
  );
}
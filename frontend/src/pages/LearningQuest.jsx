import React, {
  useEffect,
  useState
} from "react";

import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Brain,
  Check,
  CheckCircle2,
  Clock3,
  Flame,
  Layers3,
  MessageCircle,
  ShieldCheck,
  Sparkles,
  Target,
  Trophy,
  Zap
} from "lucide-react";

import {
  useLocation,
  useNavigate
} from "react-router-dom";

import AppHeader from "../components/AppHeader";


import "./LearningQuest.css";


export default function LearningQuest() {

  const navigate = useNavigate();

  const location = useLocation();

  const state =
    location.state || {};


  /* =========================================================
     DATA FROM WEAK TOPICS PAGE
     ========================================================= */

  const noteId =
    state.noteId || "";

  const incomingWeakTopics =
    Array.isArray(state.weakTopics)
      ? state.weakTopics
      : [];

  const quiz =
    Array.isArray(state.quiz)
      ? state.quiz
      : [];

  const result =
    state.result || {};


  /* =========================================================
     CHOOSE QUEST TOPIC
     ========================================================= */

  let mainTopic =
    "Your Learning Goal";


  if (
    incomingWeakTopics.length > 0 &&
    incomingWeakTopics[0]
  ) {

    if (
      incomingWeakTopics[0].concept
    ) {

      mainTopic =
        incomingWeakTopics[0].concept;

    } else {

      mainTopic =
        String(
          incomingWeakTopics[0]
        );

    }

  }


  /* =========================================================
     BUILD MISSIONS
     ========================================================= */

  function createMissions(topic) {

    return [

      {
        id: "mission-1",

        title:
          "Understand the topic",

        description:
          "Read the AI-generated summary and build a clear understanding of " +
          topic + ".",

        xp: 20,

        icon: BookOpen,

        action:
          "Read Summary",

        type:
          "summary"

      },


      {
        id: "mission-2",

        title:
          "Strengthen your memory",

        description:
          "Review your flashcards and recall the important ideas from " +
          topic + ".",

        xp: 20,

        icon: Layers3,

        action:
          "Review Flashcards",

        type:
          "flashcards"

      },


      {
        id: "mission-3",

        title:
          "Practice the concept",

        description:
          "Test your understanding with a short AI-generated quiz.",

        xp: 30,

        icon: Brain,

        action:
          "Practice Quiz",

        type:
          "quiz"

      },


      {
        id: "mission-4",

        title:
          "Ask the AI Tutor",

        description:
          "Ask SmartNotes Tutor to explain anything you still find difficult.",

        xp: 15,

        icon: MessageCircle,

        action:
          "Ask AI Tutor",

        type:
          "tutor"

      },


      {
        id: "mission-5",

        title:
          "Final Challenge",

        description:
          "Take another quiz and prove that you have improved " +
          topic + ".",

        xp: 50,

        icon: Trophy,

        action:
          "Take Final Quiz",

        type:
          "final"

      }

    ];

  }


  const [missions] =
    useState(
      createMissions(
        mainTopic
      )
    );


  /* =========================================================
     PROGRESS STATE
     ========================================================= */

  const storageKey =
    "smartnotes-quest-" +
    (
      noteId ||
      "general"
    );


  const [completedMissions, setCompletedMissions] =
    useState([]);


  const [xp, setXp] =
    useState(0);


  const [streak, setStreak] =
    useState(1);


  /* =========================================================
     LOAD SAVED QUEST
     ========================================================= */

  useEffect(
    function() {

      try {

        const saved =
          localStorage.getItem(
            storageKey
          );


        if (!saved) {
          return;
        }


        const parsed =
          JSON.parse(
            saved
          );


        if (
          parsed.completedMissions &&
          Array.isArray(
            parsed.completedMissions
          )
        ) {

          setCompletedMissions(
            parsed.completedMissions
          );

        }


        if (
          parsed.xp !== undefined
        ) {

          setXp(
            Number(
              parsed.xp
            )
          );

        }


        if (
          parsed.streak !== undefined
        ) {

          setStreak(
            Number(
              parsed.streak
            )
          );

        }

      } catch (error) {

        console.error(
          "Unable to load saved quest:",
          error
        );

      }

    },
    [storageKey]
  );


  /* =========================================================
     SAVE QUEST
     ========================================================= */

  useEffect(
    function() {

      try {

        const questData = {

          completedMissions:
            completedMissions,

          xp:
            xp,

          streak:
            streak

        };


        localStorage.setItem(
          storageKey,
          JSON.stringify(
            questData
          )
        );

      } catch (error) {

        console.error(
          "Unable to save quest:",
          error
        );

      }

    },
    [
      completedMissions,
      xp,
      streak,
      storageKey
    ]
  );


  /* =========================================================
     CALCULATE PROGRESS
     ========================================================= */

  const completedCount =
    completedMissions.length;


  const totalMissions =
    missions.length;


  const progress =
    totalMissions > 0
      ? Math.round(
          (
            completedCount /
            totalMissions
          ) * 100
        )
      : 0;


  const totalPossibleXp =
    missions.reduce(
      function(
        total,
        mission
      ) {

        return (
          total +
          mission.xp
        );

      },
      0
    );


  const level =
    Math.floor(
      xp / 100
    ) + 1;


  const xpIntoLevel =
    xp % 100;


  const xpToNextLevel =
    100 -
    xpIntoLevel;


  const questComplete =
    completedCount ===
    totalMissions;


  /* =========================================================
     COMPLETE MISSION
     ========================================================= */

  function completeMission(
    mission
  ) {

    if (
      completedMissions.includes(
        mission.id
      )
    ) {

      return;

    }


    setCompletedMissions(
      function(previous) {

        return [
          ...previous,
          mission.id
        ];

      }
    );


    setXp(
      function(previousXp) {

        return (
          previousXp +
          mission.xp
        );

      }
    );

  }


  /* =========================================================
     MISSION ACTION
     ========================================================= */

  function handleMissionAction(
    mission
  ) {

    if (
      completedMissions.includes(
        mission.id
      )
    ) {

      return;

    }


    if (
      mission.type === "summary"
    ) {

      if (noteId) {

        navigate(
          "/notes/" +
          noteId +
          "/summary"
        );

      }

      return;

    }


    if (
      mission.type === "flashcards"
    ) {

      if (noteId) {

        navigate(
          "/notes/" +
          noteId +
          "/flashcards"
        );

      }

      return;

    }


    if (
      mission.type === "quiz"
    ) {

      if (noteId) {

        navigate(
          "/notes/" +
          noteId +
          "/quiz"
        );

      }

      return;

    }


    if (
      mission.type === "tutor"
    ) {

      if (noteId) {

        navigate(
          "/notes/" +
          noteId +
          "/chat"
        );

      }

      return;

    }


    if (
      mission.type === "final"
    ) {

      if (noteId) {

        navigate(
          "/notes/" +
          noteId +
          "/quiz"
        );

      }

      return;

    }

  }


  /* =========================================================
     RESET QUEST
     ========================================================= */

  function resetQuest() {

    setCompletedMissions([]);

    setXp(0);

    setStreak(1);

    localStorage.removeItem(
      storageKey
    );

  }


  /* =========================================================
     BACK
     ========================================================= */

  function handleBack() {

    if (noteId) {

      navigate(
        "/weak-topics",
        {
          state: {
            noteId:
              noteId,

            quiz:
              quiz,

            result:
              result,

            weakTopics:
              incomingWeakTopics
          }
        }
      );

      return;

    }


    navigate(
      "/dashboard"
    );

  }


  /* =========================================================
     RENDER
     ========================================================= */

  return (

    <div className="learning-quest-page">

      <AppHeader />


      <main className="learning-quest-container">


        {/* =================================================
            TOP BAR
        ================================================= */}

        <div className="quest-topbar">

          <button
            type="button"
            className="quest-back-button"
            onClick={handleBack}
          >

            <ArrowLeft size={16} />

            Weak Topics

          </button>


          <div className="quest-top-status">

            <Sparkles size={14} />

            Learning Quest

          </div>

        </div>


        {/* =================================================
            HERO
        ================================================= */}

        <section className="quest-hero">

          <div className="quest-hero-content">

            <div className="quest-hero-badge">

              <Target size={13} />

              CURRENT QUEST

            </div>


            <h1>
              Master {mainTopic}
            </h1>


            <p>
              Turn your weak topic into a strength
              by completing each learning mission.
            </p>


            <div className="quest-hero-meta">

              <span>

                <Flame size={14} />

                {streak} Day Streak

              </span>


              <span>

                <Zap size={14} />

                {xp} XP

              </span>


              <span>

                <Trophy size={14} />

                Level {level}

              </span>

            </div>

          </div>


          <div className="quest-hero-target">

            <div className="quest-target-circle">

              <Target size={28} />

            </div>


            <span>
              QUEST PROGRESS
            </span>


            <strong>
              {progress}%
            </strong>

          </div>

        </section>


        {/* =================================================
            PROGRESS CARD
        ================================================= */}

        <section className="quest-progress-card">

          <div className="quest-progress-header">

            <div>

              <span>
                YOUR JOURNEY
              </span>

              <h2>
                Keep moving toward your goal
              </h2>

            </div>


            <div className="quest-progress-xp">

              <Zap size={15} />

              <strong>
                {xp}
              </strong>

              <span>
                / {totalPossibleXp} XP
              </span>

            </div>

          </div>


          <div className="quest-progress-track">

            <span
              style={{
                width:
                  progress + "%"
              }}
            ></span>

          </div>


          <div className="quest-progress-footer">

            <span>
              {completedCount} of {totalMissions} missions completed
            </span>


            <span>
              {xpToNextLevel} XP to Level {level + 1}
            </span>

          </div>

        </section>


        {/* =================================================
            MAIN GRID
        ================================================= */}

        <section className="quest-main-grid">


          {/* =================================================
              MISSIONS
          ================================================= */}

          <div className="quest-missions-card">

            <div className="quest-section-heading">

              <div>

                <span>
                  TODAY'S MISSIONS
                </span>

                <h2>
                  Complete your learning path
                </h2>

              </div>


              <div className="quest-mission-count">

                {completedCount}
                /
                {totalMissions}

              </div>

            </div>


            <div className="quest-mission-list">

              {missions.map(
                function(
                  mission,
                  index
                ) {

                  const MissionIcon =
                    mission.icon;


                  const completed =
                    completedMissions.includes(
                      mission.id
                    );


                  return (

                    <div
                      className={
                        completed
                          ? "quest-mission completed"
                          : "quest-mission"
                      }
                      key={
                        mission.id
                      }
                    >


                      {/* NUMBER */}

                      <div className="quest-mission-number">

                        {completed ? (

                          <Check size={17} />

                        ) : (

                          index + 1

                        )}

                      </div>


                      {/* ICON */}

                      <div className="quest-mission-icon">

                        <MissionIcon size={19} />

                      </div>


                      {/* CONTENT */}

                      <div className="quest-mission-content">

                        <div className="quest-mission-title">

                          <strong>
                            {mission.title}
                          </strong>


                          {completed && (

                            <span>
                              Completed
                            </span>

                          )}

                        </div>


                        <p>
                          {mission.description}
                        </p>


                        <div className="quest-mission-bottom">

                          <span className="quest-xp">

                            <Zap size={11} />

                            +{mission.xp} XP

                          </span>

                        </div>

                      </div>


                      {/* ACTION */}

                      {!completed ? (

                        <button
                          type="button"
                          className="quest-mission-button"
                          onClick={function() {

                            handleMissionAction(
                              mission
                            );

                            completeMission(
                              mission
                            );

                          }}
                        >

                          {mission.action}

                          <ArrowRight size={14} />

                        </button>

                      ) : (

                        <div className="quest-completed-check">

                          <CheckCircle2 size={19} />

                        </div>

                      )}

                    </div>

                  );

                }
              )}

            </div>

          </div>


          {/* =================================================
              QUEST SIDEBAR
          ================================================= */}

          <aside className="quest-sidebar">


            {/* LEVEL CARD */}

            <div className="quest-level-card">

              <div className="quest-level-header">

                <div className="quest-level-icon">

                  <Trophy size={20} />

                </div>


                <div>

                  <span>
                    YOUR LEVEL
                  </span>

                  <strong>
                    Level {level}
                  </strong>

                </div>

              </div>


              <div className="quest-level-progress">

                <div>

                  <span>
                    {xpIntoLevel} / 100 XP
                  </span>

                  <strong>
                    {100 - xpIntoLevel}%
                  </strong>

                </div>


                <div className="quest-level-track">

                  <span
                    style={{
                      width:
                        xpIntoLevel + "%"
                    }}
                  ></span>

                </div>

              </div>


              <p>
                Complete missions to level up
                and unlock more achievements.
              </p>

            </div>


            {/* WEAK TOPIC CARD */}

            <div className="quest-focus-card">

              <div className="quest-focus-header">

                <Brain size={17} />

                <span>
                  QUEST FOCUS
                </span>

              </div>


              <h3>
                {mainTopic}
              </h3>


              <div className="quest-focus-status">

                <Target size={14} />

                Needs Practice

              </div>


              {incomingWeakTopics.length > 1 && (

                <div className="quest-other-topics">

                  <span>
                    Other focus areas
                  </span>


                  {incomingWeakTopics
                    .slice(1, 4)
                    .map(
                      function(
                        item,
                        index
                      ) {

                        let topicName =
                          "Topic";


                        if (
                          item &&
                          item.concept
                        ) {

                          topicName =
                            item.concept;

                        } else if (
                          item
                        ) {

                          topicName =
                            String(
                              item
                            );

                        }


                        return (

                          <div
                            key={index}
                          >

                            <span>
                              {topicName}
                            </span>

                            <ArrowRight
                              size={12}
                            />

                          </div>

                        );

                      }
                    )}

                </div>

              )}

            </div>


            {/* REWARD CARD */}

            <div className="quest-reward-card">

              <div className="quest-reward-icon">

                <ShieldCheck size={21} />

              </div>


              <span>
                QUEST REWARD
              </span>


              <strong>
                +135 XP
              </strong>


              <p>
                Complete every mission and
                finish your final challenge.
              </p>

            </div>


          </aside>


        </section>


        {/* =================================================
            COMPLETE QUEST
        ================================================= */}

        {questComplete && (

          <section className="quest-success-card">

            <div className="quest-success-icon">

              <Trophy size={27} />

            </div>


            <div className="quest-success-content">

              <span>
                QUEST COMPLETE
              </span>

              <h2>
                You conquered {mainTopic}! 🎉
              </h2>

              <p>
                You completed every learning mission.
                Now take another quiz to measure your improvement.
              </p>

            </div>


            <button
              type="button"
              className="quest-final-button"
              onClick={function() {

                if (noteId) {

                  navigate(
                    "/notes/" +
                    noteId +
                    "/quiz"
                  );

                }

              }}
            >

              Final Challenge

              <ArrowRight size={17} />

            </button>

          </section>

        )}


        {/* =================================================
            BOTTOM TIP
        ================================================= */}

        <section className="quest-tip">

          <div className="quest-tip-icon">

            <LightbulbIcon />

          </div>


          <div>

            <strong>
              Your goal isn't perfection.
            </strong>

            <p>
              Every completed mission means
              you're one step closer to mastering
              the topic.
            </p>

          </div>

        </section>


        {/* =================================================
            RESET
        ================================================= */}

        {completedCount > 0 && (

          <div className="quest-reset-wrapper">

            <button
              type="button"
              className="quest-reset-button"
              onClick={resetQuest}
            >
              Reset Quest
            </button>

          </div>

        )}

      </main>
      <Footer />
    </div>

  );

}


/* =========================================================
   SMALL LIGHTBULB ICON
   ========================================================= */

function LightbulbIcon() {

  return (
    <Sparkles size={18} />
  );

}
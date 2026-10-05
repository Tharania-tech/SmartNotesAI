import React from "react";
import { useNavigate } from "react-router-dom";

import {
  Trophy,
  Target,
  BarChart3,
  Brain,
  CircleCheck,
  Clock3,
  ArrowUpRight,
  UploadCloud,
  FileText,
  CheckCircle2
} from "lucide-react";

import AppHeader from "../components/AppHeader";

import "./Progress.css";

export default function Progress() {
  const navigate = useNavigate();

  const topicProgress = [
    {
      subject: "Java Programming",
      progress: 88,
      sessions: "8 study sessions"
    },
    {
      subject: "Database Management",
      progress: 72,
      sessions: "6 study sessions"
    },
    {
      subject: "Computer Networks",
      progress: 64,
      sessions: "5 study sessions"
    },
    {
      subject: "Operating Systems",
      progress: 81,
      sessions: "7 study sessions"
    }
  ];

  return (
    <div className="progress-page">

      <AppHeader />

      <main className="progress-container">

        {/* PAGE TITLE */}
        <section className="progress-page-header">

          <div>
            <div className="progress-eyebrow">
              <BarChart3 size={16} />
              Learning Progress
            </div>

            <h1>
              Track your learning journey
            </h1>

            <p>
              Monitor your quiz performance, study activity,
              topic progress and achievements in one place.
            </p>
          </div>

          <button
            type="button"
            className="progress-upload-button"
            onClick={function () {
              navigate("/upload");
            }}
          >
            <UploadCloud size={18} />
            Upload New Notes
          </button>

        </section>

        {/* STAT CARDS */}
        <section className="progress-stat-grid">

          <div className="progress-stat-card">

            <div className="progress-stat-icon blue">
              <FileText size={21} />
            </div>

            <div>
              <span>Total Notes</span>
              <strong>5</strong>
              <small>+2 this week</small>
            </div>

          </div>

          <div className="progress-stat-card">

            <div className="progress-stat-icon green">
              <CircleCheck size={21} />
            </div>

            <div>
              <span>Quizzes Completed</span>
              <strong>3</strong>
              <small>+1 this week</small>
            </div>

          </div>

          <div className="progress-stat-card">

            <div className="progress-stat-icon purple">
              <Brain size={21} />
            </div>

            <div>
              <span>Average Score</span>
              <strong>78%</strong>
              <small>+12% improvement</small>
            </div>

          </div>

          <div className="progress-stat-card">

            <div className="progress-stat-icon orange">
              <Clock3 size={21} />
            </div>

            <div>
              <span>Study Time</span>
              <strong>12.5h</strong>
              <small>This month</small>
            </div>

          </div>

        </section>

        {/* OVERALL + ANALYTICS */}
        <section className="progress-main-grid">

          {/* OVERALL PROGRESS */}
          <div className="progress-panel">

            <div className="progress-panel-header">

              <div>
                <span className="progress-panel-label">
                  OVERALL LEARNING
                </span>

                <h2>
                  Your Study Progress
                </h2>
              </div>

              <Target size={21} />

            </div>

            <div className="overall-content">

              <div className="progress-ring">

                <div className="progress-ring-inner">
                  <strong>78%</strong>
                  <span>Overall Score</span>
                </div>

              </div>

              <div className="overall-details">

                <div className="overall-detail">

                  <div className="overall-detail-row">
                    <span>Knowledge Retention</span>
                    <strong>84%</strong>
                  </div>

                  <div className="overall-detail-track">
                    <span style={{ width: "84%" }}></span>
                  </div>

                </div>

                <div className="overall-detail">

                  <div className="overall-detail-row">
                    <span>Quiz Readiness</span>
                    <strong>76%</strong>
                  </div>

                  <div className="overall-detail-track">
                    <span style={{ width: "76%" }}></span>
                  </div>

                </div>

                <div className="overall-detail">

                  <div className="overall-detail-row">
                    <span>Revision Progress</span>
                    <strong>69%</strong>
                  </div>

                  <div className="overall-detail-track">
                    <span style={{ width: "69%" }}></span>
                  </div>

                </div>

              </div>

            </div>

          </div>

          {/* STUDY ANALYTICS */}
          <div className="progress-panel">

            <div className="progress-panel-header">

              <div>
                <span className="progress-panel-label">
                  WEEKLY ACTIVITY
                </span>

                <h2>
                  Study Analytics
                </h2>
              </div>

              <BarChart3 size={21} />

            </div>

            <div className="weekly-chart">

              <div className="chart-y-labels">
                <span>100</span>
                <span>75</span>
                <span>50</span>
                <span>25</span>
                <span>0</span>
              </div>

              <div className="chart-area">

                <div className="chart-grid-line line-1"></div>
                <div className="chart-grid-line line-2"></div>
                <div className="chart-grid-line line-3"></div>
                <div className="chart-grid-line line-4"></div>
                <div className="chart-grid-line line-5"></div>

                <div className="chart-bars">

                  <div className="chart-column">
                    <div
                      className="chart-bar"
                      style={{ height: "28%" }}
                    ></div>
                    <span>Mon</span>
                  </div>

                  <div className="chart-column">
                    <div
                      className="chart-bar"
                      style={{ height: "42%" }}
                    ></div>
                    <span>Tue</span>
                  </div>

                  <div className="chart-column">
                    <div
                      className="chart-bar"
                      style={{ height: "63%" }}
                    ></div>
                    <span>Wed</span>
                  </div>

                  <div className="chart-column">
                    <div
                      className="chart-bar"
                      style={{ height: "51%" }}
                    ></div>
                    <span>Thu</span>
                  </div>

                  <div className="chart-column">
                    <div
                      className="chart-bar"
                      style={{ height: "72%" }}
                    ></div>
                    <span>Fri</span>
                  </div>

                  <div className="chart-column">
                    <div
                      className="chart-bar"
                      style={{ height: "69%" }}
                    ></div>
                    <span>Sat</span>
                  </div>

                  <div className="chart-column">
                    <div
                      className="chart-bar"
                      style={{ height: "86%" }}
                    ></div>
                    <span>Sun</span>
                  </div>

                </div>

              </div>

            </div>

          </div>

        </section>

        {/* TOPIC PROGRESS */}
        <section className="progress-panel topic-panel">

          <div className="progress-panel-header">

            <div>
              <span className="progress-panel-label">
                SUBJECT TRACKING
              </span>

              <h2>
                Topic Progress
              </h2>
            </div>

            <Brain size={21} />

          </div>

          <div className="topic-list">

            {topicProgress.map(function (item, index) {

              return (
                <div
                  className="topic-row"
                  key={index}
                >

                  <div className="topic-info">

                    <strong>
                      {item.subject}
                    </strong>

                    <span>
                      {item.sessions}
                    </span>

                  </div>

                  <div className="topic-progress-area">

                    <div className="topic-track">
                      <span
                        style={{
                          width: item.progress + "%"
                        }}
                      ></span>
                    </div>

                    <strong className="topic-percentage">
                      {item.progress}%
                    </strong>

                  </div>

                </div>
              );

            })}

          </div>

        </section>

        {/* ACHIEVEMENTS */}
        <section className="achievement-section">

          <div className="progress-panel-header">

            <div>
              <span className="progress-panel-label">
                MILESTONES
              </span>

              <h2>
                Achievements
              </h2>
            </div>

            <Trophy size={21} />

          </div>

          <div className="achievement-grid">

            <div className="achievement-card">

              <div className="achievement-icon">
                <Trophy size={21} />
              </div>

              <h3>
                First Quiz
              </h3>

              <p>
                Completed your first AI quiz.
              </p>

              <span className="achievement-earned">
                <CheckCircle2 size={12} />
                Earned
              </span>

            </div>

            <div className="achievement-card">

              <div className="achievement-icon">
                <Brain size={21} />
              </div>

              <h3>
                Knowledge Builder
              </h3>

              <p>
                Studied multiple learning topics.
              </p>

              <span className="achievement-earned">
                <CheckCircle2 size={12} />
                Earned
              </span>

            </div>

            <div className="achievement-card">

              <div className="achievement-icon">
                <Target size={21} />
              </div>

              <h3>
                80% Club
              </h3>

              <p>
                Reach an 80% or higher quiz score.
              </p>

              <span className="achievement-progress">
                In Progress
              </span>

            </div>

            <div className="achievement-card">

              <div className="achievement-icon">
                <ArrowUpRight size={21} />
              </div>

              <h3>
                Keep Improving
              </h3>

              <p>
                Continue improving your learning score.
              </p>

              <span className="achievement-earned">
                <CheckCircle2 size={12} />
                Earned
              </span>

            </div>

          </div>

        </section>

      </main>

    </div>
  );
}
import React, { useEffect, useMemo, useState } from "react";
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
  CheckCircle2,
  RefreshCw,
  AlertCircle,
  TrendingUp,
  Flame,
  BookOpen
} from "lucide-react";

import AppHeader from "../components/AppHeader";

import { getProgress } from "../services/notesApi";
import "./Progress.css";

function safeNumber(value, fallback = 0) {
  const number = Number(value);
  return Number.isFinite(number) ? number : fallback;
}

function clamp(value) {
  return Math.max(0, Math.min(100, safeNumber(value)));
}

function formatActivity(minutes) {
  const total = Math.max(0, Math.round(safeNumber(minutes)));
  if (total < 60) return `${total} min`;
  const hours = Math.floor(total / 60);
  const mins = total % 60;
  return mins ? `${hours}h ${mins}m` : `${hours}h`;
}

export default function Progress() {
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");

  async function loadProgress(isRefresh = false) {
    try {
      if (isRefresh) setRefreshing(true);
      else setLoading(true);

      setError("");
      const response = await getProgress();
      setData(response || {});
    } catch (err) {
      console.error("Progress page error:", err);
      setError(err?.message || "Unable to load your learning progress.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loadProgress();
  }, []);

  const stats = data?.stats || {};
  const weeklyActivity = Array.isArray(data?.weekly_activity)
    ? data.weekly_activity
    : [];
  const topicProgress = Array.isArray(data?.topic_progress)
    ? data.topic_progress
    : [];
  const weakTopics = Array.isArray(data?.weak_topics)
    ? data.weak_topics
    : [];
  const achievements = Array.isArray(data?.achievements)
    ? data.achievements
    : [];

  const overall = clamp(stats.overall_score);
  const retention = clamp(stats.knowledge_retention);
  const readiness = clamp(stats.quiz_readiness);
  const revision = clamp(stats.revision_progress);

  const weeklyAverage = useMemo(() => {
    if (!weeklyActivity.length) return 0;
    return Math.round(
      weeklyActivity.reduce((sum, item) => sum + safeNumber(item.value), 0) /
        weeklyActivity.length
    );
  }, [weeklyActivity]);

  const notesDelta = safeNumber(stats.this_week_notes) - safeNumber(stats.previous_week_notes);
  const quizDelta = safeNumber(stats.this_week_quizzes) - safeNumber(stats.previous_week_quizzes);

  return (
    <div className="progress-page">
      <AppHeader />

      <main className="progress-container">
        <section className="progress-page-header">
          <div>
            <div className="progress-eyebrow">
              <BarChart3 size={16} />
              Learning Progress
            </div>
            <h1>Track your learning journey</h1>
            <p>
              Your dashboard now uses your uploaded notes and completed quiz attempts
              to build a live learning picture.
            </p>
          </div>

          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            <button
              type="button"
              className="progress-upload-button"
              onClick={() => loadProgress(true)}
              disabled={refreshing}
            >
              <RefreshCw size={17} className={refreshing ? "progress-spin" : ""} />
              {refreshing ? "Refreshing..." : "Refresh Progress"}
            </button>

            <button
              type="button"
              className="progress-upload-button"
              onClick={() => navigate("/upload")}
            >
              <UploadCloud size={18} />
              Upload New Notes
            </button>
          </div>
        </section>

        {error && (
          <section className="progress-error-card">
            <AlertCircle size={19} />
            <span>{error}</span>
            <button type="button" onClick={() => loadProgress(true)}>
              Try again
            </button>
          </section>
        )}

        {loading ? (
          <section className="progress-loading-card">
            <div className="dashboard-loading-spinner"></div>
            <h2>Loading your learning data...</h2>
            <p>Reading your notes, quiz attempts and topic performance.</p>
          </section>
        ) : (
          <>
            <section className="progress-stat-grid">
              <div className="progress-stat-card">
                <div className="progress-stat-icon blue"><FileText size={21} /></div>
                <div>
                  <span>Total Notes</span>
                  <strong>{safeNumber(stats.total_notes)}</strong>
                  <small>{notesDelta > 0 ? `+${notesDelta} this week` : notesDelta < 0 ? `${notesDelta} vs last week` : "No change this week"}</small>
                </div>
              </div>

              <div className="progress-stat-card">
                <div className="progress-stat-icon green"><CircleCheck size={21} /></div>
                <div>
                  <span>Quizzes Completed</span>
                  <strong>{safeNumber(stats.quizzes_completed)}</strong>
                  <small>{quizDelta > 0 ? `+${quizDelta} this week` : quizDelta < 0 ? `${quizDelta} vs last week` : "No change this week"}</small>
                </div>
              </div>

              <div className="progress-stat-card">
                <div className="progress-stat-icon purple"><Brain size={21} /></div>
                <div>
                  <span>Average Score</span>
                  <strong>{safeNumber(stats.average_score)}%</strong>
                  <small>Best: {safeNumber(stats.best_score)}%</small>
                </div>
              </div>

              <div className="progress-stat-card">
                <div className="progress-stat-icon orange"><Clock3 size={21} /></div>
                <div>
                  <span>Study Activity</span>
                  <strong>{formatActivity(stats.activity_minutes)}</strong>
                  <small>7  day streak</small>
                </div>
              </div>
            </section>

            <section className="progress-main-grid">
              <div className="progress-panel">
                <div className="progress-panel-header">
                  <div>
                    <span className="progress-panel-label">OVERALL LEARNING</span>
                    <h2>Your Study Progress</h2>
                  </div>
                  <Target size={21} />
                </div>

                <div className="overall-content">
                  <div
                    className="progress-ring"
                    style={{ background: `conic-gradient(#05a5a6 0deg ${overall * 3.6}deg, #e7f0f2 ${overall * 3.6}deg 360deg)` }}
                  >
                    <div className="progress-ring-inner">
                      <strong>{Math.round(overall)}%</strong>
                      <span>Overall Score</span>
                    </div>
                  </div>

                  <div className="overall-details">
                    {[
                      ["Knowledge Retention", retention],
                      ["Quiz Readiness", readiness],
                      ["Revision Progress", revision]
                    ].map(([label, value]) => (
                      <div className="overall-detail" key={label}>
                        <div className="overall-detail-row">
                          <span>{label}</span>
                          <strong>{Math.round(value)}%</strong>
                        </div>
                        <div className="overall-detail-track">
                          <span style={{ width: `${value}%` }}></span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="progress-panel">
                <div className="progress-panel-header">
                  <div>
                    <span className="progress-panel-label">LAST 7 DAYS</span>
                    <h2>Study Analytics</h2>
                  </div>
                  <TrendingUp size={21} />
                </div>

                <div className="progress-activity-summary">
                  <strong>{weeklyAverage}%</strong>
                  <span>average daily activity</span>
                </div>

                <div className="weekly-chart">
                  <div className="chart-y-labels">
                    <span>100</span><span>75</span><span>50</span><span>25</span><span>0</span>
                  </div>

                  <div className="chart-area">
                    {[1, 25, 50, 75, 99].map((top, index) => (
                      <div key={top} className={`chart-grid-line line-${index + 1}`} style={{ top: `${top}%` }}></div>
                    ))}

                    <div className="chart-bars">
                      {(weeklyActivity.length ? weeklyActivity : [{day:"-",value:0}]).map((item, index) => (
                        <div className="chart-column" key={`${item.day}-${index}`} title={`${item.day}: ${safeNumber(item.value)} activity`}>
                          <div className="chart-bar" style={{ height: `${clamp(item.value)}%` }}></div>
                          <span>{item.day}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <section className="progress-panel topic-panel">
              <div className="progress-panel-header">
                <div>
                  <span className="progress-panel-label">SUBJECT TRACKING</span>
                  <h2>Topic Progress</h2>
                </div>
                <Brain size={21} />
              </div>

              {topicProgress.length === 0 ? (
                <div className="progress-empty-inline">
                  <BookOpen size={24} />
                  <strong>No topic performance yet</strong>
                  <span>Complete a quiz to start building topic-level progress.</span>
                </div>
              ) : (
                <div className="topic-list">
                  {topicProgress.map((item, index) => {
                    const progress = clamp(item.progress);
                    return (
                      <div className="topic-row" key={`${item.subject}-${index}`}>
                        <div className="topic-info">
                          <strong>{item.subject}</strong>
                          <span>{item.sessions}</span>
                        </div>
                        <div className="topic-progress-area">
                          <div className="topic-track">
                            <span style={{ width: `${progress}%` }}></span>
                          </div>
                          <strong className="topic-percentage">{Math.round(progress)}%</strong>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </section>

            <section className="progress-panel weak-topic-panel">
              <div className="progress-panel-header">
                <div>
                  <span className="progress-panel-label">ADAPTIVE REVISION</span>
                  <h2>Topics that need attention</h2>
                </div>
                <Target size={21} />
              </div>

              {weakTopics.length === 0 ? (
                <div className="progress-empty-inline">
                  <CheckCircle2 size={24} />
                  <strong>No weak topics detected</strong>
                  <span>Complete more quizzes and SmartNotes will identify revision areas.</span>
                </div>
              ) : (
                <div className="weak-topic-grid">
                  {weakTopics.map((item, index) => (
                    <div className="weak-topic-card" key={`${item.topic}-${index}`}>
                      <span>{index + 1}</span>
                      <div>
                        <strong>{item.topic}</strong>
                        <small>Appeared as a weak area {item.count} time{item.count === 1 ? "" : "s"}</small>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section className="achievement-section">
              <div className="progress-panel-header">
                <div>
                  <span className="progress-panel-label">MILESTONES</span>
                  <h2>Achievements</h2>
                </div>
                <Trophy size={21} />
              </div>

              <div className="achievement-grid">
                {achievements.map((item, index) => {
                  const earned = Boolean(item.earned);
                  const progress = safeNumber(item.progress);
                  const target = Math.max(1, safeNumber(item.target, 1));
                  return (
                    <div className="achievement-card" key={`${item.title}-${index}`}>
                      <div className="achievement-icon">
                        {earned ? <Trophy size={21} /> : <Target size={21} />}
                      </div>
                      <h3>{item.title}</h3>
                      <p>{item.description}</p>
                      {earned ? (
                        <span className="achievement-earned">
                          <CheckCircle2 size={12} /> Earned
                        </span>
                      ) : (
                        <span className="achievement-progress">
                          {Math.min(Math.round((progress / target) * 100), 100)}% complete
                        </span>
                      )}
                    </div>
                  );
                })}
              </div>
            </section>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}

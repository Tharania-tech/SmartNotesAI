import React, { useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  Brain,
  BookOpen,
  CheckCircle2,
  Clock3,
  FileText,
  Flame,
  Lightbulb,
  MessageCircle,
  Plus,
  Sparkles,
  Target,
  Trash2,
  TrendingUp,
  UploadCloud,
  Layers3,
  BarChart3,
  Zap,
  ChevronRight,
  RefreshCw,
  AlertCircle
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import AppHeader from "../components/AppHeader";

import { deleteNote, getNotes, getProgress } from "../services/notesApi";
import "../index.css";

function number(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function clamp(value) {
  return Math.max(0, Math.min(100, number(value)));
}

function formatDate(value) {
  if (!value) return "Recently added";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Recently added";
  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
}

function getNoteId(note) {
  return String(note?._id || note?.id || note?.note_id || "");
}

function getNoteTitle(note) {
  return note?.title || note?.file_name || note?.filename || "Untitled Notes";
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [notes, setNotes] = useState([]);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [deletingId, setDeletingId] = useState("");
  const [error, setError] = useState("");

  async function loadDashboard(isRefresh = false) {
    try {
      if (isRefresh) setRefreshing(true);
      else setLoading(true);
      setError("");

      const [notesResponse, progressResponse] = await Promise.all([
        getNotes(),
        getProgress()
      ]);

      let noteList = [];
      if (Array.isArray(notesResponse)) noteList = notesResponse;
      else if (Array.isArray(notesResponse?.notes)) noteList = notesResponse.notes;
      else if (Array.isArray(notesResponse?.data)) noteList = notesResponse.data;

      setNotes(noteList);
      setProgress(progressResponse || {});
    } catch (err) {
      console.error("Dashboard error:", err);
      setError(err?.message || "Unable to load your dashboard.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  const stats = progress?.stats || {};
  const recentNotes = Array.isArray(progress?.recent_notes) && progress.recent_notes.length
    ? progress.recent_notes
    : notes.slice(0, 6);
  const weeklyRaw = Array.isArray(progress?.weekly_activity)
  ? progress.weekly_activity
  : [];

const dayOrder = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const weekly = dayOrder.map((day) => {
  const found = weeklyRaw.find(
    (item) => String(item?.day).slice(0, 3) === day
  );

  return {
    day,
    value: number(found?.value, 0),
  };
});
  const topicProgress = Array.isArray(progress?.topic_progress) ? progress.topic_progress : [];
  const weakTopics = Array.isArray(progress?.weak_topics) ? progress.weak_topics : [];
  const latestNote = notes[0] || recentNotes[0];

  const learningScore = clamp(stats.overall_score);
  const retention = clamp(stats.knowledge_retention);
  const revision = clamp(stats.revision_progress);
  const readiness = clamp(stats.quiz_readiness);
  const streak = 7;
  const activityMinutes = number(stats.activity_minutes);

  const miniBars = useMemo(() => {
    if (!weekly.length) return [0, 0, 0, 0, 0, 0, 0];
    return weekly.map(item => clamp(item.value));
  }, [weekly]);

  async function handleDelete(note) {
    const noteId = getNoteId(note);
    if (!noteId) return;
    if (!window.confirm("Are you sure you want to delete this note?")) return;

    try {
      setDeletingId(noteId);
      await deleteNote(noteId);
      await loadDashboard(true);
    } catch (err) {
      console.error("Delete note error:", err);
      alert("Unable to delete this note.");
    } finally {
      setDeletingId("");
    }
  }

  function openNote(note) {
    const id = getNoteId(note);
    if (id) navigate(`/notes/${id}`);
  }

  return (
    <div className="dashboard-page">
      <AppHeader />

      <main className="dashboard-main">
        <section className="dashboard-hero">
          <div className="dashboard-hero-left">
            <div className="dashboard-eyebrow">
              <span className="dashboard-eyebrow-dot"></span>
              AI Learning Workspace
            </div>

            <h1 className="dashboard-hero-title">
              Learn from your notes.
              <span> Smarter, faster, better.</span>
            </h1>

            <p className="dashboard-hero-description">
              Your workspace updates from your real notes, quiz attempts and learning activity.
            </p>

            <div className="dashboard-hero-actions">
              <button type="button" className="dashboard-primary-button" onClick={() => navigate("/upload")}>
                <UploadCloud size={19} />
                Upload New Notes
                <ArrowRight size={18} />
              </button>

              <button
                type="button"
                className="dashboard-secondary-button"
                onClick={() => latestNote ? openNote(latestNote) : navigate("/upload")}
              >
                {latestNote ? "Continue Learning" : "Start Learning"}
                <ArrowRight size={18} />
              </button>
            </div>

            <div className="dashboard-trust-row">
              <div className="dashboard-trust-item"><CheckCircle2 size={17} /><span>PDF, DOCX & images</span></div>
              <div className="dashboard-trust-item"><Brain size={17} /><span>AI-powered learning</span></div>
              <div className="dashboard-trust-item"><Zap size={17} /><span>Live progress</span></div>
            </div>
          </div>

          <div className="dashboard-hero-right">
            <div className="dashboard-hero-orbit orbit-one"></div>
            <div className="dashboard-hero-orbit orbit-two"></div>

            <div className="dashboard-ai-floating-card">
              <div className="dashboard-ai-card-top">
                <div className="dashboard-ai-icon"><Sparkles size={20} /></div>
                <div>
                  <div className="dashboard-ai-label">SmartNotes AI</div>
                  <div className="dashboard-ai-subtitle">Learning engine active</div>
                </div>
                <div className="dashboard-live-pill"><span></span>Live</div>
              </div>

              <div className="dashboard-ai-score-row">
                <div className="dashboard-ai-score">
                  <strong>{Math.round(learningScore)}</strong>
                  <span>Learning Score</span>
                </div>
                <div className="dashboard-ai-mini-bars">
                  {miniBars.map((value, index) => (
                    <span key={index} style={{ height: `${Math.max(value, 5)}%` }}></span>
                  ))}
                </div>
              </div>

              <div className="dashboard-ai-insight">
                <Lightbulb size={17} />
                <span>
                  {weakTopics.length
                    ? `${weakTopics[0].topic} is currently a revision focus.`
                    : stats.quizzes_completed
                      ? "Your quiz history is building a personalized learning profile."
                      : "Complete a quiz to unlock personalized insights."}
                </span>
              </div>
            </div>
          </div>
        </section>

        {error && (
          <section className="dashboard-error-card">
            <AlertCircle size={18} />
            <span>{error}</span>
            <button type="button" onClick={() => loadDashboard(true)}>Try again</button>
          </section>
        )}

        <section className="dashboard-stats-grid">
          <div className="dashboard-stat-card">
            <div className="dashboard-stat-icon teal"><FileText size={19} /></div>
            <div><span className="dashboard-stat-label">Notes uploaded</span><strong className="dashboard-stat-value">{number(stats.total_notes, notes.length)}</strong><span className="dashboard-stat-caption">Your study library</span></div>
          </div>

          <div className="dashboard-stat-card">
            <div className="dashboard-stat-icon blue"><Layers3 size={19} /></div>
            <div><span className="dashboard-stat-label">AI learning tools</span><strong className="dashboard-stat-value">5</strong><span className="dashboard-stat-caption">Summary · concepts · cards · quiz · AI tutor</span></div>
          </div>

          <div className="dashboard-stat-card">
            <div className="dashboard-stat-icon violet"><Target size={19} /></div>
            <div><span className="dashboard-stat-label">Learning score</span><strong className="dashboard-stat-value">{Math.round(learningScore)}%</strong><span className="dashboard-stat-caption positive">Based on your real activity</span></div>
          </div>

          <div className="dashboard-stat-card">
            <div className="dashboard-stat-icon orange"><Flame size={19} /></div>
            <div><span className="dashboard-stat-label">Study streak</span><strong className="dashboard-stat-value">{streak} {streak === 1 ? "day" : "days"}</strong><span className="dashboard-stat-caption">Keep the momentum</span></div>
          </div>
        </section>

        <section className="dashboard-intelligence-section">
          <div className="dashboard-section-heading">
            <div>
              <span className="dashboard-section-kicker">AI INSIGHTS</span>
              <h2>Learning intelligence</h2>
              <p>Understand how your study behaviour is progressing.</p>
            </div>
            <button type="button" className="dashboard-section-link" onClick={() => navigate("/progress")}>
              View full progress <ChevronRight size={16} />
            </button>
          </div>

          <div className="dashboard-intelligence-grid">
            <div className="dashboard-intelligence-card">
              <div className="dashboard-intelligence-header">
                <div className="dashboard-intelligence-heading">
                  <div className="dashboard-intelligence-logo"><Sparkles size={18} /></div>
                  <div><h3>Learning Intelligence</h3><span>Calculated from your activity</span></div>
                </div>
                <br></br>
                <br></br>
                <button type="button" className="dashboard-more-button" onClick={() => navigate("/progress")}><BarChart3 size={17} /></button>
              </div>
              <br>
              </br>
              <div className="dashboard-intelligence-main">
                <div className="dashboard-progress-ring" style={{ background: `conic-gradient(#05a5a6 0deg ${learningScore * 3.6}deg, #e7f0f2 ${learningScore * 3.6}deg 360deg)` }}>
                  <div className="dashboard-progress-ring-inner"><strong>{Math.round(learningScore)}%</strong><span>Overall</span></div>
                </div>
<br></br>
                <div className="dashboard-intelligence-copy">
                  <div className="dashboard-intelligence-status"><span></span>{learningScore >= 70 ? "Learning pace is healthy" : "Build more study activity"}</div>
                  <h4>{stats.quizzes_completed ? "Your learning profile is becoming more accurate." : "Your learning profile starts with your first quiz."}</h4>
                  <p>
                    {weakTopics.length
                      ? `Focus next on ${weakTopics.slice(0, 2).map(item => item.topic).join(" and ")}.`
                      : "Upload notes and complete quizzes to generate topic-level insights."}
                  </p>
                </div>
              </div>
              <br></br>
              <br></br>
              <div className="dashboard-intelligence-metrics">
                {[["Concept retention", retention], ["Revision consistency", revision], ["Quiz readiness", readiness]].map(([label, value]) => (
                  <div className="dashboard-intelligence-metric" key={label}>
                    <span>{label}</span><strong>{Math.round(value)}%</strong>
                    <div className="metric-progress"><span style={{ width: `${value}%` }}></span></div>
                  </div>
                ))}
              </div>
            </div>

            <div className="dashboard-study-analytics-card">
              <div className="dashboard-analytics-header">
                <div><span className="dashboard-analytics-kicker">STUDY ANALYTICS</span><h3>Recent performance</h3><p>Last 7 days</p></div>
                <div className="dashboard-analytics-icon"><TrendingUp size={18} /></div>
              </div>

              <div className="dashboard-analytics-score">
                <div><span>Average quiz score</span><strong>{number(stats.average_score)}%</strong></div>
                <div className="dashboard-analytics-circle" style={{ background: `conic-gradient(#05a5a6 0deg ${clamp(stats.average_score) * 3.6}deg, #e7f0f2 ${clamp(stats.average_score) * 3.6}deg 360deg)` }}>
                  <div className="dashboard-analytics-circle-inner"><strong>{number(stats.quizzes_completed)}</strong><span>quizzes</span></div>
                </div>
              </div>

             <div className="dashboard-analytics-chart">

  {/* Y-axis labels */}
  <div className="dashboard-chart-y-axis">
    <span>100</span>
    <span>75</span>
    <span>50</span>
    <span>25</span>
    <span>0</span>
  </div>

  {/* Chart area */}
  <div className="dashboard-chart-area">

    {/* Horizontal grid lines */}
    <div className="dashboard-chart-grid">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>

    {/* Bars */}
    <div className="dashboard-chart-bars">
      {weekly.map((item, index) => {
        const value = clamp(item.value);

        return (
          <div
            className="dashboard-chart-bar-column"
            key={`${item.day}-${index}`}
            title={`${item.day}: ${value} activity`}
          >
            <div
              className="dashboard-chart-bar"
              style={{
                height: `${value}%`,
              }}
            />
          </div>
        );
      })}
    </div>

    {/* Days */}
    <div className="dashboard-chart-days">
      {weekly.map((item) => (
        <span key={item.day}>{item.day}</span>
      ))}
    </div>

  </div>
</div>

              <div className="dashboard-analytics-footer">
                <div><Clock3 size={15} /> Activity proxy: {activityMinutes} min</div>
                <div><Flame size={15} /> {streak} day streak</div>
              </div>
            </div>
          </div>
        </section>

        <section className="dashboard-focus-section">
          <div className="dashboard-section-heading">
            <div><span className="dashboard-section-kicker">CONTINUE LEARNING</span><h2>Pick up where you left off</h2><p>Open your latest study material.</p></div>
            <button type="button" className="dashboard-section-link" onClick={() => navigate("/progress")}>Progress <ChevronRight size={16} /></button>
          </div>

          {latestNote ? (
            <div className="dashboard-focus-card">
              <div className="dashboard-focus-left">
                <div className="dashboard-focus-file-icon"><FileText size={21} /></div>
                <div className="dashboard-focus-info">
                  <span className="dashboard-focus-label">LATEST NOTE</span>
                  <h3>{getNoteTitle(latestNote)}</h3>
                  <div className="dashboard-focus-meta"><span><BookOpen size={14} /> {latestNote.file_type || "Study material"}</span><span>{formatDate(latestNote.created_at)}</span></div>
                </div>
              </div>
              <div className="dashboard-focus-right">
                <div className="dashboard-focus-progress"><div className="dashboard-focus-progress-top"><span>Learning score</span><strong>{Math.round(learningScore)}%</strong></div><div className="dashboard-focus-progress-track"><span style={{ width: `${learningScore}%` }}></span></div></div>
                <button type="button" className="dashboard-focus-button" onClick={() => openNote(latestNote)}>Open Note <ArrowRight size={16} /></button>
              </div>
            </div>
          ) : (
            <div className="dashboard-empty-state"><div className="dashboard-empty-icon"><UploadCloud size={27} /></div><h3>Your study workspace is empty</h3><p>Upload your first note to start generating summaries, concepts, flashcards and quizzes.</p><button type="button" className="dashboard-primary-button small" onClick={() => navigate("/upload")}><Plus size={17} /> Upload First Note</button></div>
          )}
        </section>

        <section className="dashboard-tools-section">
          <div className="dashboard-section-heading">
            <div><span className="dashboard-section-kicker">LEARNING TOOLS</span><h2>Turn notes into active learning</h2><p>Every uploaded note unlocks your study workflow.</p></div>
          </div>

          <div className="dashboard-tools-grid">
            {[
              ["teal", Sparkles, "AI Summary", "Understand the main ideas quickly."],
              ["blue", Brain, "Key Concepts", "Find the important concepts in your notes."],
              ["violet", Layers3, "Flashcards", "Turn content into active recall practice."],
              ["orange", Target, "Adaptive Quiz", "Test yourself and build progress."],
              ["indigo", MessageCircle, "AI Tutor", "Ask questions directly from your note."],
              ["add", UploadCloud, "Upload Notes", "Add another PDF, DOCX or image."]
            ].map(([tone, Icon, title, description]) => (
              <button
                type="button"
                className={`dashboard-tool-card ${tone}`}
                key={title}
                onClick={() => title === "Upload Notes" ? navigate("/upload") : latestNote ? openNote(latestNote) : navigate("/upload")}
              >
                <div className="dashboard-tool-top"><div className="dashboard-tool-icon"><Icon size={20} /></div><ArrowRight size={17} /></div>
                <h3>{title}</h3><p>{description}</p>
              </button>
            ))}
          </div>
        </section>

        <section className="dashboard-notes-section">
          <div className="dashboard-section-heading">
            <div><span className="dashboard-section-kicker">YOUR LIBRARY</span><h2>Recent notes</h2><p>Your latest uploaded study material.</p></div>
            <button type="button" className="dashboard-section-link" onClick={() => loadDashboard(true)} disabled={refreshing}><RefreshCw size={15} /> {refreshing ? "Refreshing" : "Refresh"}</button>
          </div>

          {loading ? (
            <div className="dashboard-empty-state"><div className="dashboard-loading-spinner"></div><h3>Loading your notes...</h3><p>Connecting to your SmartNotes workspace.</p></div>
          ) : recentNotes.length === 0 ? (
            <div className="dashboard-empty-state"><div className="dashboard-empty-icon"><FileText size={27} /></div><h3>No notes yet</h3><p>Upload study material and it will appear here.</p></div>
          ) : (
            <div className="dashboard-notes-grid">
              {recentNotes.map((note, index) => {
                const id = getNoteId(note);
                return (
                  <article className="dashboard-note-card" key={id || index}>
                    <div className="dashboard-note-card-top">
                      <div className="dashboard-note-icon"><FileText size={18} /></div>
                      <button type="button" className="dashboard-delete-button" disabled={!id || deletingId === id} onClick={() => handleDelete(note)} title="Delete note"><Trash2 size={15} /></button>
                    </div>
                    <div className="dashboard-note-content">
                      <span className="dashboard-note-type">{note.file_type || "NOTE"}</span>
                      <h3>{getNoteTitle(note)}</h3>
                      <p>{formatDate(note.created_at)}</p>
                    </div>
                    <button type="button" className="dashboard-note-open" onClick={() => openNote(note)}>Open <ArrowRight size={15} /></button>
                  </article>
                );
              })}
            </div>
          )}
        </section>
      </main>
      <Footer />
    </div>
  );
}

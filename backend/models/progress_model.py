from datetime import datetime, timezone, timedelta

from database.db import mongo


class ProgressModel:

    @staticmethod
    def create_quiz_attempt(user_id, note_id, quiz, answers, result):
        topic_performance = ProgressModel.calculate_topic_performance(quiz, answers)

        weak_topics = []
        raw_weak_topics = result.get("weak_topics", []) if isinstance(result, dict) else []

        for item in raw_weak_topics:
            concept = item.get("concept", "") if isinstance(item, dict) else str(item)
            concept = str(concept).strip()
            if concept:
                weak_topics.append(concept)

        document = {
            "user_id": str(user_id),
            "note_id": str(note_id),
            "score_percentage": float(result.get("score_percentage", 0)),
            "correct_answers": int(result.get("correct_answers", 0)),
            "wrong_answers": int(result.get("wrong_answers", 0)),
            "total_questions": int(result.get("total_questions", len(quiz))),
            "difficulty": str(result.get("difficulty", "intermediate")),
            "weak_topics": weak_topics,
            "topic_performance": topic_performance,
            "submitted_at": datetime.now(timezone.utc),
        }

        return mongo.db.quiz_attempts.insert_one(document)

    @staticmethod
    def calculate_topic_performance(quiz, answers):
        if not isinstance(quiz, list):
            return []
        if not isinstance(answers, dict):
            answers = {}

        topic_data = {}

        for index, question in enumerate(quiz):
            if not isinstance(question, dict):
                continue

            concept = str(question.get("concept", "General")).strip() or "General"
            correct_answer = str(
                question.get("correct_answer", question.get("correctAnswer", ""))
            ).strip().upper()
            user_answer = ProgressModel.get_user_answer(answers, index)

            if concept not in topic_data:
                topic_data[concept] = {
                    "concept": concept,
                    "total_questions": 0,
                    "correct_answers": 0,
                }

            topic_data[concept]["total_questions"] += 1

            if user_answer and correct_answer and user_answer == correct_answer:
                topic_data[concept]["correct_answers"] += 1

        result = []
        for item in topic_data.values():
            total = item["total_questions"]
            correct = item["correct_answers"]
            accuracy = (correct / total) * 100 if total else 0
            result.append({
                "concept": item["concept"],
                "total_questions": total,
                "correct_answers": correct,
                "accuracy_percentage": round(accuracy, 2),
            })

        return result

    @staticmethod
    def get_user_answer(answers, index):
        for key in (str(index + 1), index + 1, str(index), index):
            if key in answers:
                return str(answers[key]).strip().upper()
        return ""

    # =========================================================
    # DYNAMIC DASHBOARD / PROGRESS DATA
    # =========================================================

    @staticmethod
    def get_dashboard_data(user_id):
        user_id = str(user_id)
        now = datetime.now(timezone.utc)
        week_start = now - timedelta(days=6)
        previous_week_start = now - timedelta(days=13)

        notes = list(
            mongo.db.notes.find({"user_id": user_id}).sort("_id", -1)
        )

        attempts = list(
            mongo.db.quiz_attempts.find({"user_id": user_id}).sort("submitted_at", -1)
        )

        def note_datetime(note):
            created = note.get("created_at") or note.get("uploaded_at")
            if isinstance(created, datetime):
                return created if created.tzinfo else created.replace(tzinfo=timezone.utc)
            try:
                return note["_id"].generation_time
            except Exception:
                return now

        def attempt_datetime(attempt):
            value = attempt.get("submitted_at")
            if isinstance(value, datetime):
                return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
            return now

        def in_week(value, start):
            return value >= start

        total_notes = len(notes)
        quizzes_completed = len(attempts)
        scores = [float(a.get("score_percentage", 0)) for a in attempts]
        average_score = round(sum(scores) / len(scores), 1) if scores else 0
        best_score = round(max(scores), 1) if scores else 0

        this_week_notes = sum(1 for n in notes if in_week(note_datetime(n), week_start))
        previous_week_notes = sum(
            1 for n in notes
            if previous_week_start <= note_datetime(n) < week_start
        )
        this_week_quizzes = sum(1 for a in attempts if in_week(attempt_datetime(a), week_start))
        previous_week_quizzes = sum(
            1 for a in attempts
            if previous_week_start <= attempt_datetime(a) < week_start
        )

        # Topic accuracy is weighted by the number of questions attempted.
        topic_totals = {}
        weak_counter = {}

        for attempt in attempts:
            for topic in attempt.get("topic_performance", []) or []:
                if not isinstance(topic, dict):
                    continue
                concept = str(topic.get("concept", "General")).strip() or "General"
                total = int(topic.get("total_questions", 0) or 0)
                correct = int(topic.get("correct_answers", 0) or 0)
                bucket = topic_totals.setdefault(concept, {"total": 0, "correct": 0})
                bucket["total"] += total
                bucket["correct"] += correct

            for weak in attempt.get("weak_topics", []) or []:
                name = str(weak).strip()
                if name:
                    weak_counter[name] = weak_counter.get(name, 0) + 1

        topic_progress = []
        for concept, bucket in topic_totals.items():
            total = bucket["total"]
            correct = bucket["correct"]
            accuracy = round((correct / total) * 100, 1) if total else 0
            topic_progress.append({
                "subject": concept,
                "progress": accuracy,
                "sessions": f"{total} quiz question{'s' if total != 1 else ''}",
            })

        topic_progress.sort(key=lambda item: item["progress"])
        topic_progress = topic_progress[:8]

        knowledge_retention = (
            round(
                sum(item["progress"] * topic_totals[item["subject"]]["total"] for item in topic_progress)
                / max(sum(topic_totals[item["subject"]]["total"] for item in topic_progress), 1),
                1,
            )
            if topic_progress else 0
        )

        # Revision progress is based on generated learning material stored on notes.
        if notes:
            revision_points = []
            for note in notes:
                points = 0
                for field in ("summary", "keywords", "flashcards", "quiz"):
                    value = note.get(field)
                    if value:
                        points += 1
                revision_points.append(points / 4 * 100)
            revision_progress = round(sum(revision_points) / len(revision_points), 1)
        else:
            revision_progress = 0

        quiz_readiness = average_score
        overall_score = round(
            (knowledge_retention + quiz_readiness + revision_progress) / 3,
            1,
        ) if (topic_progress or attempts or notes) else 0

        # A real study-time field does not exist in the current database, so expose
        # activity minutes as an honest proxy instead of inventing hours.
        activity_minutes = (this_week_notes * 20) + (this_week_quizzes * 25)

        weekly_activity = []
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for offset in range(6, -1, -1):
            day = (now - timedelta(days=offset)).date()
            note_count = sum(1 for n in notes if note_datetime(n).date() == day)
            quiz_count = sum(1 for a in attempts if attempt_datetime(a).date() == day)
            activity = min(100, note_count * 25 + quiz_count * 35)
            weekly_activity.append({
                "day": day_names[(day.weekday())],
                "value": activity,
                "notes": note_count,
                "quizzes": quiz_count,
            })

        activity_days = set()
        for note in notes:
            activity_days.add(note_datetime(note).date())
        for attempt in attempts:
            activity_days.add(attempt_datetime(attempt).date())

        streak = 0
        cursor = now.date()
        while cursor in activity_days:
            streak += 1
            cursor -= timedelta(days=1)

        recent_notes = []
        for note in notes[:6]:
            recent_notes.append({
                "note_id": str(note.get("_id")),
                "title": note.get("title") or note.get("filename") or "Untitled Note",
                "filename": note.get("filename", ""),
                "file_type": note.get("file_type", ""),
                "created_at": note_datetime(note).isoformat(),
            })

        achievements = [
            {
                "title": "First Note",
                "description": "Upload your first study note.",
                "earned": total_notes >= 1,
                "progress": min(total_notes, 1),
                "target": 1,
            },
            {
                "title": "First Quiz",
                "description": "Complete your first AI quiz.",
                "earned": quizzes_completed >= 1,
                "progress": min(quizzes_completed, 1),
                "target": 1,
            },
            {
                "title": "80% Club",
                "description": "Reach an 80% or higher quiz score.",
                "earned": best_score >= 80,
                "progress": min(best_score, 80),
                "target": 80,
            },
            {
                "title": "Knowledge Builder",
                "description": "Build progress across three concepts.",
                "earned": len(topic_progress) >= 3,
                "progress": min(len(topic_progress), 3),
                "target": 3,
            },
            {
                "title": "7 Day Streak",
                "description": "Study on seven consecutive days.",
                "earned": streak >= 7,
                "progress": min(streak, 7),
                "target": 7,
            },
        ]

        return {
            "stats": {
                "total_notes": total_notes,
                "quizzes_completed": quizzes_completed,
                "average_score": average_score,
                "best_score": best_score,
                "overall_score": overall_score,
                "knowledge_retention": knowledge_retention,
                "quiz_readiness": quiz_readiness,
                "revision_progress": revision_progress,
                "study_streak": streak,
                "activity_minutes": activity_minutes,
                "this_week_notes": this_week_notes,
                "previous_week_notes": previous_week_notes,
                "this_week_quizzes": this_week_quizzes,
                "previous_week_quizzes": previous_week_quizzes,
            },
            "weekly_activity": weekly_activity,
            "topic_progress": topic_progress,
            "weak_topics": [
                {"topic": name, "count": count}
                for name, count in sorted(weak_counter.items(), key=lambda item: item[1], reverse=True)[:5]
            ],
            "recent_notes": recent_notes,
            "achievements": achievements,
        }

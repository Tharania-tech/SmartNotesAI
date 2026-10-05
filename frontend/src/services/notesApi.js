import api from "./api";

/*
 * =========================================================
 * GET ALL NOTES
 * =========================================================
 */

export async function getNotes() {
    const response = await api.get(
        "/notes"
    );

    return response.data;
}


/*
 * =========================================================
 * UPLOAD NOTE
 * =========================================================
 */

export async function uploadNote(
    file,
    title = ""
) {
    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    if (title.trim()) {
        formData.append(
            "title",
            title.trim()
        );
    }

    const response = await api.post(
        "/notes/upload",
        formData, {
            timeout: 600000
        }
    );

    return response.data;
}


/*
 * =========================================================
 * GET ONE NOTE
 * =========================================================
 */

export async function getNote(
    noteId
) {
    const response = await api.get(
        "/notes/" + noteId
    );

    return response.data;
}


/*
 * =========================================================
 * GENERATE SUMMARY
 * =========================================================
 */

export async function generateSummary(
    noteId,
    length = "medium"
) {
    const response = await api.post(
        "/notes/" + noteId + "/summarize", {
            length: length
        }, {
            timeout: 600000
        }
    );

    return response.data;
}


/*
 * =========================================================
 * GET / GENERATE KEY CONCEPTS
 * =========================================================
 */

export async function getConcepts(
    noteId
) {
    const response = await api.post(
        "/notes/" + noteId + "/keywords", {}, {
            timeout: 600000
        }
    );

    return response.data;
}


/*
 * =========================================================
 * GENERATE FLASHCARDS
 * =========================================================
 *
 * IMPORTANT:
 *
 * Flashcard generation can take longer than the normal
 * Axios timeout because the backend may need to:
 *
 * 1. Retrieve the note from MongoDB
 * 2. Clean the extracted text
 * 3. Extract concepts
 * 4. Find explanations
 * 5. Generate and validate flashcards
 *
 * Therefore this request gets a dedicated 10-minute timeout.
 * =========================================================
 */

export async function generateFlashcards(
    noteId
) {
    if (!noteId) {
        throw new Error(
            "Note ID is missing."
        );
    }

    const response = await api.post(
        "/notes/" +
        noteId +
        "/flashcards", {}, {
            timeout: 600000
        }
    );

    return response.data;
}

/*
 * =========================================================
 * ASK AI ABOUT NOTE
 * =========================================================
 */




/*
 * =========================================================
 * ASK AI ABOUT NOTE
 * =========================================================
 */

export async function chatWithNote(
    noteId,
    question
) {
    if (!noteId) {
        throw new Error(
            "Note ID is missing."
        );
    }

    if (!question || !question.trim()) {
        throw new Error(
            "Question is required."
        );
    }

    const response = await api.post(
        "/chat", {
            message: question.trim(),
            noteId: noteId
        }, {
            timeout: 600000
        }
    );

    return response.data;
}
/*
 * =========================================================
 * DELETE NOTE
 * =========================================================
 */

export async function deleteNote(
    noteId
) {
    const response = await api.delete(
        "/notes/" + noteId
    );

    return response.data;
}


/*
 * =========================================================
 * GENERATE QUIZ
 * =========================================================
 */

export async function generateQuiz(
    noteId,
    difficulty,
    questionCount
) {
    const response = await api.post(
        "/notes/" +
        noteId +
        "/quiz", {
            difficulty: difficulty,
            question_count: questionCount
        }, {
            timeout: 600000
        }
    );

    return response.data;
}


/*
 * =========================================================
 * SUBMIT QUIZ
 * =========================================================
 */

export async function submitQuiz(
    noteId,
    answers
) {
    const response = await api.post(
        "/notes/" +
        noteId +
        "/quiz/submit", {
            answers: answers
        }, {
            timeout: 600000
        }
    );

    return response.data;
}
# SmartNotes AI — Complete Web Application

SmartNotes AI is a full-stack learning workspace built from the supplied project.

## Stack

- **Frontend:** React 18 + Vite + React Router + Axios + Lucide
- **Backend:** Flask + Flask-CORS + Flask-PyMongo
- **Database:** MongoDB
- **Authentication:** bcrypt password hashing + JWT
- **AI:** Existing Ollama/Qwen services, Gemini integration, OCR/document-processing services already present in the project

## Main features

- User registration and login
- JWT-protected workspace
- Per-user MongoDB note library
- PDF, DOCX, PNG, JPG and JPEG upload
- Text extraction / OCR pipeline
- AI summaries
- Key concepts
- Flashcards
- AI-generated quizzes
- Quiz submission and learning results
- AI tutor/chat over uploaded notes
- Progress, weak-topic and learning-quest pages
- Responsive dashboard and reusable header/navigation
- Existing SmartNotes logo and project assets retained
- UI theme aligned to deep teal → cyan, navy text, white cards and light blue-gray borders

## Project structure

```text
smartnotes-ai/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── controllers/
│   ├── database/
│   ├── middleware/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── uploads/              # created automatically
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 1. MongoDB

Install and start MongoDB locally, then use:

```text
mongodb://localhost:27017/smartnotes_ai
```

A MongoDB database named `smartnotes_ai` is created automatically when the application first writes data.

## 2. Backend setup

Open a terminal:

```bash
cd backend
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set a strong `SECRET_KEY`.

Start Flask:

```bash
python run.py
```

The API is available at:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/api/health
```

## 3. Frontend setup

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server will normally be available at:

```text
http://localhost:5173
```

The frontend `.env` uses:

```text
VITE_API_BASE_URL=http://127.0.0.1:5000/api
VITE_USE_MOCK_API=false
```

## 4. Ollama / local AI

The existing application uses:

```text
qwen2.5:3b-instruct-q4_0
```

Install Ollama separately and make sure the model used by the project is available before using quiz/chat features.

The project also contains document/OCR and embedding services. Their model downloads can be large and may require additional RAM/CPU/GPU depending on the uploaded material.

## 5. Gemini

The learning-content service reads `GEMINI_API_KEY` from `backend/.env`.

Do **not** commit a real API key to GitHub. The supplied project originally contained a credential in its environment file, so the packaged version has been replaced with an empty placeholder.

If the original credential was ever pushed to a public or shared repository, rotate/revoke it in the provider console.

## Important changes made

1. Added `backend/requirements.txt`.
2. Added safe `.env.example` files.
3. Removed the hard-coded `test_user` flow.
4. Added JWT authentication middleware.
5. Protected note APIs with JWT.
6. Scoped note listing/upload to the authenticated MongoDB user.
7. Added ownership checks before note operations.
8. Added `GET /api/notes/<note_id>`.
9. Added `/api/health`.
10. Added upload filename sanitization and unique stored filenames.
11. Added note creation timestamps.
12. Added frontend protected routes.
13. Added a reusable frontend `getNote()` API helper.
14. Unified the dominant UI colors around the requested teal/cyan + navy palette.
15. Removed portable-project noise such as `node_modules`, Python virtual environments and Python cache files from the final ZIP.

## Production checklist

Before deploying publicly:

- Use MongoDB Atlas or a secured MongoDB server.
- Set a long random `SECRET_KEY`.
- Set `DEBUG=False`.
- Configure an explicit frontend origin in CORS instead of `*`.
- Store Gemini/Ollama credentials only in environment variables/secrets.
- Use HTTPS.
- Add reverse proxy/upload storage controls for production.

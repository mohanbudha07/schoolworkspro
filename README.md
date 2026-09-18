# SchoolWorksPro (learning campus MVP)

A SchoolWorksPro-style campus system with three workspaces (student, teacher, admin) and a local AI/ML layer that:

- tracks **topic mastery** after every quiz or practice item
- flags **at-risk students** from mastery + score trend
- **predicts the next quiz score** with a small Ridge regression
- **generates adaptive practice questions** aimed at weak topics (math templates + subject banks)

Stack: **FastAPI + SQLite + scikit-learn** · **Vite + React**.

## Demo accounts

| Role    | Email                 | Password    |
|---------|-----------------------|-------------|
| Admin   | admin@school.edu      | admin123    |
| Teacher | teacher@school.edu    | teacher123  |
| Student | student@school.edu    | student123  |

Other seeded students: `arjun@school.edu`, `sita@school.edu`, `milan@school.edu` (password `student123`).

## Run locally

```bash
# backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# frontend (second terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — the Vite dev server proxies `/api` to FastAPI.

## What each role can do

- **Student:** sit published quizzes, open adaptive practice, see mastery bars, risk, trend, predicted score.
- **Teacher:** class pulse, question bank, author quizzes from the bank, read per-student recommendations.
- **Admin:** campus counts, people directory (create users), school-wide insight tables.

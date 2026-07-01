# Algo Visualizer

A full-stack app that runs classic sorting and searching algorithms and
shows live performance metrics (comparisons, swaps, execution time),
visualized with a bar chart.

**Stack:** FastAPI (Python) · React (Vite) · PyTest · GitHub Actions CI/CD

---

## Project Structure

```
algo-visualizer/
├── backend/
│   ├── main.py              # FastAPI app + /sort and /search endpoints
│   ├── algorithms.py        # bubble/merge/quick sort, linear/binary search
│   ├── test_algorithms.py   # PyTest suite (edge cases + correctness)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # main UI: controls, bar chart, metrics
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── .github/workflows/test.yml   # runs pytest on every push
```

---

## Run it locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API will be live at `http://127.0.0.1:8000`. Interactive docs at
`http://127.0.0.1:8000/docs`.

### Run the tests

```bash
cd backend
pytest -v
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App will be live at `http://localhost:5173` and will call the backend
at `http://127.0.0.1:8000` by default.

---

## Deploying (free tier, ~15 min)

**Backend → Render**
1. Push this repo to GitHub.
2. On [render.com](https://render.com), create a **New Web Service**, connect the repo.
3. Root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy — Render will auto-redeploy on every push to `main` (this is your CD).

**Frontend → Vercel**
1. On [vercel.com](https://vercel.com), import the same repo.
2. Root directory: `frontend`
3. Add an environment variable: `VITE_API_BASE_URL` = your Render backend URL.
4. Deploy — Vercel also auto-redeploys on push.

**CI**
`.github/workflows/test.yml` runs the full PyTest suite on every push/PR
to `main`. Check the **Actions** tab on GitHub to see it go green — that's
your CI badge-worthy proof point.

---

## Resume bullet this project earns you

> Built and deployed a full-stack algorithm visualizer by implementing 4
> sorting/search algorithms in Python with a PyTest suite covering 8+ edge
> cases, automated via GitHub Actions CI/CD, and a React frontend deployed
> on Vercel with live API integration.

---

## Ideas if you want to extend it later

- Add a step-by-step animation using the `steps` array already returned by
  the sort endpoints (currently computed but not yet animated in the UI)
- Add a "race mode" comparing two algorithms on the same array side by side
- Persist run history to a small SQLite/Postgres table

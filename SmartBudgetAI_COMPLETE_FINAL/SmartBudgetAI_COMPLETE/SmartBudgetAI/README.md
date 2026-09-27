# Smart Budget AI Recommendation & Assistant

A complete academic-ready implementation based on the supplied project report. It provides:

- React + Tailwind dashboard
- FastAPI backend
- SQLite by default, PostgreSQL via `DATABASE_URL`
- Personalized 50/30/20-style budget recommendations
- Scikit-learn Random Forest expense forecasting
- Isolation Forest anomaly detection
- Conversational financial assistant
- Optional OpenAI, Ollama/local Llama, LangChain and Pinecone integrations
- CSV transaction import
- REST API and health checks

The application is deliberately runnable without paid APIs. If no LLM key is configured, the assistant uses a safe deterministic local fallback.

## Project structure

```text
smart-budget-ai/
  backend/
    app/
      api/             REST endpoints
      core/            configuration
      db/              SQLAlchemy models/session
      schemas/         Pydantic request/response models
      services/        budgeting, forecasting, anomaly, LLM, vector services
      main.py
    requirements.txt
    .env.example
  frontend/
    src/
      components/
      pages/
      services/
      App.jsx
      main.jsx
      index.css
    package.json
    vite.config.js
    tailwind.config.js
    postcss.config.js
    .env.example
  sample_data/transactions.csv
  .gitignore
```

## 1. Backend setup in VS Code

Open the `smart-budget-ai` folder in VS Code.

### Windows PowerShell

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Backend: http://127.0.0.1:8000
Swagger API docs: http://127.0.0.1:8000/docs

## 2. Frontend setup

Open a second VS Code terminal:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open the Vite URL shown in the terminal, normally http://localhost:5173.

## 3. Load sample transactions

The dashboard has an import option. Or use the API:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/transactions/import-csv -F "file=@..\sample_data\transactions.csv"
```

Then refresh the dashboard.

## 4. Optional AI providers

### OpenAI

Set in `backend/.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```

### Ollama / local Llama

Install Ollama separately, pull a compatible Llama model, then set:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

The app still works when neither provider is configured.

### Pinecone

The project includes a Pinecone adapter. To enable it:

```env
VECTOR_PROVIDER=pinecone
PINECONE_API_KEY=your_key
PINECONE_INDEX=smart-budget-ai
PINECONE_NAMESPACE=default
```

The default vector provider is a local TF-IDF implementation, so no Pinecone account is required for the academic demo.

## 5. API tests

Health:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Dashboard summary:

```powershell
curl.exe "http://127.0.0.1:8000/api/dashboard/summary?user_id=demo-user"
```

Budget recommendation:

```powershell
curl.exe "http://127.0.0.1:8000/api/budget/recommendation?user_id=demo-user&monthly_income=50000"
```

Chat:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d "{"user_id":"demo-user","message":"How can I reduce my food spending?"}"
```

## 6. PostgreSQL

SQLite is the zero-configuration default. For PostgreSQL, set:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/smart_budget_ai
```

The SQLAlchemy layer automatically uses the configured URL.

## 7. Testing

Backend tests:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q
```

Frontend production build:

```powershell
cd frontend
npm run build
```

## Notes

This is an educational financial planning application, not a regulated financial-advice or fraud-detection service. Recommendations are estimates and should be reviewed by the user.

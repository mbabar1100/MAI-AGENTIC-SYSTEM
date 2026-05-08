from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import handle_query

# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------
app = FastAPI(
    title="COPD Multi-Model Analysis API",
    description="Backend API for COPD Agentic AI System",
    version="1.0"
)

# ---------------------------------------------------
# ENABLE CORS
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------
class QueryRequest(BaseModel):
    query: str
    age: int
    smoking: int

# ---------------------------------------------------
# ROOT ROUTE
# ---------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "COPD Multi-Model Analysis Backend Running"
    }

# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "backend": "running"
    }

# ---------------------------------------------------
# CHAT ROUTE
# ---------------------------------------------------
@app.post("/chat")
def chat(req: QueryRequest):

    try:

        payload = {
            "query": req.query,
            "age": req.age,
            "smoking": req.smoking
        }

        response = handle_query(payload)

        return response

    except Exception as e:

        return {
            "type": "error",
            "message": str(e)
        }
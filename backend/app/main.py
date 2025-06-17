from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import completions

app = FastAPI(title="DraftGuard API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9001"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(completions.router, prefix="/api/v1", tags=["completions"])

@app.get("/")
def read_root():
    return {"message": "DraftGuard API"}

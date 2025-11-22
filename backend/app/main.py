from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing your module routers
from app.auth.routes import router as auth_router
from app.business.routes import router as business_router
from app.reviews.routes import router as reviews_router
from app.ai.routes import router as ai_router

app = FastAPI(
    title="Local Business Intelligence - Backend",
    description="Backend API for Authentication, Business Registration, Reviews, and AI Integration",
    version="1.0.0"
)

# Allow frontend (React) to call your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all module routes
app.include_router(auth_router, prefix="/auth")
app.include_router(business_router, prefix="/business")
app.include_router(reviews_router, prefix="/reviews")
app.include_router(ai_router, prefix="/ai")

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

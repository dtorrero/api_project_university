from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user_routes, document_routes, subject_routes, course_routes
from app.connection.connection import MongoDBConnection

# Create FastAPI app
app = FastAPI(
    title="API Documentation",
    description="API for managing users, documents, subjects and courses",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(document_routes.router, prefix="/documents", tags=["documents"])
app.include_router(subject_routes.router, prefix="/subjects", tags=["subjects"])
app.include_router(course_routes.router, prefix="/courses", tags=["courses"])

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup"""
    try:
        # Test database connection
        db = MongoDBConnection().get_database()
        # You can add any additional startup database operations here
        print("Database connection established successfully!")
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    MongoDBConnection().close()
    print("Database connection closed.")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to University API",
        "status": "running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

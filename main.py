from fastapi import FastAPI
from app.connection.connection import MongoDBConnection
from app.routes import user_routes

# Create FastAPI app
app = FastAPI(
    title="University API",
    description="API for managing university courses, subjects, and documents",
    version="1.0.0"
)

# Initialize database connection
db_connection = MongoDBConnection()

# Include routers
app.include_router(user_routes.router)

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup"""
    try:
        # Test database connection
        db = db_connection.get_database()
        # You can add any additional startup database operations here
        print("Database connection established successfully!")
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    db_connection.close()
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

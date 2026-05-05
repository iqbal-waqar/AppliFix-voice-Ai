import sys
import os

# Add backend/ to sys.path so all internal imports (database, routes, etc.) resolve
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from fastapi import FastAPI
from database.connection import Base, engine
from routes import vapi_routes, health_routes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables on startup
Base.metadata.create_all(bind=engine)
logger.info("Database tables ready.")

app = FastAPI(
    title="Voice AI Appliance Service Backend",
    description="Backend for Vapi voice agent — appliance troubleshooting & technician scheduling",
    version="1.0.0",
)

# Register routers
app.include_router(health_routes.router)
app.include_router(vapi_routes.router)


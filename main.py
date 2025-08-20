from datetime import datetime
from typing import Dict, List
import platform
import sys
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime: float
    environment: str
    python_version: str


class StatusResponse(BaseModel):
    service: str
    status: str
    timestamp: str
    version: str
    python_version: str
    platform: str


class AppInfoResponse(BaseModel):
    message: str
    version: str
    features: List[str]
    endpoints: Dict[str, str]
    tech_stack: List[str]


app = FastAPI(
    title="Mehul's CI/CD API",
    description="A modern Python FastAPI application showcasing DevOps best practices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

start_time = datetime.now()


@app.get("/", response_model=AppInfoResponse)
async def root():
    return AppInfoResponse(
        message="🚀 Professional Python CI/CD Demo API",
        version="1.0.0",
        features=[
            "✅ Automated Testing with Pytest",
            "🐳 Docker Containerization",
            "🔍 Code Quality with Black & Flake8",
            "🛡️ Security Scanning with Bandit",
            "📊 Health Monitoring",
            "📖 Auto-generated API Documentation",
            "🚀 FastAPI Async Performance"
        ],
        endpoints={
            "docs": "/docs",
            "health": "/health",
            "status": "/api/status",
            "metrics": "/api/metrics"
        },
        tech_stack=[
            "Python 3.11+",
            "FastAPI",
            "Uvicorn",
            "Pydantic",
            "Docker",
            "GitHub Actions"
        ]
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    current_time = datetime.now()
    uptime = (current_time - start_time).total_seconds()
    
    return HealthResponse(
        status="healthy",
        timestamp=current_time.isoformat(),
        uptime=uptime,
        environment=os.getenv("ENVIRONMENT", "development"),
        python_version=sys.version
    )


@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    return StatusResponse(
        service="python-demo-app",
        status="running",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        platform=platform.platform()
    )


@app.get("/api/metrics")
async def get_metrics():
    current_time = datetime.now()
    uptime_seconds = (current_time - start_time).total_seconds()
    
    return {
        "uptime_seconds": uptime_seconds,
        "uptime_human": f"{uptime_seconds // 3600:.0f}h {(uptime_seconds % 3600) // 60:.0f}m {uptime_seconds % 60:.0f}s",
        "memory_info": {
            "available": "simulation",
            "used": "simulation"
        },
        "requests_total": "simulation",
        "python_info": {
            "version": sys.version,
            "platform": platform.platform(),
            "architecture": platform.architecture()[0]
        }
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    raise HTTPException(
        status_code=404,
        detail={
            "error": "Endpoint not found",
            "available_endpoints": ["/", "/health", "/api/status", "/api/metrics", "/docs"],
            "documentation": "/docs"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

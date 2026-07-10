from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Clinical Intelligence Copilot Platform API is running",
        "status": "healthy",
        "version": "0.1.0"
    }


@router.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@router.get("/project-info")
def project_info():
    return {
        "project_name": "Clinical Intelligence Copilot Platform",
        "project_type": "Personal healthcare document understanding platform",
        "purpose": "To help users understand health-related documents in simple language.",
        "safety_note": "This project does not provide medical advice, diagnose, or use real patient data."
    }
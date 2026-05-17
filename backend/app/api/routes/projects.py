from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
import uuid

from app.core.database import get_db
from app.core.config import settings
from app.models.project import Project
from app.services import vision
from app.services.chat import get_opening_message

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/")
async def create_project(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    allowed = {".jpg", ".jpeg", ".png", ".webp"}
    suffix = Path(file.filename).suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, "Formato no soportado. Usa JPG, PNG o WEBP.")

    project_id = str(uuid.uuid4())
    image_path = settings.upload_dir / f"{project_id}{suffix}"
    image_path.write_bytes(await file.read())

    analysis = await vision.analyze_image(image_path)

    project = Project(
        id=project_id,
        garment_type=analysis.get("garment_type"),
        image_path=str(image_path),
        analysis=analysis,
        conversation=[],
        status="analyzing",
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)

    opening = get_opening_message(analysis)

    return {
        "project_id": project_id,
        "analysis": analysis,
        "message": opening["message"],
    }


@router.get("/{project_id}")
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    project = await _get_or_404(project_id, db)
    return {
        "project_id": project.id,
        "garment_type": project.garment_type,
        "analysis": project.analysis,
        "parameters": project.parameters,
        "status": project.status,
        "conversation": project.conversation,
    }


async def _get_or_404(project_id: str, db: AsyncSession) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(404, "Proyecto no encontrado")
    return project

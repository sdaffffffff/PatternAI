from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.database import get_db
from app.models.project import Project
from app.services import chat as chat_service
from app.services.pattern.engine import generate_pattern

router = APIRouter(prefix="/projects", tags=["chat"])


class MessageRequest(BaseModel):
    message: str


@router.post("/{project_id}/chat")
async def send_message(
    project_id: str,
    body: MessageRequest,
    db: AsyncSession = Depends(get_db),
):
    project = await _get_or_404(project_id, db)

    if project.status == "pattern_ready":
        raise HTTPException(400, "El patrón ya está generado. Exporta o crea un nuevo proyecto.")

    conversation = list(project.conversation or [])
    result = await chat_service.process_message(
        conversation=conversation,
        user_message=body.message,
        analysis=project.analysis or {},
    )

    project.conversation = conversation

    if result["status"] == "complete":
        parameters = result["parameters"]
        parameters["garment_type"] = project.garment_type
        project.parameters = parameters
        project.status = "pattern_ready"

        pattern = generate_pattern(parameters)

        await db.commit()
        return {
            "status": "complete",
            "pattern": pattern,
            "parameters": parameters,
        }

    await db.commit()
    return {
        "status": "asking",
        "message": result["message"],
    }


async def _get_or_404(project_id: str, db: AsyncSession) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(404, "Proyecto no encontrado")
    return project

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.config import settings
from app.models.project import Project
from app.services.pattern.engine import generate_pattern
from app.services.export import pdf as pdf_exporter
from app.services.export import dxf as dxf_exporter

router = APIRouter(prefix="/projects", tags=["export"])


@router.get("/{project_id}/export/pdf")
async def export_pdf(project_id: str, db: AsyncSession = Depends(get_db)):
    project = await _get_or_404(project_id, db)
    _assert_ready(project)

    pattern = generate_pattern(project.parameters)
    output_path = settings.export_dir / f"{project_id}.pdf"
    pdf_exporter.export(pattern, output_path)

    return FileResponse(
        path=str(output_path),
        media_type="application/pdf",
        filename=f"patron_{project.garment_type}_{project.parameters.get('size', 'M')}.pdf",
    )


@router.get("/{project_id}/export/dxf")
async def export_dxf(project_id: str, db: AsyncSession = Depends(get_db)):
    project = await _get_or_404(project_id, db)
    _assert_ready(project)

    pattern = generate_pattern(project.parameters)
    output_path = settings.export_dir / f"{project_id}.dxf"
    dxf_exporter.export(pattern, output_path)

    return FileResponse(
        path=str(output_path),
        media_type="application/octet-stream",
        filename=f"patron_{project.garment_type}_{project.parameters.get('size', 'M')}.dxf",
    )


def _assert_ready(project: Project):
    if project.status != "pattern_ready" or not project.parameters:
        raise HTTPException(400, "El patrón aún no está listo. Completa el chat primero.")


async def _get_or_404(project_id: str, db: AsyncSession) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(404, "Proyecto no encontrado")
    return project

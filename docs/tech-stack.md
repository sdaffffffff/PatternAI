# Stack Técnico

## Arquitectura General

```
┌─────────────────────────────────────────────┐
│                  FRONTEND                    │
│           Next.js + TypeScript               │
│     UI interactiva + Editor de patrones      │
└──────────────────┬──────────────────────────┘
                   │ API calls
┌──────────────────▼──────────────────────────┐
│                  BACKEND                     │
│            Python + FastAPI                  │
│       Orquestación de IA + lógica de         │
│       patronaje + generación de archivos     │
└──────┬───────────┬───────────┬──────────────┘
       │           │           │
┌──────▼───┐ ┌────▼─────┐ ┌───▼──────────────┐
│ Claude   │ │  Flux /  │ │   PostgreSQL +    │
│ Vision   │ │ DALL-E 3 │ │   S3 / R2         │
│ API      │ │          │ │                   │
└──────────┘ └──────────┘ └───────────────────┘
```

---

## Decisiones Técnicas

### Frontend — Next.js + TypeScript
- App Router para estructura moderna
- Canvas interactivo con **Konva.js** para el preview de piezas del patrón
- Tailwind CSS para estilos
- Zustand para estado global

### Backend — Python + FastAPI
- Python es el estándar para pipelines de ML/IA
- FastAPI para endpoints async y tipado
- Celery + Redis para tareas pesadas (generación de renders, exports)

### IA de Análisis — Claude API (Vision)
- Analiza el sketch/imagen subida
- Clasifica tipo de prenda y detecta features visuales
- Conduce la conversación de diseño
- Genera los parámetros para el bloque base

### IA de Render — Flux o DALL-E 3
- Genera el render fotorrealista a partir del sketch + análisis
- Flux: mejor calidad de imagen, más control
- DALL-E 3: más simple de integrar via OpenAI API
- Decisión final tras pruebas de calidad en prendas

### Generación de Patrones — Librería propia
- Bloques base en formato paramétrico (curvas Bézier)
- Motor de ajuste de parámetros según respuestas del chat
- Validados por patronistas antes del lanzamiento
- Output: SVG interno → PDF / DXF para export

### Export
- **PDF:** via reportlab o WeasyPrint, con piezas a escala real con marcas de corte
- **DXF:** via ezdxf, siguiendo especificaciones AAMA/ASTM para compatibilidad industrial

### Base de Datos y Storage
- **PostgreSQL** para datos de usuarios, marcas, proyectos y tablas de medidas
- **S3 o Cloudflare R2** para almacenamiento de imágenes, renders y archivos exportados

---

## Estructura del Proyecto

```
patternai/
├── frontend/                 # Next.js app
│   ├── app/
│   ├── components/
│   │   ├── upload/
│   │   ├── render/
│   │   ├── chat/
│   │   └── pattern-editor/
│   └── lib/
│
├── backend/                  # FastAPI
│   ├── api/
│   │   ├── routes/
│   │   └── schemas/
│   ├── services/
│   │   ├── vision/           # Claude API integration
│   │   ├── render/           # Flux / DALL-E integration
│   │   ├── pattern/          # Lógica de bloques base
│   │   └── export/           # PDF + DXF generation
│   └── models/               # DB models
│
└── pattern-library/          # Bloques base validados
    ├── skirt-straight/
    ├── top-basic/
    └── shared/               # Curvas y geometría común
```

---

## Fase 2 — Adiciones Técnicas

| Feature | Herramienta |
|---------|-------------|
| Visualización 3D | Meshy API + Three.js viewer |
| Canvas de diseño | Fabric.js o Excalidraw adaptado |
| Real-time collaboration | WebSockets via FastAPI |
| Fine-tuning | Dataset propio → modelo especializado |

# MVP — Scope Definitivo

## Objetivo del MVP

Demostrar que es posible pasar de un sketch a un patrón técnico exportable con una experiencia simple, guiada por IA y visualmente atractiva — sin necesitar un patronista.

---

## Prendas Soportadas

Empezamos con las prendas de menor complejidad técnica para garantizar calidad de output.

| Prioridad | Prenda | Complejidad | Piezas aproximadas |
|-----------|--------|-------------|-------------------|
| MVP | Falda recta | Muy baja | 2-3 piezas |
| MVP | Top básico sin mangas | Baja | 2-4 piezas |
| Fase 2 | Blusa / Camisa | Media | 5-8 piezas |
| Fase 2 | Vestido | Media-alta | 4-8 piezas |
| Fase 3 | Pantalón | Alta | 5-7 piezas |

---

## Flujo del MVP

```
[1] ONBOARDING
    Crear cuenta
    Subir tabla de medidas de la marca → o usar tabla estándar incluida

[2] UPLOAD
    Subir sketch, foto o referencia visual de la prenda

[3] RENDER
    IA analiza la imagen (Claude Vision)
    IA genera render fotorrealista (Flux / DALL-E 3)
    Usuario confirma o ajusta ("Más evasé", "Cuello más pronunciado")

[4] CONVERSACIÓN DE DISEÑO
    IA hace preguntas en lenguaje de diseño, no técnico:
    → "¿La falda es recta o evasé?"
    → "¿El cierre va en lateral o en la espalda?"
    → "¿Cuánto largo quieres aproximadamente?"
    → "¿Qué talla usamos como base?"

[5] PATRÓN
    Sistema selecciona bloque base correspondiente
    Aplica parámetros de la conversación
    Muestra preview 2D interactivo de las piezas

[6] EXPORT
    PDF → para modista local o corte manual
    DXF → para software industrial (AAMA/ASTM)
```

---

## Lo que NO está en el MVP

- Canvas de diseño propio (Fase 2)
- Visualización 3D (Fase 2)
- Más de 2 tipos de prenda
- Grading automático de tallas múltiples
- Colaboración en tiempo real
- API para terceros

---

## Criterio de Éxito del MVP

Un diseñador sin formación técnica puede subir un sketch, responder las preguntas de la IA y obtener un patrón exportable que un patronista considera un **punto de partida válido** — reduciendo la primera iteración de correcciones de días a minutos.

---

## Validación con Patronistas

Antes de lanzar, los bloques base necesitan ser validados por patronistas reales para garantizar que el output técnico es correcto. Este es el activo más crítico del MVP y debe construirse en paralelo al desarrollo.

**Proceso de validación:**
1. Definir bloques base para falda recta y top en tallas S/M/L/XL
2. Patronistas validan geometría, curvas, márgenes de costura
3. Tests con prendas físicas antes de activar exports para usuarios

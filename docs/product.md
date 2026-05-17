# Producto

## Usuario Objetivo (MVP)

**Diseñadores de marcas de moda pequeñas** que:
- No pueden permitirse contratar un patronista
- Tienen conocimiento de diseño pero no de patronaje técnico
- Están acostumbrados a herramientas digitales (la "generación Shopify" de la moda)
- Tienen tolerancia alta a probar herramientas nuevas si son accesibles y asequibles

No son patronistas. No son técnicos. Son creativos que necesitan que la tecnología hable su idioma.

---

## Filosofía de UX

**Referencia negativa: CLO3D**
- Interfaz compleja orientada a patronistas técnicos
- Curva de aprendizaje muy alta
- No está diseñado para diseñadores sin formación técnica

**Nuestra posición: lo contrario de CLO3D**
- Interfaz aesthetic, limpia y visual
- La IA guía al usuario — no al revés
- Lenguaje de diseño, no lenguaje técnico
- El usuario no necesita saber qué es una pinza para usar la app

---

## Principios de Diseño de Producto

1. **La IA pregunta, el diseñador responde** — nunca al revés
2. **Lenguaje visual primero** — render antes de patrón
3. **Cero jerga técnica** — "¿quieres que quede ajustado en la cintura?" no "¿dónde posicionas la pinza de busto?"
4. **Lo visual no es decorativo** — el render fotorrealista es funcional, valida antes de generar
5. **Simple por defecto, configurable si se necesita** — tallas estándar como punto de partida, tabla de medidas propia como opción

---

## Sistema de Medidas

Cada marca define su propia tabla de medidas porque las tallas no son universales — la M de una marca no es la M de otra.

**Flujo:**
- Al crear cuenta, la marca sube su tabla de medidas propia, O
- Usa la tabla estándar incluida como punto de partida y la ajusta

Esto es un diferenciador real: el sistema aprende las especificaciones de cada marca, no impone un estándar genérico.

---

## Flujo de Usuario Completo

```
1. Crear cuenta
   └── Subir tabla de medidas de la marca (o usar estándar)

2. Nueva prenda
   └── Subir sketch o referencia visual

3. Validación visual
   └── IA genera render fotorrealista
   └── "¿Es esto lo que buscas?" → ajustes si necesario

4. Conversación de diseño
   └── IA hace preguntas en lenguaje de diseño
   └── Tipo de prenda, silueta, escote, cierre, largo, etc.

5. Generación de patrón
   └── Preview 2D interactivo de las piezas del patrón

6. Export
   └── PDF (para modista local o corte manual)
   └── DXF (para software industrial)
```

---

## Roadmap de Producto

### MVP
- Subir diseño + render fotorrealista
- Chat conversacional de diseño
- Prendas: falda recta y top básico
- Export PDF + DXF

### Fase 2
- Canvas de diseño propio (diseñar directamente en la app)
- Más tipos de prenda (blusa, vestido, pantalón)
- Visualización 3D via Meshy API
- Historial de versiones

### Fase 3
- API B2B para integración con ERPs y PLMs
- Colaboración en tiempo real
- Fine-tuning con datos propios de producción
- Integraciones con CLO3D, Lectra, Gerber

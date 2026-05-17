# Riesgos y Decisiones

## Riesgos Identificados

### 1. Calidad del Patrón Output
**Riesgo:** Un patrón al 90% correcto puede ser inútil si el 10% restante son curvas críticas o márgenes de costura.

**Mitigación:**
- Bloques base validados por patronistas reales antes del lanzamiento
- El sistema genera a partir de bloques probados, no desde cero
- Feedback loop con patronistas para mejorar iterativamente

---

### 2. Competencia de CLO3D
**Riesgo:** CLO3D tiene distribución, datos y recursos para mejorar su UX y atacar nuestro mercado.

**Mitigación:**
- Velocidad de ejecución — establecer base de usuarios antes de que lo hagan bien
- Precio muy por debajo de CLO3D (~1,500-2,500€/año vs. nuestro modelo accesible)
- Foco en diseñadores no técnicos que CLO3D históricamente ha ignorado
- Tabla de medidas por marca como mecanismo de lock-in

---

### 3. El Diseñador No Sabe Lo Que No Sabe
**Riesgo:** Cuando la IA pregunte sobre decisiones técnicas, el diseñador puede no entenderlas.

**Mitigación:**
- Lenguaje de diseño puro — nunca terminología técnica de patronaje
- Preguntas cerradas con opciones visuales cuando sea posible
- La IA traduce intención ("ajustado en cintura") a parámetros técnicos internamente

---

### 4. Liability por Patrones Incorrectos
**Riesgo:** Si una marca corta 500 metros de tela con un patrón erróneo, el daño es enorme.

**Mitigación:**
- Términos de servicio claros — PatternAI genera puntos de partida, no patrones finales certificados
- Recomendación explícita en el UI de validar con una muestra antes de producción masiva
- En MVP, usuarios son marcas pequeñas con cortes limitados — el riesgo es menor

---

### 5. Datos de Entrenamiento
**Riesgo:** Para mejorar el modelo, necesitamos datos de sketch→patrón correcto que casi no existen en formato digital.

**Mitigación:**
- Construir el dataset propio desde el día uno — cada patrón generado y validado es un dato
- Los patronistas con acceso son el activo más valioso a largo plazo
- El modelo híbrido (Claude + bloques paramétricos) no requiere un gran dataset para el MVP

---

## Decisiones Tomadas y Razonamiento

| Decisión | Alternativa descartada | Por qué |
|----------|----------------------|---------|
| MVP solo falda y top | Más tipos de prenda | Calidad sobre cantidad — mejor 2 tipos perfectos |
| No 3D en MVP | Meshy API desde el inicio | 3D básico no reduce fitting; patrón bueno sí |
| Render fotorrealista como hook | Solo preview 2D | El visual es el diferenciador de UX, no decoración |
| Tallas estándar + tabla propia | Solo tallas estándar | Cada marca tiene sus propias especificaciones |
| Export PDF + DXF | Solo PDF | No limitar el mercado a corte manual desde el inicio |
| Python backend | Node.js backend | Ecosistema ML/AI es Python; FastAPI es moderno y rápido |

---

## Próximas Decisiones Pendientes

- [ ] Flux vs. DALL-E 3 para render (requiere pruebas de calidad en prendas)
- [ ] Modelo de precios (suscripción mensual vs. por uso vs. freemium)
- [ ] Idiomas del MVP (español primero, inglés simultáneo, o solo uno)
- [ ] Hosting inicial (Vercel + Railway vs. AWS desde el inicio)

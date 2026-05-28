# Polymarket Intelligence Engine — CLAUDE.md

---

## Rol de Claude Code en este proyecto

Eres un mentor técnico. Tu trabajo es guiarme paso a paso para que YO aprenda haciendo.

### División de responsabilidades

**Backend** — lo construyo yo. Claude me guía como mentor: explica, da tareas pequeñas, revisa, corrige.

**Frontend** — lo construye Claude completamente. Yo no aprendo frontend en este proyecto. Claude implementa todas las fases de frontend sin pedirme que intente nada.

### Cómo debes comportarte en el backend

**Nunca escribas código completo por mí sin que yo te lo indique.**

Cuando pida trabajar en algo:

1. Explícame brevemente qué vamos a hacer y por qué
2. Dime qué leer antes de empezar — sección específica, no "lee la doc" en caso de que sea necesario
3. Dame una tarea concreta y pequeña
4. Espera a que yo lo intente
5. Revisa lo que hice y dime específicamente qué está mal y por qué
6. Si está bien, confirma y dame la siguiente tarea

Si lo hago mal, dime exactamente dónde fallé y por qué. Sin rodeos.

### Lo que NO debes hacer (backend)

- No escribas implementaciones completas solo cuando yo lo pida
- No me des "aquí tienes el código listo"
- No asumas que entendí algo sin verificarlo
- No avances a la siguiente tarea si la anterior tiene problemas reales
- No uses frases vacías como "excelente trabajo" si hay errores — dime el error directamente

---

## El proyecto

Un motor de recolección y análisis de datos de mercados de predicción de Polymarket.

**Objetivo:** recolectar datos de múltiples fuentes, hacer ingeniería de datos, y eventualmente entrenar un modelo que identifique oportunidades en mercados de Polymarket.

**Contexto de negocio:** esto va a convertirse en una SaaS de 1-2 desarrolladores. Las decisiones técnicas deben favorecer velocidad de iteración y mantenibilidad sobre arquitectura perfecta.

---

## Fuentes de datos (en orden)

1. **Polymarket Gamma API** — metadata de mercados (precios, volumen, liquidez, estado)
2. **Polymarket CLOB API** — historial de precios por mercado
3. **Reddit API (PRAW)** — menciones y sentimiento vinculadas a mercados
4. **NewsAPI / TheNewsAPI** — noticias vinculadas a mercados
5. **Otras** — se definen cuando lleguemos
6. **Web Scrapping** — se definen cuando lleguemos a ellas

Cada fuente se implementa completa antes de pasar a la siguiente.

---

## Stack tecnológico

### Backend
- **Python 3.12+**
- **FastAPI** — API REST
- **SQLAlchemy 2.0** — ORM async (asyncpg como driver)
- **Alembic** — migraciones
- **PostgreSQL** — base de datos principal
- **Redis** — cache (fases posteriores)
- **Kafka** — streaming (fases posteriores)
- **httpx** — cliente HTTP
- **Pydantic v2** — validación y schemas

### Ingeniería de datos
- **pandas** — transformación y limpieza
- **Pandera** — validación de schemas de datos

### Testing
- **pytest** — solo donde agrega valor real
- **pytest-asyncio** — para tests con async/await
- **respx** — mock de HTTP en tests unitarios

### Frontend
- **Next.js 14** con App Router
- **TypeScript**
- **shadcn/ui + Tailwind**

### DevOps
- **Docker + Docker Compose**
- **GitHub Actions** — CI básico

---

## Estructura del proyecto

```
polymarket-intelligence/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   └── markets.py     # endpoints de FastAPI
│   │   │   └── deps.py            # dependencias compartidas (db session, etc)
│   │   ├── services/
│   │   │   └── markets.py         # lógica de negocio
│   │   ├── repositories/
│   │   │   └── markets.py         # queries a la DB
│   │   ├── models/
│   │   │   └── market.py          # SQLAlchemy models
│   │   ├── schemas/
│   │   │   └── market.py          # Pydantic schemas (request/response)
│   │   ├── ingestion/
│   │   │   ├── polymarket/
│   │   │   │   ├── gamma_client.py
│   │   │   │   └── clob_client.py
│   │   │   ├── reddit/
│   │   │   └── news/
│   │   ├── core/
│   │   │   ├── config.py          # settings con pydantic-settings
│   │   │   ├── database.py        # engine y sesión
│   │   │   └── logging.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_services/
│   │   └── test_api/
│   ├── alembic/
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── markets/
│   ├── components/
│   ├── lib/                       # clientes HTTP, utils
│   ├── types/
│   ├── public/
│   ├── next.config.ts
│   └── package.json
├── docker-compose.yml
└── CLAUDE.md
```

### La separación que importa

```
routes/        ← solo recibe requests y devuelve responses, sin lógica
services/      ← toda la lógica de negocio vive aquí
repositories/  ← solo habla con la DB, sin lógica de negocio
ingestion/     ← clientes externos y pipeline ETL, separados por fuente
models/        ← definición de tablas
schemas/       ← contratos de la API (lo que entra y sale)
```

**Regla práctica:** si un `route` tiene más de 5 líneas de lógica, esa lógica pertenece al `service`. Si un `service` tiene queries SQL, esas queries pertenecen al `repository`.

---

## Principios de desarrollo

### Lo que sí importa

**Nombres que explican intención**
`fetch_active_markets()` no `get_data()`. El nombre debe decir qué hace sin leer el cuerpo.

**Funciones con una responsabilidad**
Si necesitas "y" para describir lo que hace una función, probablemente hace demasiado.

**Sin valores hardcodeados**
URLs, credenciales, límites de paginación — todo en `core/config.py` via variables de entorno. Nunca en el código.

**Manejo de errores explícito**
`except Exception` sin logging y sin re-raise es un bug esperando ocurrir. Si capturas una excepción, haz algo útil con ella.

**Commits descriptivos**
`feat: add market price history endpoint` no `fix stuff`. Prefijos: `feat:`, `fix:`, `refactor:`, `chore:`.

### Tests — pragmáticos, no exhaustivos

No se hace TDD. Se escriben tests donde el riesgo de error es alto o la lógica es compleja.

**Escribe tests para:**
- Lógica de transformación de datos (el ETL)
- Servicios con lógica de negocio no trivial
- Endpoints críticos de la API

**No es prioritario testear:**
- Repositories simples (CRUD básico)
- Configuración
- Código que es obvio por su simplicidad

**Regla mínima:** si algo falló en producción o fue difícil de debuggear, escribe un test para ese caso.

### Pipeline ETL — no negociable

Cada dato que entra al sistema pasa por esto, sin importar la fuente:

```
1. Extracción     → obtener dato crudo de la fuente
2. Validación     → verificar schema con Pandera antes de procesar
3. Limpieza       → nulls, duplicados, tipos incorrectos
4. Transformación → forma útil para almacenamiento
5. Carga          → upsert en PostgreSQL, no insert ciego
6. Log            → registrar cuántos registros, anomalías encontradas
```

Esto no es arquitectura ceremonial — es lo que evita datos corruptos en la DB que son imposibles de debuggear después.

---

## Roadmap de fases

**Bloque 0 — Fundación**
- [ ] **Fase 0** — Estructura del proyecto, config, Docker con PostgreSQL

**Bloque 1 — Polymarket Gamma API**
- [ ] **Fase 1** — Cliente HTTP + ingesta de mercados activos + guardado en DB
- [ ] **Fase 2** — Pipeline ETL completo (validación, limpieza, upsert)
- [ ] **Fase 3** — FastAPI: endpoints que exponen los mercados
- [ ] **Fase 4** — Frontend v1: lista de mercados con precio y volumen

**Bloque 2 — Historial de precios (CLOB API)**
- [ ] **Fase 5** — Cliente CLOB + pipeline ETL de historial de precios
- [ ] **Fase 6** — Frontend v2: gráfico de precio histórico por mercado

**Bloque 3 — Sentimiento (Reddit)**
- [ ] **Fase 7** — Ingesta Reddit: menciones vinculadas a mercados
- [ ] **Fase 8** — Frontend v3: panel de sentimiento por mercado

**Bloque 4 — Noticias**
- [ ] **Fase 9** — Ingesta de noticias vinculadas a mercados
- [ ] **Fase 10** — Frontend v4: titulares recientes por mercado

**Bloque 5 — Escala**
- [ ] **Fase 11** — Redis: cache de endpoints
- [ ] **Fase 12** — Kafka: streaming de precios en tiempo real
- [ ] **Fase 13** — Frontend v5: precios en tiempo real

**Bloque 6 — Inteligencia**
- [ ] **Fase 14** — Feature engineering
- [ ] **Fase 15** — Modelo ML: señal de oportunidad por mercado
- [ ] **Fase 16** — Frontend v6: dashboard con señal del modelo

**Bloque 7 — Deployment**
- [ ] **Fase 17** — Producción con CI/CD y monitoreo básico

> No avanzar de bloque si hay deuda técnica que va a escalar el problema.
> El frontend de cada bloque consume solo lo que el backend de ese bloque expone.

---

## Señales de alerta — advertirme si

- Un dato va de la API directo a la DB sin pasar por el pipeline ETL
- Un `route` tiene lógica de negocio que debería estar en `service`
- Un `service` tiene queries SQL que deberían estar en `repository`
- Hay `except Exception` sin logging ni manejo específico
- Hay valores hardcodeados que deberían estar en `config.py`
- Una función o variable tiene un nombre que no explica su intención
- Se está añadiendo tecnología nueva sin haber terminado la fase actual
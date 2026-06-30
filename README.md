# EVsphere‑Twin

## One‑stop Digital Twin Platform for the EV Ecosystem

**EVSphere‑Twin** is a premium, end‑to‑end simulation and monitoring solution for electric‑vehicle supply‑chain networks. It combines a Neo4j graph backend, a TimescaleDB time‑series store, and a Flask‑driven web portal to deliver:

- **Real‑time topology view** (Cytoscape.js) of suppliers, batteries, vehicles, chargers, and service centers.
- **Geospatial intelligence** (Leaflet) with live charger and service‑center locations.
- **AI/ML‑driven risk prediction** – LightGBM, XGBoost, CatBoost models to forecast component failures and revenue impact.
- **Interactive cascade simulation** – Sankey‑style propagation of failures across the supply chain.
- **Export suite** – One‑click download of data in JSON, CSV, GraphML, Cypher, and PNG.
- **Docker‑Compose stack** – PostgreSQL, TimescaleDB, Neo4j, and the Flask web service, all reproducible across environments.

---

## Architecture Overview

```
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│   PostgreSQL +      │   │   TimescaleDB       │   │   Neo4j Graph DB    │
│   TimescaleDB       │   │   (time‑series)    │   │   (supply‑chain)   │
└─────────┬───────────┘   └─────────┬───────────┘   └─────────┬───────────┘
          │                         │                         │
          │                         │                         │
          ▼                         ▼                         ▼
       ┌───────────────────────────────────────────────────────┐
       │               Flask Web Service (Python)            │
       │  - API endpoints: /api/graph, /api/map, /api/predict │
       │  - Jinja2 templates: index, graph, map, digital‑twin│
       │  - Authentication placeholder (middleware/auth.py) │
       └───────────────────────────────────────────────────────┘
                         │            │            │
          ┌──────────────┘            │            └───────────────
          ▼                           ▼                            ▼
   ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
   │   UI Front‑ │            │   UI Front‑ │            │   UI Front‑ │
   │   end (HTML│            │   end (HTML│            │   end (HTML│
   │   + CSS +   │            │   + CSS +   │            │   + CSS +   │
   │   JS)       │            │   JS)       │            │   JS)       │
   └─────────────┘            └─────────────┘            └─────────────┘
```

---

## Core Use‑Cases

| Use‑Case | Description | Impact |
|----------|-------------|--------|
| **Supply‑Chain Visibility** | Visualise every node and relationship in real time. | Faster root‑cause analysis. |
| **Failure Impact Simulation** | Select a seed node, set probability & depth, see cascading effects. | Proactive risk mitigation, revenue loss estimation. |
| **Geospatial Monitoring** | Map charger density, service‑center coverage, factory locations. | Optimise deployment planning. |
| **AI‑Powered Forecasting** | Predict component failure probability using trained models. | Reduce downtime, improve maintenance scheduling. |
| **Data Export & Integration** | Download the full graph in multiple formats for downstream tools. | Seamless integration with BI/Analytics pipelines. |

---

## Getting Started (Local Development)

1. **Clone the repo**
   ```bash
   git clone https://github.com/Aditya-Ranjan1234/EVsphere‑Twin.git
   cd EVsphere‑Twin
   ```
2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   .\\venv\\Scripts\\activate   # Windows PowerShell
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env to set your DB URLs, MAPBOX token, etc.
   ```
4. **Start the Docker stack** (requires Docker Desktop)
   ```bash
   python scripts/docker_show_info.py   # review image sizes, approve pull
   docker-compose up -d
   ```
5. **Run the Flask server**
   ```bash
   python -m src.flask_app.app
   ```
6. **Open the portal**
   Visit `http://127.0.0.1:5000` in your browser.

---

## Deployment on Vercel (Server‑less)

1. **Add a Vercel project** pointing to the repository root.
2. **Create a `vercel.json`** (already included) that builds the Flask app using a serverless function.
3. **Set the required environment variables** in the Vercel dashboard (copy from `.env`).
4. **Deploy** – Vercel will run `pip install -r requirements.txt` and launch the Flask server.
5. **Optional** – Enable the Docker‑Compose stack on a separate VPS if you need the full Neo4j/TimescaleDB stack; otherwise, switch to Vercel‑hosted PostgreSQL and a hosted Neo4j service.

---

## Project Structure

```
EVsphere‑Twin/
│   README.md               # ← this file
│   .gitignore
│   docker-compose.yml
│   requirements.txt
│   setup_env.bat
│
├─src/
│   ├─flask_app/
│   │   ├─static/ (css, js)
│   │   ├─templates/ (HTML Jinja2)
│   │   ├─api.py   # REST endpoints
│   │   ├─app.py   # Flask entry point
│   │   └─routes.py
│   └─graph/      # Neo4j helper layer
│       ├─db.py
│       ├─graph_builder.py
│       └─impact_engine.py
│
├─scripts/
│   ├─docker_show_info.py   # image review before pull
│   └─download_datasets.py
│
├─tests/        # pytest suite
└─docker/       # data volumes for DB containers
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome‑feature`).
3. Write tests and ensure the CI pipeline passes.
4. Open a Pull Request.

---

## License

Open‑source under the MIT License.

---

*Built with love, glass‑morphism UI, Inter font, and a vibrant HSL colour palette for a premium experience.*

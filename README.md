# Asana Data Simulation Generator

A high-fidelity, scalable generator for creating realistic seed data for an Asana-like Reinforcement Learning (RL) environment.

## 🚀 Overview

This project simulates the data ecosystem of a mid-sized B2B SaaS company, **"TechFlow Solutions"**. It procedurally generates a complete Organization graph—including Users, Teams, Projects, Tasks, Comments, and Custom Fields—specifically designed to train and evaluate AI agents on complex project management workflows.

**Key Features:**
*   **High Scalability**: capable of generating 10,000+ entities efficiently.
*   **Hybrid Intelligence**: Uses a combination of **Llama 3 (via Groq)** and statistical heuristics to create data that looks and feels real.
*   **Relational Integrity**: Strictly enforces business logic (e.g., users are only assigned to projects within their teams).
*   **Temporal Realism**: Simulates a 6-month history with realistic work patterns (weekday clusters, creating vs. completion lag).

---

## 🧠 Methodology

### Data Generation Strategy
The system uses a **tiered approach** to balance quality and performance:

1.  **Tier 1: Statistical Backbone (Heuristics)**
    *   Used for: Dates, Statuses, Relationships.
    *   Logic: Weighted randoms based on real-world benchmarks (e.g., 85% of tasks due on weekdays, 15% unassigned backlog rate).

2.  **Tier 2: Semantic Layer (Templates)**
    *   Used for: Project names, standard tasks.
    *   Logic: Domain-specific templates derived from GitHub issues (e.g., `[Backend] Refactor API`).

3.  **Tier 3: Creative Layer (LLM/Groq)**
    *   Used for: Unique task descriptions, specific comments.
    *   Logic: "Few-shot" prompting to generate context-aware content (e.g., "Fix race condition in Auth service").

### Database Schema
The data is modeled in **SQLite** with strict foreign keys to ensure data validity. Key design patterns include:
*   **EAV (Entity-Attribute-Value)**: For flexible Custom Fields on tasks.
*   **Self-Referencing Tasks**: For infinite subtask hierarchy.
*   **Many-to-Many Memberships**: For Users belonging to multiple Teams.

---

## 🛠 Project Structure

```bash
├── README.md                    # You are here
├── requirements.txt             # Dependencies (Faker, Groq, etc.)
├── schema.sql                   # Complete SQLite DDL (13 tables)
├── .env.example                 # Config template
├── src/
│   ├── main.py                  # 🚀 Entry Point / Orchestrator
│   ├── scrapers/                # Modules for external data
│   ├── generators/              # 🏭 Logic for generating entities
│   │   ├── users.py             # Users & Teams
│   │   ├── projects.py          # Projects & Sections
│   │   ├── tasks.py             # Tasks & Subtasks (LLM-integrated)
│   │   ├── comments.py          # Activity Feed
│   │   ├── custom_fields.py     # EAV Pattern implementation
│   │   └── tags.py              # Metadata
│   ├── utils/
│   │   ├── db.py                # Database helpers
│   │   └── llm_helper.py        # Groq API wrapper with fallbacks
│   └── models/                  # Data models
├── prompts/                     # LLM System Prompts
└── output/
    └── asana_simulation.sqlite  # 💾 Final Database Artifact
```

---

## ⚡ Quick Start

### 1. Prerequisities
*   (Optional) A free **Groq API Key** for high-quality text generation.

### 2. Installation

```bash
# Clone the repository (if applicable)
# git clone ...

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file to control the scale of the simulation:

```ini
# .env
DB_PATH=output/asana_simulation.sqlite

# Scale configuration
SEED_COUNT_USERS=50
SEED_COUNT_PROJECTS=20
SEED_COUNT_TASKS_PER_PROJECT=15

# (Optional) For LLM-powered text generation
# GROQ_API_KEY=gsk_...
```

### 4. Run the Generator

```bash
python -m src.main
```

You will see the generation progress in the terminal. The final result will be saved to `output/asana_simulation.sqlite`.

---

## 🔍 Verification

To inspect the generated data, you can use any SQLite viewer or run the python checker (if provided):

```python
import sqlite3
# Example check
conn = sqlite3.connect("output/asana_simulation.sqlite")
print(conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0])
```


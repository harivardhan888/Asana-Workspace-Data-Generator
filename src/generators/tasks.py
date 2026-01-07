import uuid
import random
import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Heuristics for Task Names
COMPONENTS = ["Auth Service", "Payment Gateway", "User Profile", "Dashboard", "API Docs", "Mobile Nav", "Search Index"]
ACTIONS = ["Refactor", "Implement", "Fix", "Update", "Optimize", "Deprecate"]
DETAILS = ["race condition", "memory leak", "UI glitch", "responsiveness", "latency issues", "error handling"]

MARKETING_CAMPAIGNS = ["Q1 Launch", "Black Friday", "Summer Sale", "Rebranding"]
MARKETING_DELIVERABLES = ["Email Copy", "Social Assets", "Landing Page", "Ad Creatives", "Blog Post"]

def generate_task_name(project_context="Engineering"):
    if "Engineering" in project_context or "Web" in project_context:
        return f"{random.choice(COMPONENTS)} - {random.choice(ACTIONS)} - {random.choice(DETAILS)}"
    elif "Marketing" in project_context:
        return f"{random.choice(MARKETING_CAMPAIGNS)} - {random.choice(MARKETING_DELIVERABLES)}"
    else:
        return fake.sentence(nb_words=4).replace(".", "")

from src.utils.llm_helper import generate_task_content_hybrid

def generate_tasks(conn, project_ids, user_ids, num_tasks_per_project=15):
    cursor = conn.cursor()
    
    # Pre-fetch sections
    project_sections = {} # project_id -> [section_ids]
    cursor.execute("SELECT project_id, section_id FROM sections")
    for row in cursor.fetchall():
        if row['project_id'] not in project_sections:
            project_sections[row['project_id']] = []
        project_sections[row['project_id']].append(row['section_id'])
        
    total_tasks = 0
    print(f"Starting task generation for {len(project_ids)} projects...")
    
    # Need to get project names for context
    project_names = {}
    cursor.execute("SELECT project_id, name, team_id FROM projects")
    for row in cursor.fetchall():
        project_names[row['project_id']] = (row['name'], "Engineering") # Default to Eng for simple team lookup
        
    for project_id in project_ids:
        # Determine context
        proj_name, team_name = project_names.get(project_id, ("Project", "General"))
        
        sections = project_sections.get(project_id, [])
        if not sections:
            continue
            
        for _ in range(num_tasks_per_project):
            task_id = str(uuid.uuid4())
            
            # Hybrid generation: LLM or Heuristics
            name, description = generate_task_content_hybrid(proj_name, team_name)
            
            section_id = random.choice(sections)
            assignee_id = random.choice(user_ids) if random.random() > 0.15 else None # 15% unassigned
            
            # Dates
            created_delta = random.randint(1, 60)
            created_at = datetime.now() - timedelta(days=created_delta)
            
            due_delta = random.randint(-5, 30) # Some overdue
            due_date = created_at + timedelta(days=created_delta + due_delta)
            
            completed = random.random() > 0.4
            completed_at = None
            if completed:
                # Completed 1-10 days after creation
                comp_delta = random.randint(1, 10)
                completed_at = created_at + timedelta(days=comp_delta)
                # Ensure it's before now
                if completed_at > datetime.now():
                     completed_at = datetime.now()
            
            cursor.execute("""
                INSERT INTO tasks (task_id, name, description, project_id, section_id, assignee_id, due_date, completed, completed_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_id, name, description, project_id, section_id, assignee_id, due_date.date(), completed, completed_at, created_at))
            
            total_tasks += 1
            
            if total_tasks % 1000 == 0:
                print(f"Generated {total_tasks} tasks...")
                conn.commit() # Periodic commit
            
    conn.commit()
    print(f"Generated {total_tasks} tasks.")

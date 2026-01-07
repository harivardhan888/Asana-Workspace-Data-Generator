import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

PROJECT_TEMPLATES = {
    "Engineering": ["Backend Migration", "API Refactor", "Mobile App v2", "Bug Bash Q1", "Infrastructure Upgrade"],
    "Product": ["Q1 Roadmap", "User Research", "Feature Spec: Analytics", "Competitor Analysis"],
    "Design": ["Design System v2", "Marketing Assets", "Homepage Redesign"],
    "Marketing": ["Social Media Campaign", "Webinar Series", "Q1 Newsletter", "Content Calendar"],
    "Sales": ["Outbound Strategy", "Lead Qualification Process", "CRM Cleanup"],
    "HR": ["Employee Onboarding", "Performance Review Cycle", "Hiring Pipeline"],
    "Operations": ["Office Move", "Vendor Audit", "Budget Planning"]
}

SECTIONS_TEMPLATE = {
    "Engineering": ["Backlog", "To Do", "In Progress", "Code Review", "QA", "Done"],
    "Default": ["To Do", "In Progress", "Done"]
}

def generate_projects(conn, team_ids_map, user_ids, num_projects=20):
    cursor = conn.cursor()
    project_ids = []
    
    # Get users by team to assign owners correctly (simplification: assume random user is fine for now, or fetch membership)
    # Better: fetch valid team members
    
    generated_count = 0
    
    teams = list(team_ids_map.keys())
    
    for _ in range(num_projects):
        team_name = random.choice(teams)
        team_id = team_ids_map[team_name]
        
        # Pick a project name appropriate for the team
        if team_name in PROJECT_TEMPLATES:
            proj_name = random.choice(PROJECT_TEMPLATES[team_name])
        else:
            proj_name = f"{team_name} Initiative"
            
        project_id = str(uuid.uuid4())
        owner_id = random.choice(user_ids) # Simplification: random user as owner
        status = random.choice(["On Track", "At Risk", "Off Track", "On Hold"])
        
        # Dates
        created_delta = random.randint(1, 180)
        created_at = datetime.now() - timedelta(days=created_delta)
        due_delta = random.randint(10, 60)
        due_date = created_at + timedelta(days=due_delta)
        
        cursor.execute(
            """INSERT INTO projects 
               (project_id, name, description, team_id, owner_id, status, due_date, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (project_id, proj_name, fake.catch_phrase(), team_id, owner_id, status, due_date.date(), created_at)
        )
        
        # Generate Sections for the project
        sections = SECTIONS_TEMPLATE.get(team_name, SECTIONS_TEMPLATE["Default"])
        for i, section_name in enumerate(sections):
            section_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO sections (section_id, project_id, name, list_order) VALUES (?, ?, ?, ?)",
                (section_id, project_id, section_name, i)
            )
            
        project_ids.append(project_id)
        generated_count += 1
        
    conn.commit()
    print(f"Generated {generated_count} projects and their sections.")
    return project_ids

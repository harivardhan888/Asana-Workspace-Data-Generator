import uuid
import random
from faker import Faker

fake = Faker()

TEAMS = [
    ("Engineering", "Building the core platform"),
    ("Product", " defining product strategy"),
    ("Design", "UI/UX and brand"),
    ("Marketing", "Growth and acquisition"),
    ("Sales", "Revenue generation"),
    ("Customer Success", "Support and retention"),
    ("HR", "People and culture"),
    ("Operations", "Internal processes")
]

ROLES = ["Admin", "Member", "Guest"]

def generate_teams(conn, workspace_id):
    cursor = conn.cursor()
    team_ids = {}
    
    for name, desc in TEAMS:
        team_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO teams (team_id, name, description, workspace_id) VALUES (?, ?, ?, ?)",
            (team_id, name, desc, workspace_id)
        )
        team_ids[name] = team_id
        
    conn.commit()
    print(f"Generated {len(TEAMS)} teams.")
    return team_ids

def generate_users(conn, workspace_id, num_users=50):
    cursor = conn.cursor()
    user_ids = []
    seen_emails = set()
    
    generated = 0
    while generated < num_users:
        user_id = str(uuid.uuid4())
        profile = fake.profile()
        name = profile['name']
        email = profile['mail']
        
        if email in seen_emails:
            # Modify email to be unique
            email = f"{email.split('@')[0]}_{random.randint(1000, 9999)}@{email.split('@')[1]}"
            if email in seen_emails:
                continue

        seen_emails.add(email)
        role = random.choices(ROLES, weights=[5, 90, 5])[0] # Mostly members
        
        cursor.execute(
            "INSERT INTO users (user_id, email, name, role, workspace_id) VALUES (?, ?, ?, ?, ?)",
            (user_id, email, name, role, workspace_id)
        )
        user_ids.append(user_id)
        generated += 1
        
        if generated % 1000 == 0:
            print(f"Generated {generated} users...")
            conn.commit()
            
    conn.commit()
    print(f"Generated {num_users} users.")
    return user_ids

def assign_users_to_teams(conn, user_ids, team_ids_map):
    cursor = conn.cursor()
    team_ids = list(team_ids_map.values())
    
    assignments = 0
    for user_id in user_ids:
        # Assign each user to 1-3 teams
        num_teams = random.randint(1, 3)
        assigned_teams = random.sample(team_ids, k=num_teams)
        
        for team_id in assigned_teams:
            cursor.execute(
                "INSERT OR IGNORE INTO team_memberships (team_id, user_id) VALUES (?, ?)",
                (team_id, user_id)
            )
            assignments += 1
            
    conn.commit()
    print(f"Generated {assignments} team memberships.")

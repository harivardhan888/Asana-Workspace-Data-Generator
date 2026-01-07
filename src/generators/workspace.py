import uuid
from faker import Faker

fake = Faker()

def generate_workspace(conn):
    """
    Generates the main organization workspace.
    """
    cursor = conn.cursor()
    
    workspace_id = str(uuid.uuid4())
    name = "TechFlow Solutions" # Example SaaS Company
    domain = "techflow.example.com"
    
    cursor.execute(
        "INSERT INTO workspaces (workspace_id, name, domain) VALUES (?, ?, ?)",
        (workspace_id, name, domain)
    )
    conn.commit()
    print(f"Generated Workspace: {name} ({workspace_id})")
    return workspace_id

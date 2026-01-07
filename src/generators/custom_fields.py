import uuid
import random
import json

FIELD_TYPES = {
    "Priority": {"type": "enum", "options": ["High", "Medium", "Low"]},
    "Estimated Hours": {"type": "number", "options": None},
    "Stage": {"type": "enum", "options": ["Discovery", "Development", "Testing", "Deployment"]},
    "Risk Level": {"type": "enum", "options": ["Critical", "High", "Moderate", "Low"]},
    "Cost Center": {"type": "text", "options": None}
}

def generate_custom_definitions(conn, workspace_id):
    cursor = conn.cursor()
    field_ids = {} # name -> id
    
    for name, meta in FIELD_TYPES.items():
        field_id = str(uuid.uuid4())
        options = json.dumps(meta["options"]) if meta["options"] else None
        
        cursor.execute(
            "INSERT INTO custom_field_definitions (field_id, workspace_id, name, type, options) VALUES (?, ?, ?, ?, ?)",
            (field_id, workspace_id, name, meta["type"], options)
        )
        field_ids[name] = field_id
        
    conn.commit()
    print(f"Generated {len(field_ids)} custom field definitions.")
    return field_ids

def associate_custom_fields_to_projects(conn, project_ids, field_ids_map):
    cursor = conn.cursor()
    count = 0
    
    # Priority is on almost all projects
    priority_id = field_ids_map.get("Priority")
    
    for project_id in project_ids:
        # Add Priority
        if priority_id:
            cursor.execute("INSERT OR IGNORE INTO project_custom_fields (project_id, field_id) VALUES (?, ?)", (project_id, priority_id))
        
        # Add 1-2 other random fields
        other_fields = [fid for name, fid in field_ids_map.items() if name != "Priority"]
        selected = random.sample(other_fields, k=random.randint(0, 2))
        
        for fid in selected:
            cursor.execute("INSERT OR IGNORE INTO project_custom_fields (project_id, field_id) VALUES (?, ?)", (project_id, fid))
            count += 1
            
    conn.commit()
    print(f"Associated custom fields to projects.")

def generate_custom_field_values(conn):
    """
    Populates custom_field_values for tasks based on their project's fields.
    """
    cursor = conn.cursor()
    
    # 1. Get all tasks and their projects
    cursor.execute("SELECT task_id, project_id FROM tasks")
    tasks = cursor.fetchall()
    
    # 2. Get map of Project -> [Fields] and Field definitions
    cursor.execute("""
        SELECT pcf.project_id, cfd.field_id, cfd.type, cfd.options
        FROM project_custom_fields pcf
        JOIN custom_field_definitions cfd ON pcf.field_id = cfd.field_id
    """)
    proj_fields = {} # project_id -> list of (field_id, type, options)
    for row in cursor.fetchall():
        if row['project_id'] not in proj_fields:
            proj_fields[row['project_id']] = []
        proj_fields[row['project_id']].append((row['field_id'], row['type'], row['options']))
        
    generated_count = 0
    
    for task in tasks:
        t_id = task['task_id']
        p_id = task['project_id']
        
        fields = proj_fields.get(p_id, [])
        for f_id, f_type, f_options in fields:
            value = None
            if f_type == 'enum':
                opts = json.loads(f_options)
                value = random.choice(opts)
            elif f_type == 'number':
                value = str(random.randint(1, 20))
            elif f_type == 'text':
                value = "Cost Center " + str(random.randint(100, 999))
            
            if value:
                cursor.execute(
                    "INSERT INTO custom_field_values (task_id, field_id, value) VALUES (?, ?, ?)",
                    (t_id, f_id, value)
                )
                generated_count += 1
                
    conn.commit()
    print(f"Generated {generated_count} custom field values.")

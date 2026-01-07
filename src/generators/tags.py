import uuid
import random

TAGS = ["Urgent", "Bug", "Feature", "Q1", "Blocked", "Needs Review", "Customer Request"]
COLORS = ["red", "orange", "blue", "green", "purple", "yellow", "gray"]

def generate_tags(conn, workspace_id):
    cursor = conn.cursor()
    tag_ids = []
    
    for name in TAGS:
        tag_id = str(uuid.uuid4())
        color = random.choice(COLORS)
        
        cursor.execute(
            "INSERT INTO tags (tag_id, workspace_id, name, color) VALUES (?, ?, ?, ?)",
            (tag_id, workspace_id, name, color)
        )
        tag_ids.append(tag_id)
        
    conn.commit()
    print(f"Generated {len(tag_ids)} tags.")
    return tag_ids

def assign_tags_to_tasks(conn, tag_ids):
    cursor = conn.cursor()
    
    cursor.execute("SELECT task_id FROM tasks")
    tasks = cursor.fetchall()
    
    count = 0
    for task in tasks:
        if random.random() > 0.8: # 20% of tasks have tags
            selected_tag = random.choice(tag_ids)
            cursor.execute(
                "INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (?, ?)",
                (task['task_id'], selected_tag)
            )
            count += 1
            
    conn.commit()
    print(f"Assigned {count} tags to tasks.")

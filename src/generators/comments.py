import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

COMMENTS = [
    "Looked into this, seems tricky.",
    "Can you clarify the requirements?",
    "Done. Ready for review.",
    "Blocked by API downtime.",
    "LGTM!",
    "Please update the docs.",
    "Deploying to staging now.",
    "Fixing a typo.",
    "Meeting reschedule?"
]

def generate_comments(conn, user_ids):
    cursor = conn.cursor()
    
    cursor.execute("SELECT task_id, created_at, completed_at FROM tasks")
    tasks = cursor.fetchall()
    
    generated_count = 0
    
    for task in tasks:
        # 30% chance of comment
        if random.random() > 0.7:
            num_comments = random.randint(1, 3)
            current_time = datetime.strptime(task['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            
            for _ in range(num_comments):
                story_id = str(uuid.uuid4())
                text = random.choice(COMMENTS) if random.random() > 0.5 else fake.sentence()
                user_id = random.choice(user_ids)
                
                # Comment time
                current_time += timedelta(hours=random.randint(1, 48))
                if current_time > datetime.now():
                    break
                    
                cursor.execute(
                    "INSERT INTO stories (story_id, task_id, user_id, text, type, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (story_id, task['task_id'], user_id, text, 'comment', current_time)
                )
                generated_count += 1
                
    conn.commit()
    print(f"Generated {generated_count} comments.")

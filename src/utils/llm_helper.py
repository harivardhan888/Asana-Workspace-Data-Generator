import os
import random
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()

client = None
if os.getenv("GROQ_API_KEY"):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Backup static pool if API fails or is not provided
BACKUP_TASK_NAMES = [
    "Refactor login page", "Update API documentation", "Fix CSS bug on mobile", 
    "Database migration", "Implement dark mode", "Write unit tests", "Client meeting preparation"
]

BACKUP_DESCRIPTIONS = [
    "Please look into this ASAP.", "See attached screenshot for details.", 
    "Customer reported this issue yesterday.", "Blocking the Q3 release."
]

def generate_text_with_llm(prompt_template, context_dict, max_tokens=60):
    """
    Generates text using Groq API (Llama 3 8b)
    """
    if not client:
        return None

    try:
        # Construct prompt
        prompt = prompt_template.format(**context_dict)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant generating seed data for a project management tool. Return only the requested text, no chatter."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=max_tokens,
        )
        return chat_completion.choices[0].message.content.strip().strip('"')
    except Exception as e:
        print(f"LLM Generation Failed: {e}")
        return None

def generate_task_content_hybrid(project_name, team_name):
    """
    Tries to generate task name/desc via LLM, falls back to templates
    """
    
    # 50% chance to use LLM if available to save rate limits/time for 10k items
    # (For 10,000 items, we might want to batch or rely more on templates)
    if client and random.random() > 0.8: # Only 20% LLM for speed on 10k items
        prompt = f"Generate a realistic task name for a '{team_name}' team working on '{project_name}'. Max 6 words."
        name = generate_text_with_llm(prompt, {})
        
        desc_prompt = f"Generate a 1-sentence description for a task named '{name}'. Max 15 words."
        description = generate_text_with_llm(desc_prompt, {})
        
        if name:
            return name, description if description else "See details."
            
    # Fallback
    base = random.choice(BACKUP_TASK_NAMES)
    return f"{project_name} - {base} {random.randint(1, 999)}", random.choice(BACKUP_DESCRIPTIONS)

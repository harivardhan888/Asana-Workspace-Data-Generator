import os
import sqlite3

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("Asana Data Simulation Generator Starting...")
    
    db_path = os.getenv("DB_PATH", "output/asana_simulation.sqlite")
    
    # ensure output directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    print(f"Database will be created at: {db_path}")

    # Initialize Database
    from src.utils.db import init_db, get_db_connection
    init_db(db_path=db_path)
    
    conn = get_db_connection(db_path)

    # Import Generators
    from src.generators import (
        generate_workspace,
        generate_teams,
        generate_users,
        assign_users_to_teams,
        generate_projects,
        generate_custom_definitions,
        associate_custom_fields_to_projects,
        generate_custom_field_values,
        generate_tasks,
        generate_comments,
        generate_tags,
        assign_tags_to_tasks
    )

    try:
        # 1. Workspace
        workspace_id = generate_workspace(conn)
        
        # 2. Users & Teams
        num_users = int(os.getenv("SEED_COUNT_USERS", 50))
        team_ids_map = generate_teams(conn, workspace_id)
        user_ids = generate_users(conn, workspace_id, num_users=num_users)
        assign_users_to_teams(conn, user_ids, team_ids_map)
        
        # 3. Custom Definitions & Tags
        field_ids_map = generate_custom_definitions(conn, workspace_id)
        tag_ids = generate_tags(conn, workspace_id)
        
        # 4. Projects
        num_projects = int(os.getenv("SEED_COUNT_PROJECTS", 20))
        project_ids = generate_projects(conn, team_ids_map, user_ids, num_projects=num_projects)
        associate_custom_fields_to_projects(conn, project_ids, field_ids_map)
        
        # 5. Tasks
        num_tasks = int(os.getenv("SEED_COUNT_TASKS_PER_PROJECT", 15))
        generate_tasks(conn, project_ids, user_ids, num_tasks_per_project=num_tasks)
        
        # 6. Post-Task Logic
        generate_custom_field_values(conn)
        generate_comments(conn, user_ids)
        assign_tags_to_tasks(conn, tag_ids)
        
        print("\nSimulation Data Generation Complete!")
        
    except Exception as e:
        print(f"An error occurred during generation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()

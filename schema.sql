-- Enable Foreign Keys
PRAGMA foreign_keys = ON;

-- 1. Workspaces / Organizations
CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id TEXT PRIMARY KEY, -- UUID
    name TEXT NOT NULL,
    domain TEXT, -- for organizations
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY, -- UUID
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    avatar_url TEXT,
    role TEXT, -- Admin, Member, Guest
    workspace_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

-- 3. Teams
CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY, -- UUID
    name TEXT NOT NULL,
    description TEXT,
    workspace_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

-- 4. Team Memberships
CREATE TABLE IF NOT EXISTS team_memberships (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT DEFAULT 'Member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 5. Projects
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY, -- UUID
    name TEXT NOT NULL,
    description TEXT,
    team_id TEXT NOT NULL,
    owner_id TEXT, -- Project owner
    status TEXT, -- On Track, At Risk, Off Track
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archived BOOLEAN DEFAULT 0,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- 6. Sections (Columns in Board view, or Sections in List view)
CREATE TABLE IF NOT EXISTS sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    list_order INTEGER NOT NULL, -- To maintain order
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- 7. Tasks
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY, -- UUID
    name TEXT NOT NULL,
    description TEXT,
    project_id TEXT NOT NULL,
    section_id TEXT, -- Can be null if not in a specific section (though usually is in 'Untitled')
    assignee_id TEXT,
    parent_task_id TEXT, -- For subtasks relationships
    due_date DATE,
    completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id)
);

-- 8. Comments / Stories (Activity Feed)
CREATE TABLE IF NOT EXISTS stories (
    story_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT, -- User who created the story (can be null for system messages)
    text TEXT,
    type TEXT, -- 'comment', 'system' (e.g., "marked complete")
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 9. Tags
CREATE TABLE IF NOT EXISTS tags (
    tag_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

-- 10. Task Tags
CREATE TABLE IF NOT EXISTS task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- 11. Custom Field Definitions
CREATE TABLE IF NOT EXISTS custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- 'text', 'number', 'enum', 'date'
    options TEXT, -- JSON string for enum options
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

-- 12. Project Custom Fields (Association: which projects use which fields)
CREATE TABLE IF NOT EXISTS project_custom_fields (
    project_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    PRIMARY KEY (project_id, field_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id)
);

-- 13. Custom Field Values
CREATE TABLE IF NOT EXISTS custom_field_values (
    task_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    value TEXT, -- Stored as string, cast based on definition type
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (task_id, field_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id)
);

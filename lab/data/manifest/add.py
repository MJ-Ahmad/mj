#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime

DATA_FILE = "data.json"


def now():
    return datetime.now().isoformat()


def create_project_structure(project_name, tree_content):

    timestamp = now()

    return {
        "mj-ahmad": {

            "manifest": {
                "schema_version": "1.0.0",
                "created_at": timestamp,
                "updated_at": timestamp,
                "owner": "MJ Ahmad",
                "organization": "",
                "license": "",
                "project_type": "",
                "status": "active"
            },

            "project": {
                "name": project_name,
                "short_name": project_name.lower().replace(" ", "-"),
                "description": "",
                "mission": "",
                "vision": "",
                "goals": [],
                "main_language": "",
                "repository": "",
                "homepage": "",
                "version": "1.0.0"
            },

            "ai_context": {
                "system_overview": "",
                "architecture_summary": "",
                "key_modules": [],
                "known_problems": [],
                "future_plans": [],
                "coding_standards": [],
                "important_notes": []
            },

            "tree": {
                "source": "",
                "content": tree_content
            },

            "directories": {},

            "files": {},

            "dependencies": {
                "python": [],
                "node": [],
                "dotnet": [],
                "system": []
            },

            "database": {
                "engine": "",
                "connection": "",
                "schemas": {},
                "tables": {},
                "views": {},
                "procedures": {}
            },

            "api": {
                "base_url": "",
                "routes": {},
                "middlewares": {},
                "authentication": {}
            },

            "environment": {
                "variables": {},
                "required": [],
                "optional": []
            },

            "deployment": {
                "docker": {},
                "nginx": {},
                "apache": {},
                "systemd": {},
                "hosting": {}
            },

            "documentation": {
                "readme": "",
                "installation": "",
                "configuration": "",
                "usage": "",
                "architecture": "",
                "developer_notes": ""
            },

            "tasks": {
                "todo": [],
                "in_progress": [],
                "completed": []
            },

            "issues": {
                "open": [],
                "closed": []
            },

            "roadmap": {
                "phase_1": [],
                "phase_2": [],
                "phase_3": []
            },

            "history": [
                {
                    "date": timestamp,
                    "version": "1.0.0",
                    "author": "MJ Ahmad",
                    "action": "Project created"
                }
            ],

            "contacts": {
                "owner": {
                    "name": "MJ Ahmad",
                    "email": "",
                    "phone": "",
                    "website": ""
                },

                "contributors": []
            },

            "notes": []
        }
    }


def save_json(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def main():

    if len(sys.argv) != 3:

        print("")
        print("Usage:")
        print("")
        print('python3 add.py "Project Name" tree.txt')
        print("")
        sys.exit(1)

    project_name = sys.argv[1]
    tree_file = sys.argv[2]

    if not os.path.exists(tree_file):
        print(f"Tree file not found: {tree_file}")
        sys.exit(1)

    with open(tree_file, "r", encoding="utf-8") as f:
        tree_content = f.read()

    data = create_project_structure(
        project_name,
        tree_content
    )

    save_json(data)

    print("")
    print("✅ Project Manifest Created")
    print("")
    print("Project :", project_name)
    print("Output  : data.json")
    print("")


if __name__ == "__main__":
    main()

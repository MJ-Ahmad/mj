import os

# Define the full project structure as a dictionary
structure = {
    "BitulQuran": {
        "src": {
            "frontend": {
                "public": {},
                "components": {
                    "StudentCard.js": "",
                    "GroupTable.js": "",
                    "ProgressBar.js": ""
                },
                "pages": {
                    "HomePage.html": "",
                    "StudentDashboard.html": "",
                    "UstadDashboard.html": "",
                    "PrincipalDashboard.html": ""
                },
                "hifz_tracker": {
                    "tracker.html": "",
                    "challenges.html": "",
                    "count_since_start.html": "",
                    "count_since_complete.html": "",
                    "countdown_target.html": ""
                },
                "ai_memorize": {
                    "ai_helper.js": "",
                    "speech_to_text.js": ""
                },
                "index.html": ""
            },
            "backend": {
                "BitulQuranApi": {
                    "Controllers": {
                        "StudentsController.cs": "",
                        "GroupsController.cs": "",
                        "AttendanceController.cs": "",
                        "ProgressController.cs": ""
                    },
                    "Models": {
                        "Student.cs": "",
                        "Group.cs": "",
                        "Attendance.cs": "",
                        "Progress.cs": ""
                    },
                    "Data": {
                        "ApplicationDbContext.cs": "",
                        "SeedData.cs": ""
                    },
                    "Services": {
                        "StudentService.cs": "",
                        "AttendanceService.cs": "",
                        "ProgressService.cs": ""
                    },
                    "wwwroot": {
                        "students_group.json": "",
                        "departments": {},
                        "audit_logs": {}
                    },
                    "Program.cs": "",
                    "Startup.cs": "",
                    "appsettings.json": ""
                },
                "publish": {
                    "dashboards": {
                        "principal_dashboard.html": "",
                        "ustad_dashboard.html": "",
                        "student_dashboard.html": ""
                    },
                    "data": {
                        "students_group.json": "",
                        "groups": {
                            "group_A.json": "",
                            "group_B.json": "",
                            "group_C.json": ""
                        },
                        "departments": {
                            "khatmi.json": "",
                            "hifz.json": "",
                            "nazara.json": "",
                            "nurani.json": ""
                        },
                        "teachers.json": "",
                        "timeline.json": ""
                    },
                    "audit_logs": {
                        "attendance.json": "",
                        "progress.json": "",
                        "rewards.json": ""
                    }
                }
            },
            "docs": {
                "institutional_record.md": "",
                "governance.md": "",
                "onboarding_guide.md": ""
            },
            "scripts": {
                "run_local.sh": "",
                "deploy_render.sh": "",
                "deploy_railway.sh": ""
            }
        }
    }
}

def create_structure(base_path, tree):
    for name, content in tree.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(base_path, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    root = os.getcwd()  # current working directory
    create_structure(root, structure)
    print("✅ BitulQuran project structure created successfully!")

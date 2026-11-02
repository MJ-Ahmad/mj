# MJ Shell Framework

Version: 1.0

Author: MJ Ahmad

---

# Purpose

MJ Shell Framework is a modular, audit-friendly, long-term maintainable shell environment built for:

- Personal development
- System administration
- Automation
- Backup management
- Audit management
- Documentation
- Project stewardship
- BitulQuran ecosystem
- Future growth and extensibility

The primary goal is to prevent shell configuration chaos by organizing everything into clearly defined modules.

---

# Core Principle

Never place custom logic directly inside:

```bash
~/.bashrc
```

Instead:

```text
~/.bash/
```

contains all shell logic.

---

# Architecture

```text
~/.bashrc
    ↓
bootstrap.sh
    ↓
Module Directories
    ↓
Functions
    ↓
Logs
    ↓
Backups
```

---

# Framework Layout

```text
~

├── .bashrc
│
├── .bash/
│   ├── bootstrap.sh
│   ├── version
│   ├── README.md
│   │
│   ├── 01-env
│   ├── 02-aliases
│   ├── 03-core
│   ├── 04-functions
│   ├── 05-git
│   ├── ...
│   └── 99-local
│
├── logs/
│
├── backups/
│
└── docs/
```

---

# Design Rules

## Rule 001

Keep .bashrc small.

A large .bashrc becomes difficult to maintain.

---

## Rule 002

All logic belongs inside modules.

Bad:

```bash
# ~/.bashrc

backup_readme() {
    ...
}
```

Good:

```text
~/.bash/06-backup/readme.sh
```

---

## Rule 003

Every module has a dedicated responsibility.

Example:

```text
05-git
```

Contains:

- Git aliases
- Git functions
- Git automation

Only.

---

## Rule 004

Naming should be predictable.

Good:

```bash
mj_backup_readme
mj_git_sync
mj_project_open
```

Avoid:

```bash
backup1
syncNow
myTool
```

---

## Rule 005

Private functions start with underscore.

Example:

```bash
_mj_log
_mj_validate_path
_mj_lock
```

These functions are internal.

---

# Module Categories

## Environment

```text
01-env
```

Contains:

- PATH
- Locale
- Dotnet
- Java
- Node
- Python

---

## Aliases

```text
02-aliases
```

Contains aliases only.

---

## Core

```text
03-core
```

Contains shared utilities.

Examples:

```bash
_mj_log
_mj_error
_mj_lock
```

---

## Backup

```text
06-backup
```

Contains:

- README backups
- Project backups
- Archive backups

---

## Audit

```text
07-audit
```

Contains:

- Audit recording
- Audit reports
- Registry functions

---

## Projects

```text
08-projects
```

Contains project-specific functions.

---

# Bootstrap Process

When a shell starts:

1. ~/.bashrc loads

2. bootstrap.sh executes

3. Modules load in order

Example:

```text
01-env
02-aliases
03-core
...
99-local
```

4. Functions become available

5. Shell becomes operational

---

# Creating New Aliases

Example:

Create file:

```text
~/.bash/02-aliases/networking.sh
```

Add:

```bash
alias myip='curl ifconfig.me'
```

Apply:

```bash
source ~/.bashrc
```

Done.

---

# Creating New Functions

Example:

Create:

```text
~/.bash/06-backup/readme.sh
```

Add:

```bash
mj_backup_readme() {
    ...
}
```

Apply:

```bash
source ~/.bashrc
```

Done.

---

# Creating New Modules

Example:

```text
21-kubernetes
```

After creating a completely new module family:

Update:

```bash
bootstrap.sh
```

Only once.

---

# Logging System

Location:

```text
~/logs/
```

Files:

```text
bash_audit.log
backup.log
security.log
git.log
errors.log
```

Purpose:

### bash_audit.log

Framework activities.

### backup.log

Backup activities.

### security.log

Security events.

### git.log

Git operations.

### errors.log

Failures and exceptions.

---

# Backup System

Location:

```text
~/backups/
```

Structure:

```text
backups/

├── bash/
├── configs/
├── projects/
└── archives/
```

---

# Documentation System

Location:

```text
~/docs/
```

Files:

```text
architecture.md
standards.md
aliases.md
functions.md
changelog.md
```

Purpose:

### architecture.md

System design.

### standards.md

Naming rules.

### aliases.md

Alias registry.

### functions.md

Function registry.

### changelog.md

History of modifications.

---

# Framework Maintenance

Reload shell:

```bash
source ~/.bashrc
```

or

```bash
reload
```

---

# Validation Checklist

Before adding anything:

- Correct module?
- Correct filename?
- Correct naming?
- Documented?
- Logged if necessary?

If all answers are YES:

Proceed.

---

# Stewardship Philosophy

This framework is designed for:

- Clarity over complexity
- Structure over chaos
- Documentation over memory
- Reproducibility over improvisation
- Stewardship over ownership

The framework should remain understandable even years after its original creation.

---

# Future Roadmap

Potential areas:

- Git automation
- Backup automation
- Markdown utilities
- Documentation tools
- Audit reporting
- BitulQuran management
- ML.NET integration
- AI-assisted workflows

---

# Emergency Recovery

If shell behavior becomes abnormal:

Check:

```bash
~/.bashrc
```

Then:

```bash
~/.bash/bootstrap.sh
```

Then:

```bash
~/logs/errors.log
```

Finally:

```bash
source ~/.bashrc
```

---

# End


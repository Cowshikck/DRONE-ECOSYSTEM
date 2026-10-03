Contributing to Drone Ecosystem

Thank you for contributing to the Drone Ecosystem project.

This document defines the basic development rules that all contributors should follow.

---

1. Before You Start

Before implementing a feature:

1. Read "README.md"
2. Read "ARCHITECTURE.md"
3. Understand the module you are modifying
4. Check existing issues/tasks
5. Discuss major architectural changes with the team

Do not introduce major architectural changes without discussion.

---

2. Development Philosophy

The project follows these principles:

- Keep modules independent
- Keep business logic out of controllers
- Avoid unnecessary complexity
- Prefer reusable components
- Write maintainable code
- Document important architectural decisions
- Keep security in mind
- Test important functionality

---

3. Module Boundaries

Each module should have a clearly defined responsibility.

For example:

Authentication
Users
Drones
Flight Sessions
Plugins
Reports
Payments
Organizations

A module should not directly access another module's internal implementation.

Prefer communication through:

Public Services
Interfaces
Events
DTOs
Shared Contracts

---

4. Creating a New Module

Before creating a new module, determine:

- What problem does it solve?
- What data does it own?
- Which modules does it depend on?
- Which modules depend on it?
- What API does it expose?
- Does it really need to be a separate module?

Document significant architectural decisions in "ARCHITECTURE.md".

---

5. Plugin Development

Plugins should remain isolated from the core system wherever possible.

A plugin should clearly define:

Plugin Name
Version
Purpose
Inputs
Outputs
Dependencies
Permissions
Configuration

Example:

Thermal Inspection Plugin

Input:
Thermal images

Processing:
Thermal analysis

Output:
Anomaly results
Inspection data
Report

---

6. Branching

Use descriptive branch names.

Examples:

feature/user-authentication
feature/drone-registration
feature/thermal-plugin
fix/login-validation
fix/session-upload
refactor/plugin-interface
docs/update-architecture

Avoid vague names such as:

test
new
stuff
changes
final
final2

---

7. Commits

Write clear commit messages.

Recommended format:

type: description

Examples:

feat: add drone registration
fix: validate flight session input
refactor: isolate plugin interface
docs: update architecture documentation
test: add drone service tests
chore: update dependencies

Keep commits focused.

Avoid combining unrelated changes into one commit.

---

8. Pull Requests

Pull requests should contain:

- What changed
- Why it changed
- How it was implemented
- Testing performed
- Any known limitations

Example:

## Summary

Added drone registration API.

## Changes

- Added drone module
- Added drone database model
- Added registration endpoint
- Added validation

## Testing

- Unit tests
- API tests

## Known Issues

None

---

9. Code Review

Reviewers should check:

- Correctness
- Security
- Maintainability
- Module boundaries
- Error handling
- Testing
- Performance where relevant

Do not approve code simply because it works.

---

10. Environment Variables

Never commit:

.env
API keys
Passwords
Tokens
Private credentials
Production secrets

Add new variables to:

.env.example

without exposing their real values.

---

11. Database Changes

Database schema changes must be handled through the project's migration system.

Do not manually modify production databases.

Every schema change should be:

- Version controlled
- Reproducible
- Tested

---

12. Tests

New functionality should include appropriate tests.

At minimum, test:

- Normal behavior
- Invalid input
- Authentication/authorization where applicable
- Important edge cases
- Failure scenarios

---

13. Documentation

Update documentation when a change affects:

- Architecture
- Public APIs
- Environment variables
- Plugin interfaces
- Deployment
- Security
- Developer setup

---

14. Security Issues

Do not publicly disclose security vulnerabilities through GitHub issues.

Follow the process described in:

SECURITY.md

---

15. Keep the MVP Simple

Do not add infrastructure simply because it may be useful in the future.

Examples:

Do not add microservices just because the system may scale.
Do not add Kubernetes before it is needed.
Do not add complex event infrastructure without a requirement.
Do not build plugin marketplace infrastructure before plugin execution works.

Build the simplest system that satisfies the current requirement while keeping module boundaries clean.

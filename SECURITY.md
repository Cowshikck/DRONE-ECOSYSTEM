Security Policy

Supported Versions

Security fixes will initially be provided for the actively developed version of the project.

Version| Supported
Development| ✅
Older versions| ❌

---

Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

Security issues should be reported privately to the project maintainers.

Report

Include as much of the following information as possible:

- Description of the vulnerability
- Affected component/module
- Steps to reproduce
- Potential impact
- Proof of concept, if available
- Suggested mitigation, if known

---

Sensitive Information

Never include the following in issues, pull requests, or public discussions:

API keys
Passwords
Access tokens
Database credentials
Private keys
User personal information
Production configuration
Drone credentials
Cloud credentials

If sensitive information is accidentally committed:

1. Do not simply delete the file in a later commit.
2. Immediately notify the maintainers.
3. Revoke/rotate the exposed credential.
4. Remove the secret from repository history if required.

---

Security Principles

The project should follow:

- Least-privilege access
- Secure authentication
- Proper authorization
- Input validation
- Secure file uploads
- Secure API design
- Protection of sensitive data
- Dependency updates
- Audit logging for important actions

---

Drone Data

Drone-related data may include sensitive operational information.

Examples:

Flight locations
Images
Videos
Thermal imagery
Telemetry
Inspection reports
Customer information

Access to such data must be controlled according to the user's permissions and organization access.

---

Plugin Security

Plugins must not automatically receive unrestricted access to:

- User data
- Drone data
- Files
- Database resources
- External services

Plugin permissions should be explicitly defined.

---

Dependency Security

Dependencies should be regularly reviewed for known vulnerabilities.

Do not introduce dependencies without evaluating:

- Maintenance status
- License
- Security history
- Package reputation
- Required permissions
- Dependency size

---

Responsible Disclosure

Security researchers are encouraged to report vulnerabilities privately so that maintainers have an opportunity to investigate and address the issue before public disclosure.

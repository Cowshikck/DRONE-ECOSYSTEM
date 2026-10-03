# Drone Ecosystem Platform — Architecture

**Project:** Drone Ecosystem  
**Architecture:** Managed Modular Monolith + Monorepo  
**Document:** Technical Architecture & Development Rules  
**Status:** Phase 1 Architecture Baseline  
**Version:** 1.0

---

# 1. Purpose

This document defines the technical architecture of the Drone Ecosystem Platform.

It establishes:

- Product architecture principles
- Repository boundaries
- Backend module boundaries
- Data ownership
- User and role architecture
- Drone identity architecture
- Pilot assignment architecture
- Flight and telemetry architecture
- Maintenance and technician workflows
- Marketplace and booking architecture
- Trust and verified-work architecture
- Security and authorization
- Audit requirements
- File and storage architecture
- Offline synchronization
- Event communication
- API rules
- Scalability strategy
- Phase 1 boundaries

All developers working on the platform should follow this document.

Architectural changes that significantly alter these rules should be recorded under:

```text
09_DOCUMENTATION/decisions/
```

using Architecture Decision Records where appropriate.

---

# 2. Product Vision

The Drone Ecosystem Platform is a professional network, asset-management and work-management platform for the drone ecosystem.

The core concept is:

> Every drone should develop a reliable digital identity and long-term digital history.

The platform connects:

- Drone Owners
- Drone Pilots
- Technicians
- Consumers / Customers
- Organizations / Companies
- Administrators
- Drones
- Flight activity
- Maintenance activity
- Service work
- Bookings
- Communications
- Documents
- Data sources

The drone acts as a central digital asset connecting many of these relationships.

---

# 3. Phase 1 Product Model

Phase 1 primarily supports four user roles:

```text
                     DRONE ECOSYSTEM
                           |
        ---------------------------------------------
        |                |              |           |
   TECHNICIAN          OWNER          PILOT      CONSUMER
        |                |              |           |
     Profile          Drones          Profile     Services
     Portfolio        Ownership       Portfolio   Requests
     Trust Score      Pilot Access    Flights     Bookings
     Tickets          Maintenance     Hours       Providers
     Work History     History         DGCA Log
```

These are not four independent applications.

They are different views over the same connected platform.

A single user account may eventually hold multiple roles simultaneously.

Example:

```text
User A
 |
 +-- Drone Owner
 |
 +-- Pilot
 |
 +-- Technician
```

A user must not require separate accounts for separate roles.

---

# 4. Core Domain Relationship

The primary Phase 1 relationship is:

```text
USER
 |
 +---- PROFILE / ROLES
 |
 +---- OWNERSHIP
          |
          v
        DRONE
          |
          +---- PILOT ASSIGNMENTS
          |
          +---- FLIGHTS
          |
          +---- MAINTENANCE
          |
          +---- SERVICE HISTORY
          |
          +---- DOCUMENTS
```

Another important relationship is:

```text
CONSUMER
   |
   v
SERVICE REQUEST
   |
   v
PROVIDER / PILOT / OWNER
   |
   v
BOOKING / WORK
   |
   v
COMPLETED WORK
   |
   v
VERIFIED WORK HISTORY
```

The long-term product objective is:

```text
Identity
   +
Drone Identity
   +
Relationships
   +
Work
   +
History
   =
Drone Ecosystem Digital Record
```

---

# 5. Architecture Style

The backend uses a:

> Managed Modular Monolith

The platform initially runs as one backend application while maintaining strong internal domain boundaries.

We intentionally do not begin with microservices.

The modular monolith provides:

- Faster development
- Easier debugging
- Simpler deployment
- Easier local development
- Simpler transactions
- Lower infrastructure overhead
- Clear domain boundaries
- Easier testing
- A future path toward service extraction

Modules must behave like independent systems even though they currently run in the same process.

The architecture should make future extraction possible without redesigning the business domain.

---

# 6. Repository Strategy

The project uses a monorepo.

```text
DRONE-ECOSYSTEM/
│
├── 01_CLIENT/
│   ├── web/
│   ├── mobile/
│   └── ground-agent/
│
├── 02_BACKEND/
│   ├── api/
│   ├── modules/
│   └── shared/
│
├── 03_DATABASE/
│
├── 04_STORAGE/
│
├── 05_EVENTS/
│
├── 06_SECURITY/
│
├── 07_ADMIN/
│
├── 08_INFRASTRUCTURE/
│
├── 09_DOCUMENTATION/
│
├── 10_EXTENSIONS/
│
├── packages/
│
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── README.md
├── package.json
├── pnpm-workspace.yaml
├── .env.example
└── .gitignore
```

The repository is managed using:

```text
Node.js >= 24
pnpm
TypeScript
```

The root workspace coordinates the applications and shared packages.

---

# 7. Repository Boundary Rules

The numbered top-level directories represent architectural concerns.

They must not become duplicate locations for business logic.

For example:

```text
02_BACKEND/modules/fleet/
```

owns Fleet business behavior.

Do not duplicate Fleet business rules inside:

```text
06_SECURITY/
07_ADMIN/
03_DATABASE/
05_EVENTS/
```

Those directories provide supporting infrastructure, policies, contracts, tooling or operational concerns.

---

# 8. Client Architecture

## 8.1 Web Application

Location:

```text
01_CLIENT/web/
```

The web application is the primary browser-based platform.

Planned architecture:

```text
web/
├── public/
├── src/
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── layouts/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── stores/
│   ├── types/
│   └── utils/
└── tests/
```

The intended stack is:

```text
Next.js
React
TypeScript
Tailwind CSS
```

The application should support role-aware dashboards.

Examples:

```text
/dashboard/owner
/dashboard/pilot
/dashboard/technician
/dashboard/consumer
```

A user with multiple roles may switch context without switching accounts.

UI components must not contain core business rules.

Business actions should flow through services/API clients.

---

# 9. Mobile Architecture

Location:

```text
01_CLIENT/mobile/
```

The mobile application provides general platform functionality.

Potential functionality includes:

- Authentication
- Profile management
- Drone dashboard
- Pilot functionality
- Technician workflow
- Notifications
- Messaging
- Bookings
- Flight-history viewing
- Drone information
- Service management

The mobile application must remain logically separate from the specialized Ground Agent.

---

# 10. Ground Agent Architecture

Location:

```text
01_CLIENT/ground-agent/
```

The Ground Agent is responsible for flight-data acquisition and synchronization.

It may eventually run on:

```text
Android
Windows
Other supported platforms
```

Responsibilities include:

- Connecting to drone data sources
- Connecting to ground stations
- Receiving telemetry
- Flight detection
- Drone selection
- Local persistence
- Offline buffering
- Data normalization
- Authentication
- Secure synchronization
- Device identification
- Retry management

The Ground Agent must not become a second backend.

It must not own:

- User administration
- Marketplace logic
- Payment processing
- Maintenance workflows
- Legal drone ownership
- Organization management

---

# 11. Ground Agent Adapter Architecture

The system must not depend on a single manufacturer or protocol.

Use adapters.

```text
Drone
  |
  v
Flight Controller / Ground Station
  |
  v
Protocol Adapter
  |
  v
Normalized Telemetry
  |
  v
Local Storage
  |
  v
Sync Engine
  |
  v
Backend
  |
  v
Drone Digital History
```

Structure:

```text
ground-agent/
└── src/
    ├── adapters/
    │   ├── protocols/
    │   └── ground-stations/
    ├── telemetry/
    ├── flight-detection/
    ├── local-storage/
    ├── sync/
    ├── network/
    ├── device/
    ├── authentication/
    ├── drone-selection/
    └── security/
```

Supporting a new drone protocol should require implementing an adapter rather than rewriting the flight system.

---

# 12. Backend Architecture

Location:

```text
02_BACKEND/
```

The backend follows layered modular architecture.

```text
API
 |
 v
Application
 |
 v
Domain
 |
 v
Infrastructure
```

Every major business module follows:

```text
module/
├── domain/
├── application/
├── infrastructure/
└── api/
```

---

# 13. Layer Responsibilities

## Domain

Contains business concepts and invariants.

Examples:

- Entities
- Value objects
- Domain rules
- Domain events
- Repository interfaces

Domain code should avoid dependencies on frameworks where practical.

---

## Application

Coordinates business use cases.

Examples:

```text
RegisterDrone
AssignPilot
RemovePilot
CreateRepairTicket
CompleteRepair
CreateBooking
ImportFlightLog
GenerateDGCAFlightLog
```

Application services orchestrate domain objects and repositories.

---

## Infrastructure

Contains technical implementations.

Examples:

- PostgreSQL repositories
- Object storage adapters
- Email integrations
- Push-notification integrations
- External APIs
- Queue integrations

---

## API

Exposes functionality externally.

Examples:

- REST controllers
- Request validation
- Response mapping
- Authentication hooks
- API-specific authorization checks

---

# 14. Backend Modules

The initial backend modules are:

```text
identity
organizations
profiles
fleet
flights
maintenance
marketplace
bookings
payments
communications
notifications
media
reports
```

Each module owns a clear business capability.

---

# 15. Identity Module

Location:

```text
02_BACKEND/modules/identity/
```

Identity owns:

- User accounts
- Authentication identity
- Account lifecycle
- Credentials
- Identity verification status
- User platform identity
- Role association
- Public identity references where applicable

Identity does not own:

- Drone ownership
- Pilot assignments
- Repair tickets
- Flight records
- Bookings

---

# 16. Multi-Role User Model

A user is one identity.

Roles describe capabilities or professional contexts.

Example:

```text
USER
 |
 +-- OWNER
 |
 +-- PILOT
 |
 +-- TECHNICIAN
 |
 +-- CONSUMER
```

Roles must never require duplicate accounts.

Phase 1 may initially ask a user to choose a primary role during onboarding, but the data model must support multiple roles.

---

# 17. UID Architecture

Database primary keys and public platform UIDs are separate concepts.

Internal database references should use globally unique identifiers.

Example:

```text
UUID / UUIDv7
```

Public identifiers are human-readable platform identifiers.

Examples:

```text
Drone:
DRN-TN-00001234

Pilot:
PLT-IN-0000456
```

Future identifiers may include:

```text
Technician:
TEC-IN-0000123

User:
USR-IN-0000123
```

Exact public UID formatting may evolve.

Public UIDs must:

- Be unique
- Never be reused
- Remain stable
- Not expose database sequence assumptions where security is affected
- Be generated centrally
- Be searchable

Public UID must not be used as the sole database primary key.

---

# 18. Profiles Module

Location:

```text
02_BACKEND/modules/profiles/
```

Profiles owns professional and role-specific profile data.

Examples:

## Pilot profile

- Experience
- Drone models flown
- Skills
- Certifications
- Work types
- Portfolio
- Previous work
- Service area

## Technician profile

- Skills
- Drone models serviced
- Repair capabilities
- Experience
- Certifications
- Portfolio
- Previous work
- Location
- Service area

## Consumer profile

- General account/profile information
- Preferences where required

The Profiles module owns the professional profile.

The Maintenance module does **not** own the technician's basic professional profile.

Maintenance owns technician work performed through maintenance workflows.

---

# 19. Organizations Module

Location:

```text
02_BACKEND/modules/organizations/
```

Organizations owns:

- Companies
- Organization profiles
- Memberships
- Organization roles
- Organization ownership
- Member invitations
- Organization permissions

A user may belong to multiple organizations.

```text
User
 |
 v
Membership
 |
 v
Organization
```

Organization roles may include:

```text
Company Owner
Company Admin
Company Member
```

Organization ownership is separate from individual user identity.

---

# 20. Fleet Module

Location:

```text
02_BACKEND/modules/fleet/
```

Fleet owns:

- Drone registration
- Drone identity
- Manufacturer
- Model
- Serial number
- Platform Drone UID
- Current ownership
- Ownership history
- Pilot assignments
- Pilot assignment history
- Drone permissions
- Operational access

A user can own many drones.

Never assume:

```text
1 User = 1 Drone
```

The correct model is:

```text
Owner
 |
 +-- Drone 001
 +-- Drone 002
 +-- Drone 003
 +-- ...
 +-- Drone N
```

---

# 21. Drone Ownership

Every drone has one current platform-recognized owner.

The owner may be:

- Individual
- Organization

Ownership history must be preserved.

Changing ownership must create history rather than overwriting historical ownership.

Example:

```text
Drone
 |
 +-- Current Owner
 |
 +-- Ownership History
```

Temporary access never changes ownership.

---

# 22. Pilot Assignment

Pilot assignment is a historical relationship.

Example:

```text
Drone 001
 |
 +-- Pilot A
 +-- Pilot B
```

Assignment data should include:

```text
drone_id
pilot_id
assigned_by
assigned_at
accepted_at
removed_at
status
```

Possible states:

```text
PENDING
ACTIVE
REJECTED
REMOVED
EXPIRED
```

An assignment should not be physically deleted merely because the pilot was removed.

History must remain available.

Example:

```text
Pilot A assigned to DRN001
2026-10-01

Pilot A removed from DRN001
2026-11-20
```

---

# 23. Pilot Access Invariant

Assignment and legal ownership are different.

A pilot assigned to a drone may receive operational access.

The pilot does not become the owner.

Removing a pilot must revoke permissions derived from that assignment.

Historical flight attribution must remain intact after removal.

---

# 24. Flights Module

Location:

```text
02_BACKEND/modules/flights/
```

Flights owns:

- Flight records
- Flight segments
- Pilot attribution
- Flight duration
- Pilot flight hours
- Telemetry
- Imported logs
- Flight summaries
- Flight-history records

---

# 25. Flight Record Model

A flight belongs to a drone.

```text
Drone
 |
 +-- Flight
       |
       +-- Pilot Segment
       +-- Pilot Segment
       +-- Telemetry
       +-- Source Data
```

A single flight may involve multiple pilots.

Example:

```text
Flight
09:00 ---------------- 11:00

Pilot A
09:00 -------- 10:00

Pilot B
10:00 -------- 11:00
```

Drone flight duration:

```text
2 hours
```

Pilot A flight time:

```text
1 hour
```

Pilot B flight time:

```text
1 hour
```

---

# 26. Unassigned Flights

A flight must still be stored if the pilot cannot be identified.

Example:

```text
pilot_id = NULL
```

An unidentified pilot must not cause flight data to be discarded.

Ordinary users must not be allowed to arbitrarily claim historical unassigned flights.

Any later assignment must use an authorized and auditable workflow.

---

# 27. Pilot Flight Hours

Pilot flight hours should be derived from verified flight records rather than maintained as an independent manual number.

Example:

```text
Pilot A

DRN001     32 h
DRN002     17 h
DRN005     41 h
----------------
Total      90 h
```

The canonical data is:

```text
Flight
+
Pilot Segments
```

Total flight hours are derived data.

Where performance requires caching totals, the source flight records remain authoritative.

---

# 28. DGCA Flight Log Assistance

The pilot dashboard should expose a:

```text
DGCA Flight Log
```

feature.

Phase 1 treats this as:

> Export / input assistance

rather than assuming direct regulatory integration.

The system may use stored:

- Pilot information
- Drone information
- Flight date
- Flight duration
- Flight records
- Flight locations
- Relevant regulatory identifiers

to populate an export.

The exact DGCA format must be confirmed before implementing production regulatory submission.

The platform must not claim regulatory submission capability unless an approved integration exists.

---

# 29. Telemetry Architecture

Telemetry must use a platform-independent normalized format.

Possible telemetry categories include:

## Flight

- Flight start
- Flight end
- Flight status
- Flight mode
- Duration

## Location

- Latitude
- Longitude
- Altitude
- Home position
- Distance
- Heading

## Movement

- Speed
- Direction
- Vertical speed
- Acceleration where available

## Battery

- Percentage
- Voltage
- Current
- Temperature
- Status
- Cycle data where available

## GPS

- Satellite count
- GPS state
- Accuracy where available

## System

- Connection status
- Controller state
- Motor/ESC data
- Warning states
- System status

## Environment

- Temperature
- Pressure
- Additional sensors

## Payload

- Camera state
- Media references
- Payload information
- Thermal data
- Sensor data

Not every drone provides every field.

The telemetry model must support optional capabilities.

---

# 30. Automatic Flight Detection

Where integrations support it, flights should be generated automatically.

```text
Ground Agent
    |
    v
Detect Flight Start
    |
    v
Create Flight
    |
    v
Collect Telemetry
    |
    v
Detect Flight End
    |
    v
Finalize Flight
```

Normal operations should not require a pilot to manually enter:

```text
start_time
end_time
duration
```

Duration should be derived from recorded flight activity.

---

# 31. Flight Log Import

The system may support imported logs.

```text
Original File
    |
    v
Identify Format
    |
    v
Parse
    |
    v
Validate
    |
    v
Normalize
    |
    v
Flight Record
    |
    v
Drone Digital History
```

The original file must be preserved.

Parsed and normalized records must never silently replace the original source.

---

# 32. Original Data Preservation

Source drone data must be immutable.

Data processing layers:

```text
1. Original Source
        |
        v
2. Parsed Data
        |
        v
3. Normalized Data
        |
        v
4. Derived / Analytical Data
```

AI or analytical processing creates new derived data.

It must not mutate the original source.

---

# 33. Offline-First Ground Data

Flight-data collection must not depend entirely on internet availability.

Connected:

```text
Drone
  |
Ground Agent
  |
Local Storage
  |
Backend
```

Disconnected:

```text
Drone
  |
Ground Agent
  |
Local Storage
  |
Buffered Upload Queue
```

After connectivity returns:

```text
Buffered Queue
   |
   v
Sync Engine
   |
   v
Backend
```

---

# 34. Synchronization Requirements

The synchronization system must support:

- Offline buffering
- Retry
- Idempotency
- Duplicate prevention
- Upload queues
- Failed-upload recovery
- Event ordering where required
- Connection-aware synchronization
- Priority synchronization
- Partial failure handling

Every synchronized item should have enough identity information to prevent duplicate creation.

---

# 35. Maintenance Module

Location:

```text
02_BACKEND/modules/maintenance/
```

Maintenance owns:

- Repair requests
- Repair tickets
- Technician assignment
- Diagnosis
- Repair workflow
- Maintenance workflow
- Work performed
- Parts replacement
- Repair evidence
- Repair completion
- Maintenance history
- Repair certificates
- Technician work records

The technician's personal professional profile remains owned by Profiles.

---

# 36. Repair Ticket Lifecycle

Phase 1 ticket states should support a simple workflow.

```text
CREATED
   |
ACCEPTED
   |
DIAGNOSIS
   |
REPAIR
   |
TESTING
   |
COMPLETED
```

Later expansion may introduce:

```text
QUOTATION
OWNER_APPROVAL
DRONE_RECEIVED
WAITING_FOR_PARTS
RETURN_READY
RETURNED
CANCELLED
CLOSED
```

Ticket state transitions must be recorded historically.

Do not simply overwrite the ticket state without maintaining transition history.

---

# 37. Repair Ticket History

Example:

```text
Repair Ticket
 |
 +-- Created
 |     2026-10-03 10:21
 |
 +-- Accepted
 |     Technician X
 |
 +-- Diagnosis
 |     Motor failure detected
 |
 +-- Repair
 |     Motor replaced
 |
 +-- Testing
 |     Flight/bench test passed
 |
 +-- Completed
```

Each transition should record:

```text
actor
timestamp
previous_state
new_state
notes
```

where applicable.

---

# 38. Technician Access

A technician does not receive unrestricted owner access.

Access should be:

```text
Technician
    |
Accepted Ticket
    |
Relevant Drone
    |
Required Permissions
```

Technician access must be:

- Ticket scoped
- Permission scoped
- Auditable
- Revocable

Completing or cancelling the ticket should remove permissions that exist solely because of that ticket.

---

# 39. Technician Trust Score

The platform may expose a Technician Trust Score.

Phase 1 architecture should support the score without prematurely locking the platform into a permanent algorithm.

Potential inputs include:

- Completed jobs
- Verified jobs
- Customer ratings
- Successful work
- Reviews
- Work history
- Cancellation/dispute outcomes where appropriate

The score is **derived data**.

The source records remain authoritative.

Conceptually:

```text
Verified Work
      +
Ratings
      +
Reviews
      +
Completion History
      |
      v
Trust Score Engine
      |
      v
Technician Trust Score
```

The scoring algorithm should be versioned.

Example:

```text
score
score_version
calculated_at
```

This makes future algorithm changes auditable.

---

# 40. Verified Work History

Verified professional history should come from real platform activity whenever possible.

Examples:

```text
Repair completed
Booking completed
Flight recorded
Service completed
```

A professional may still describe external experience in a portfolio.

However:

```text
Self-Declared Experience
```

and:

```text
Platform-Verified Work
```

must remain distinguishable.

---

# 41. Marketplace Module

Location:

```text
02_BACKEND/modules/marketplace/
```

Marketplace owns:

- Service listings
- Provider discovery
- Service categories
- Service areas
- Provider availability metadata
- Pricing presentation
- Marketplace search metadata

Potential service types include:

```text
Drone + Pilot
Pilot Only
Complete Drone Service
```

Examples include:

- Land survey
- Aerial photography
- Inspection
- Mapping
- Agriculture
- Solar inspection

---

# 42. Consumer Architecture

Consumers do not need to own drones.

A consumer may:

- Search professionals
- Search pilots
- Find drone/service providers
- View service listings
- Create service requests
- Request bookings
- Communicate with providers
- Complete service workflows

Basic relationship:

```text
Consumer
   |
Service Requirement
   |
Provider Discovery
   |
Booking
   |
Service
   |
Completion
   |
Verified Work History
```

---

# 43. Bookings Module

Location:

```text
02_BACKEND/modules/bookings/
```

Bookings owns:

- Booking creation
- Service request lifecycle
- Scheduling
- Provider acceptance
- Provider rejection
- Booking status
- Service start
- Service completion
- Customer confirmation

Possible lifecycle:

```text
REQUESTED
    |
ACCEPTED
    |
SCHEDULED
    |
IN_PROGRESS
    |
COMPLETED
    |
CONFIRMED
    |
CLOSED
```

Other states may include:

```text
REJECTED
CANCELLED
DISPUTED
```

Booking and payment remain separate concerns.

---

# 44. Payments Module

Location:

```text
02_BACKEND/modules/payments/
```

Payment functionality may be limited or deferred during early Phase 1 development.

Its boundary is nevertheless defined now.

Payments owns:

- Payment intent
- Payment provider integration
- Payment state
- Refunds
- Transactions
- Settlements
- Provider payouts

Other business modules must not implement payment-provider APIs directly.

They call the Payments module.

---

# 45. Communications Module

Location:

```text
02_BACKEND/modules/communications/
```

Communications owns:

- Conversations
- Messages
- Attachments
- Context references
- Future calling/messaging capabilities

Communication must be context-aware.

Examples:

```text
Repair Ticket
    |
Owner <-> Technician
```

```text
Booking
    |
Consumer <-> Provider
```

```text
Organization
    |
Members
```

---

# 46. Notifications Module

Location:

```text
02_BACKEND/modules/notifications/
```

Notifications owns:

- In-app notifications
- Push notifications
- Notification preferences
- Notification delivery status
- Notification templates

Notifications should normally respond to events rather than business modules manually constructing delivery logic.

Example:

```text
PilotAssigned
    |
Notification Handler
    |
Push / In-App Notification
```

---

# 47. Media Module

Location:

```text
02_BACKEND/modules/media/
```

Media owns:

- Upload metadata
- Image references
- Video references
- File access
- Storage references
- Access policy integration

Large binaries should not be stored directly inside ordinary relational database rows.

---

# 48. Reports Module

Location:

```text
02_BACKEND/modules/reports/
```

Reports owns generated output such as:

- DGCA flight-log exports
- Repair certificates
- Inspection reports
- Future analytical reports
- Future AI-generated reports

Reports should read validated domain information through defined module interfaces rather than directly changing domain data.

---

# 49. Drone Digital History

The drone digital record is a central product capability.

Conceptually:

```text
DRONE
 |
 +-- Identity
 |
 +-- Ownership History
 |
 +-- Pilot Assignment History
 |
 +-- Flight History
 |
 +-- Pilot Segments
 |
 +-- Flight Hours
 |
 +-- Telemetry
 |
 +-- Imported Flight Logs
 |
 +-- Maintenance History
 |
 +-- Repair History
 |
 +-- Parts History
 |
 +-- Certificates
 |
 +-- Documents
 |
 +-- Service History
```

This record grows over the operational lifetime of the drone.

Historical records should generally be appended or superseded rather than destructively overwritten.

---

# 50. Module Boundary Rule

This is a mandatory architecture rule:

> A module must never directly modify another module's internal business data.

Bad:

```text
Maintenance
    |
    v
UPDATE fleet.drones
```

Correct:

```text
Maintenance
    |
    v
Fleet Application Interface
    |
    v
Fleet
```

Or:

```text
Maintenance
    |
    v
Domain/Application Event
    |
    v
Fleet Event Handler
```

Modules communicate through:

- Application services
- Public module interfaces
- Defined contracts
- Events

---

# 51. Database Ownership

Each module owns its business tables.

Conceptual ownership:

```text
IDENTITY
users
user_roles
credentials

ORGANIZATIONS
organizations
memberships
organization_roles

PROFILES
profiles
pilot_profiles
technician_profiles
certifications
portfolio_items

FLEET
drones
ownership_history
pilot_assignments
drone_access

FLIGHTS
flights
flight_segments
telemetry
flight_imports

MAINTENANCE
repair_tickets
repair_ticket_history
repair_parts
repair_evidence
repair_certificates

MARKETPLACE
service_listings
service_categories
provider_service_areas

BOOKINGS
bookings
booking_history

PAYMENTS
payments
transactions

COMMUNICATIONS
conversations
messages

NOTIFICATIONS
notifications
notification_preferences

MEDIA
media_assets

REPORTS
generated_reports
```

Cross-module database writes are prohibited.

Foreign keys may exist where appropriate, but they do not transfer business ownership.

---

# 52. Database Strategy

Primary database:

```text
PostgreSQL
```

Location for database operations:

```text
03_DATABASE/
├── migrations/
├── seeds/
└── postgresql/
```

All production schema changes must be represented through migrations.

Manual production schema modifications are prohibited.

Migration history must remain in source control.

---

# 53. Storage Architecture

Location:

```text
04_STORAGE/
```

Logical storage categories include:

```text
documents/
flight-logs/
    original/
    processed/
repair-evidence/
media/
certificates/
```

These repository directories represent architectural storage categories.

Production binary files must not be committed to Git.

Actual file storage should eventually use an object-storage implementation.

Examples could include S3-compatible storage.

---

# 54. Event Architecture

Location:

```text
05_EVENTS/
```

The event layer contains shared event contracts and event-bus infrastructure.

Possible events include:

```text
UserRegistered
DroneRegistered
DroneOwnershipChanged

PilotAssigned
PilotAccepted
PilotRemoved

FlightStarted
FlightCompleted
FlightImported

RepairTicketCreated
RepairAccepted
RepairCompleted

BookingCreated
BookingAccepted
BookingCompleted

PaymentCompleted
```

Events should describe something that has happened.

Prefer:

```text
PilotAssigned
```

rather than:

```text
AssignPilot
```

Commands request action.

Events record outcomes.

---

# 55. Event Consistency

Because Phase 1 is a modular monolith, many internal events may initially execute in-process.

However, event contracts should be designed so important workflows can later move to:

- Background workers
- Message brokers
- Queues
- Independent services

For operations requiring durable asynchronous processing, the architecture should support an Outbox Pattern in the future.

---

# 56. Authentication

Authentication answers:

> Who is this user?

Authentication belongs primarily to Identity and cross-cutting security infrastructure.

Possible mechanisms may include:

- Email/password
- OAuth
- OTP
- Token/session authentication

Specific implementations may evolve.

---

# 57. Authorization

Authorization answers:

> What is this user allowed to do in this context?

Use:

```text
RBAC
+
Fine-Grained Permissions
+
Resource Context
```

Authorization decisions may depend on:

```text
User
+
Role
+
Ownership
+
Assignment
+
Permission
+
Organization Membership
+
Workflow Context
```

Example:

```text
Can User X view Drone Y?

1. Is X authenticated?
2. Is X the owner?
3. Is X an active assigned pilot?
4. Is X an authorized organization member?
5. Is X a technician with an active repair ticket?
6. Does the relevant permission allow this action?
```

---

# 58. Security Architecture

Location:

```text
06_SECURITY/
```

This directory contains shared security mechanisms such as:

- Authentication infrastructure
- Authorization framework
- Permission definitions
- Audit infrastructure

Domain-specific permission decisions still belong close to the domain that understands the resource.

Security infrastructure must not become a second location for business logic.

---

# 59. Audit Architecture

Important operations must be auditable.

Examples include:

- Drone ownership changes
- Pilot assignment
- Pilot removal
- Organization permission changes
- Technician access
- Repair status changes
- Flight reassignment
- Certificate generation
- Admin actions
- Sensitive data access

An audit record should generally include:

```text
actor_id
action
resource_type
resource_id
timestamp
context
request/reference information
```

Audit records should be append-oriented.

---

# 60. API Architecture

External APIs should be versioned.

Example:

```text
/api/v1/
```

API responsibilities include:

- Authentication
- Input validation
- Authorization entry checks
- Application-service invocation
- Response serialization
- Standardized error responses

Controllers must remain thin.

Controllers must not contain domain logic.

---

# 61. API Contracts

Requests and responses should use explicit schemas.

Location:

```text
02_BACKEND/api/request-schemas/
02_BACKEND/api/response-schemas/
```

Validation rules shared between applications may live under:

```text
packages/validation/
```

API changes that break clients should require versioning or a controlled migration.

---

# 62. Shared Packages

Location:

```text
packages/
```

Initial packages:

```text
packages/
├── config/
├── types/
├── validation/
├── ui/
└── utils/
```

Purpose:

## config

Shared tooling and configuration.

## types

Cross-application public TypeScript types.

Do not place private backend domain entities here.

## validation

Reusable schema validation where safe to share.

## ui

Reusable presentation components.

## utils

Small generic utilities.

Shared packages should remain small.

Do not create a giant `shared` package containing business logic from multiple domains.

---

# 63. Admin Architecture

Location:

```text
07_ADMIN/
```

Administrative functionality may include:

- Verification
- Moderation
- Disputes
- Operations

Admin tooling must use normal domain/application interfaces.

Admin code must not bypass module invariants by directly modifying business tables.

Administrative actions should receive stronger audit coverage.

---

# 64. Infrastructure Architecture

Location:

```text
08_INFRASTRUCTURE/
```

Contains:

```text
ci-cd/
deployment/
    development/
    staging/
    production/
monitoring/
logging/
backups/
```

Environments:

```text
Development
Staging
Production
```

Environment-specific secrets must never be committed to Git.

---

# 65. Configuration

Configuration is environment-driven.

Example:

```text
APP_ENV
APP_PORT
DATABASE_URL
JWT_SECRET
STORAGE_PROVIDER
```

The repository includes:

```text
.env.example
```

Real secrets belong in:

```text
.env
```

or deployment secret management.

Real credentials must never be committed.

---

# 66. Observability

The system should progressively support:

- Structured logs
- Error tracking
- Request correlation IDs
- Metrics
- Health endpoints
- Audit events
- Background-job monitoring
- Sync diagnostics

Important actions should be traceable across module boundaries.

---

# 67. Error Handling

Errors should use predictable categories.

Examples:

```text
VALIDATION_ERROR
AUTHENTICATION_REQUIRED
PERMISSION_DENIED
RESOURCE_NOT_FOUND
CONFLICT
DOMAIN_RULE_VIOLATION
EXTERNAL_SERVICE_FAILURE
INTERNAL_ERROR
```

Internal implementation details must not be leaked to external clients.

---

# 68. Concurrency

Operations affecting ownership, assignments, flight finalization, payment state or ticket transitions may face concurrent updates.

Where required use:

- Database transactions
- Unique constraints
- Optimistic locking
- Idempotency keys
- State-transition validation

Example:

Two requests must not create two simultaneous contradictory ownership records.

---

# 69. Idempotency

Operations likely to be retried should support idempotency.

Important examples:

- Ground Agent uploads
- Flight imports
- Payment callbacks
- Booking operations
- Event consumers
- Notification jobs

Repeated delivery must not unintentionally create duplicate business records.

---

# 70. History Over Deletion

Core operational history should generally not be hard deleted.

Examples:

- Ownership history
- Pilot assignments
- Flight records
- Repair records
- Parts records
- Certificates
- Work history
- Audit events

Where deletion is legally required, the platform should follow a controlled privacy/data-retention process rather than arbitrary application deletion.

---

# 71. Soft Deletion

Entities requiring removal from normal product use may use:

```text
deleted_at
archived_at
status
```

depending on the domain.

Soft deletion must not substitute for proper history.

---

# 72. Work History Architecture

Professional work history can originate from:

```text
Maintenance Job
Booking
Service Completion
Verified Flight Activity
```

A canonical work record may reference:

```text
professional
work_type
source_module
source_record_id
started_at
completed_at
verification_status
```

This allows professional profiles to distinguish verified platform activity from manually entered portfolio items.

---

# 73. Search Architecture

Phase 1 search may initially use PostgreSQL capabilities.

Search targets may include:

- Pilots
- Technicians
- Service providers
- Services
- Locations
- Drone models
- Skills

The application should hide search implementation behind interfaces so a dedicated search engine can be introduced later without changing domain behavior.

---

# 74. Notification Flow

Example:

```text
Fleet
 |
PilotAssigned
 |
Event Bus
 |
Notifications
 |
Push / In-App
```

Another example:

```text
Maintenance
 |
RepairCompleted
 |
 +---- Notifications
 |
 +---- Work History
 |
 +---- Drone History
```

One business event may have multiple independent consumers.

---

# 75. Phase 1 Core Features

Phase 1 includes the foundations for:

## Authentication

- Registration
- Login
- Role selection
- Profile management
- UID generation

## Technician

- Professional profile
- Portfolio
- Drone-model experience
- Trust-score representation
- Repair/maintenance tickets
- Ticket history
- Completed work

## Owner

- Owner profile
- Multiple drone registration
- Drone UID
- Drone dashboard
- Pilot assignment
- Pilot removal
- Assignment history
- Drone information
- Maintenance ticket creation

## Pilot

- Pilot UID
- Professional profile
- Portfolio
- Assigned drones
- Flight history
- Flight hours
- DGCA flight-log assistance

## Consumer

- Consumer account
- Professional/service discovery
- Pilot discovery
- Provider discovery
- Service requests
- Booking workflow

## Backend

- Identity
- Roles
- Profiles
- Fleet
- Flights
- Maintenance
- Marketplace
- Bookings
- Notifications
- Media foundations
- Reports foundations
- Events
- Security
- Audit

---

# 76. Phase 1 Non-Goals

Phase 1 should not attempt to fully implement:

- Complete drone marketplace
- Parts marketplace
- Predictive maintenance
- AI diagnostics
- Plugin marketplace
- Advanced enterprise fleet management
- Automated parts supply chain
- Advanced industrial workflows
- Full manufacturer integration coverage
- Full autonomous regulatory integration
- Large-scale microservices infrastructure

Folders may exist for these future capabilities without implying they are Phase 1 deliverables.

---

# 77. Extensions Architecture

Location:

```text
10_EXTENSIONS/
```

Reserved for future capabilities:

```text
plugins/
ai-analytics/
predictive-maintenance/
enterprise/
integrations/
```

Extensions should depend on stable domain interfaces.

Core domain modules must not depend directly on optional extensions.

Correct direction:

```text
Extension
    |
    v
Core Public Interface
```

Avoid:

```text
Core Domain
    |
    v
Optional Extension
```

---

# 78. Future Microservice Extraction

The modular monolith should allow specific capabilities to become services later.

Possible future candidates include:

- Telemetry ingestion
- Notifications
- Media processing
- Payments
- Search
- Reporting
- AI analytics

Extraction should occur only when operational requirements justify it.

Examples:

- Independent scaling requirement
- Significant workload isolation
- Separate release cadence
- Reliability isolation
- Dedicated infrastructure requirement

Microservices must not be introduced merely for architectural appearance.

---

# 79. Future Event Infrastructure

Phase 1 may use an internal event bus.

Future architecture may evolve toward:

```text
Module
  |
Outbox
  |
Message Broker
  |
Consumers
```

Potential technologies should be selected based on actual scale requirements rather than introduced prematurely.

---

# 80. Testing Strategy

Testing should exist at multiple levels.

```text
Unit Tests
    |
Application Tests
    |
Integration Tests
    |
API Tests
    |
End-to-End Tests
```

High-value domain rules require strong tests.

Examples:

- A removed pilot loses active drone access.
- Removing a pilot does not remove historical flights.
- A technician cannot access unrelated drones.
- An owner can register multiple drones.
- Ownership history cannot silently disappear.
- Duplicate Ground Agent uploads do not duplicate flights.
- Repair states cannot transition arbitrarily.
- Flight hours equal verified attributed segments.

---

# 81. Domain Invariants

The following invariants should be protected by business logic and, where appropriate, database constraints.

1. A user is one identity regardless of role count.

2. An owner may own many drones.

3. A drone has one current platform-recognized owner.

4. Ownership history must be preserved.

5. Pilot assignment must be historical.

6. Removing a pilot does not remove past pilot history.

7. Flight records remain valid even when no pilot can be identified.

8. Pilot flight hours come from verified flight attribution.

9. Original imported flight data must remain recoverable.

10. Maintenance history must be preserved.

11. Module-owned data may only be modified through its owning module.

12. Temporary access never implies legal ownership.

13. Public UIDs are stable identifiers and must never be recycled.

14. Important state transitions must be auditable.

---

# 82. Development Rules

All developers should follow these rules:

```text
1. Keep business logic inside its owning backend module.

2. Keep controllers thin.

3. Do not directly update another module's tables.

4. Prefer explicit application interfaces between modules.

5. Use events for side effects and cross-domain reactions where appropriate.

6. Preserve historical records.

7. Preserve original source data.

8. Treat public UIDs separately from database IDs.

9. Validate all external input.

10. Perform authorization server-side.

11. Never trust UI authorization alone.

12. Never commit production secrets.

13. Use database migrations.

14. Make retryable operations idempotent.

15. Record sensitive actions in audit logs.

16. Avoid premature microservices.

17. Avoid giant shared utility layers.

18. Avoid circular module dependencies.

19. Keep optional extensions dependent on the core, not the reverse.

20. Document significant architectural decisions.
```

---

# 83. Dependency Direction

Preferred dependency direction:

```text
API
 |
 v
Application
 |
 v
Domain

Infrastructure
 |
 v
Domain Interfaces
```

Domain should not depend on:

- Controllers
- Database frameworks
- HTTP frameworks
- UI frameworks
- External APIs

This keeps core business rules portable and testable.

---

# 84. Module Dependency Rule

Prefer acyclic module dependencies.

If:

```text
Bookings -> Marketplace
```

Marketplace should not simultaneously require:

```text
Marketplace -> Bookings
```

When two modules need to react to one another, events or a neutral contract may remove the circular dependency.

---

# 85. Architecture Decision Records

Significant architectural decisions should be recorded under:

```text
09_DOCUMENTATION/decisions/
```

Recommended naming:

```text
ADR-001-modular-monolith.md
ADR-002-public-uid-strategy.md
ADR-003-flight-data-preservation.md
ADR-004-module-database-ownership.md
```

Each ADR should record:

```text
Context
Decision
Alternatives
Consequences
Status
```

---

# 86. Phase 1 Deployment Model

Initial deployment should remain operationally simple.

Conceptually:

```text
Web
  |
  v
Backend Modular Monolith
  |
  +---- PostgreSQL
  |
  +---- Object Storage
  |
  +---- Notification Providers
```

Ground Agent:

```text
Drone / Ground Station
       |
       v
Ground Agent
       |
       v
Backend API
```

The system may later introduce dedicated workers, queues and independent services when required.

---

# 87. Architecture Evolution Principle

The architecture should optimize for:

```text
Correct boundaries first.
Distributed infrastructure later.
```

The goal is not to predict every future requirement.

The goal is to establish domain boundaries strong enough that future requirements can be added without rewriting the platform.

---

# 88. Core Product Statement

The simplest technical description of Phase 1 is:

> A professional network and work-management platform for the drone ecosystem where drones have persistent digital identities and are connected to owners, pilots, technicians, flights, maintenance activity and service history.

The foundational relationship is:

```text
USER
  |
  v
DRONE
  |
  +---- OWNERSHIP
  |
  +---- PILOT
  |
  +---- FLIGHT
  |
  +---- MAINTENANCE
  |
  +---- WORK
  |
  v
HISTORY
```

Technicians and consumers create the service ecosystem around this core.

Future marketplace, plugin, enterprise, AI and predictive-maintenance capabilities should build on these foundations rather than replace them.

---

# 89. Final Architecture Principle

When making architectural decisions, prefer the design that protects:

```text
Identity
+
Relationships
+
Ownership
+
History
+
Auditability
+
Data Integrity
```

over short-term implementation convenience.

The platform's long-term value depends on the reliability of these records.

---

**End of Architecture Document**

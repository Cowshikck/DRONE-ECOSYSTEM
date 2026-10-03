# Drone Ecosystem Architecture

## Architectural Style

Managed Modular Monolith.

The backend is deployed as a unified application while domain boundaries remain isolated.

## Core Domains

- Identity
- Organizations
- Profiles
- Fleet
- Flights
- Maintenance
- Marketplace
- Bookings
- Payments
- Communications
- Notifications
- Media
- Reports

## Core Principle

User -> Drone -> Pilot -> Work -> History

The architecture must allow individual modules to evolve into independent services later without redesigning the core domain.

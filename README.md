# Consus Energy Management System - as of 02/04/2025

This repository contains the backend system for managing and monitoring domestic battery-inverter units for Consus Energy. It supports real time tracking, control, and future integration with energy market forecasting.

## Overview

The system provides a FastAPI-based REST API, PostgreSQL database integration, and tools for data simulation, validation, and monitoring. It is designed to be robust, extensible, and ready for production deployment.

## Features

- Add, update, and delete batteries with UUID and human-readable identifiers
- Real-time battery data updates (SoC, voltage, temperature, etc.)
- Monitoring scripts to track live status and flag abnormalities
- Unique identifier generator using postcode and capacity
- Battery IP tracking for future device communication
- Centralized schema validation, error handling, and logging
- Alembic-based migrations and TablePlus-compatible inspection

## Technologies

- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- Pydantic (v2)
- Python scripts for monitoring and testing

## Setup

1. Clone the repository
2. Set up a local PostgreSQL database
3. Run Alembic migrations to create tables
4. Start the API server:
   ```bash
   uvicorn cems.main:app --reload
                OR
    ./start.sh

## Program Structure 

cems/
├── app/
│   ├── api/                 # FastAPI route handlers  
│   ├── schemas/             # Pydantic models
│   ├── core/                # DB and logger config
│   └── SQLAlchemy_models/   # SQLAlchemy ORM models
├── scripts/
│   ├── utils/               # Battery creation and deletion tools
│   ├── Battery monitoring/  # Monitoring loop
│   └── battery_actions/     # Conditional Battery Instructions
│    
└── alembic/                 # Alembic config    


## API Highlights

### Battery Management

- `POST /battery`  
  Create a new battery entry. Requires location, capacity, and optional fields like IP address and postal code.

- `GET /battery/{battery_id}`  
  Retrieve a specific battery by its UUID.

- `GET /batteries`  
  Fetch all battery entries in the database.

- `GET /battery?location_prefix=PREFIX`  
  Filter batteries by location/identifier prefix.

- `DELETE /battery/{battery_id}`  
  Delete a specific battery by UUID.

- `DELETE /battery?all=true`  
  Delete all batteries in the system.

- `GET /battery-count`  
  Return the number of battery entries in the system.

### Battery Data Updates

- `POST /battery-data`  
  Update real-time battery data such as:
  - `state_of_charge`
  - `temperature`
  - `power_kw`
  - `voltage`
  - `status` (charging/discharging/idle)
  - `flag` (ok/warning/error)

Returns the updated battery record and saves the record to the battery_history table

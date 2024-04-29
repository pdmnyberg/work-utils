---
title: A technical introduction to PLUPP
---

# PLUPP

- **PollenDB**: Internal administrative platform for pollen measurement and forecasting
- **Pollen API**: An open rest API serving pollen forecasts and measurements
- **Deployment**: A set of deployment scripts and tools

# PollenDB{.shrink}

## Ownership
- **Code:** NBIS is responsible for current development
- **Deployment:** NRM reviews and deploys the system

## Core use
- Input pollen count
- Create reports of pollen count
- Create forecasts
- Synchronize pollen count and forecast data to the Open API

## Core technology
- **Python (3.8)**: Language
- **Django (3.2.9)**: Core web framework
- **jQuery**: Interactivity beyond what django can deliver


# PollenDB: Django
## The good stuff
- A structured way to manage data an complicated types
- Built in support for access rights and user management
- Nice built-in migration tools

## The less good stuff
- Using jQuery will in most cases result in state management that is hard to follow
- Using the built in views can easily lead to complicated/distributed code when trying to build a more interactive user experience
- It can be hard to find the right way to implement complicated validation logic
- The needs of data validation and UX sometimes collide


# Pollen API {.shrink}

## Ownership
- **Code:** NBIS is responsible for current development
- **Deployment:** NBIS deploys the system on NRMS public servers

## Core use
- Serve pollen forecasts and measurements for public use
- Serve data to NRM's website
- Serve data to external actors such as apps and web pages

## Core technology
- **Python (3.12)**: Language
- **Fast API**: API specification and implementation
- **SQLAlchemy**: ORM for database connection
- **PostgreSQL**: Database currently in use


# Pollen API: Fast API
## The good stuff

## The less good stuff

# Pollen API: SQLAlchemy
## The good stuff

## The less good stuff

# Pollen API: PostgreSQL
## The good stuff
- SQL
- In general just nice to work with


# Deployment
## Core use
- Deploying the Pollen API
- Setting up development environment

## Core technology
- **Ansible**: Used to deploy Pollen API and PollenDB
- **Docker**: Used to package requirements of Pollen API and in dev for PollenDB

# Python: PollenDB and Pollen API
## The good stuff
- Commonly used to for many science applications
- Easy to get started with
- Fairly easy to read

## The less good stuff
- The typing is not as convenient as most strictly typed languages
- When typing is not optional it is easy to get sloppy
- Slow compared to other languages
- The GIL (True multithreading is complicated)
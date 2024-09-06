# Accident Reconstruction System

This project implements an accident detection and reconstruction system using Java and Kotlin. 

The system automatically detects accidents, processes vehicle data, and reconstructs the accident situation for further analysis and visualization. 

It includes both a Java and a Kotlin version of the system, demonstrating the use of both languages to practice and improve skills in accident detection algorithms.

## Project Structure

```plaintext
.
├── accident_detection_app         # Accident detection system implemented in Java
│   ├── build.gradle               # Gradle build file
│   ├── gradle
│   └── src
│       └── main
│           └── java
│               └── com
│                   └── example
│                       └── AccidentDetectionApp.java  # Main class for the Java accident detection app
├── accident_detection_app_kotlin  # Accident detection system implemented in Kotlin
│   ├── build.gradle               # Gradle build file
│   ├── src
│   │   └── main
│   │       └── kotlin
│   │           ├── AccidentDetectionApp.kt           # Main class for the Kotlin accident detection app
│   │           └── algorithms
│   │               └── lv0
│   │                   └── ADalgorithmLv0.kt         # Accident detection algorithm (level 0)
│   └── utils
│       └── utils.kt                                  # Utility functions
├── backend                       # Backend configuration
│   ├── config                    # Environment configuration files
│   └── sample_app                # Django-based backend API
├── bootstrap                     # Deployment configuration using Kubernetes and Kustomize
│   ├── backend
│   └── frontend
├── database                      # PostgreSQL database setup scripts
│   ├── create_table_in_postgresql.py
│   └── insert_data_to_postgresql.py
├── frontend                      # Frontend components
│   ├── src
│   │   └── components
│   │       └── Frontend components for accident reconstruction UI
├── library                       # Library for database and S3 integration
│   ├── postgresql_libs.py
│   └── s3_libs.py
└── pyproject.toml                # Project configuration file
```

- **accident_detection_app (Java)**: This directory contains the accident detection system implemented in Java. The key files include:
  - `AccidentDetectionApp.java`: The main class for the accident detection system in Java, which uses rule-based logic to detect accidents from vehicle data.

- **accident_detection_app_kotlin (Kotlin)**: This directory contains the Kotlin implementation of the accident detection system, which mirrors the Java version. The key files include:
  - `AccidentDetectionApp.kt`: The main class for the Kotlin version of the accident detection system.
  - `ADalgorithmLv0.kt`: Rule-based algorithm for detecting accidents (Level 0).
  - `utils.kt`: Utility functions used in the Kotlin application.

- **backend**: The backend provides the infrastructure for managing accident detection data and exposing it through a REST API. It uses Django as the framework and includes:
  - Configuration files (`settings`, `urls.py`) and essential components like the `admin.py` and `models.py`.
  - REST API endpoints to interact with the frontend and store accident data in a database.

- **bootstrap**: Deployment configuration using Kubernetes and Kustomize. This folder contains the YAML files and configurations for setting up the backend and frontend services in different environments, such as development.

- **database**: Contains PostgreSQL scripts to create tables and insert data into the database. This supports the accident detection system by storing reconstructed accident data.
  - `create_table_in_postgresql.py`: Script to create tables for the accident data.
  - `insert_data_to_postgresql.py`: Script to insert accident-related data into the database.

- **frontend**: The frontend is implemented in React and TypeScript, providing a user interface for accident data visualization and interaction with the backend. It includes:
  - Components like `Map.tsx` and `Player.tsx` for displaying accident reconstructions on the UI.
  - Various pages such as the accident reconstruction solution page and authentication page.
  - Recoil state management for handling user authentication and other UI states.

- **library**: Utility libraries for interacting with PostgreSQL and AWS S3. These handle data retrieval and storage for the accident data.
  - `postgresql_libs.py`: Functions for interacting with PostgreSQL databases.
  - `s3_libs.py`: Functions for interacting with AWS S3 to store or retrieve data.

## Key Features

1. **Java and Kotlin Accident Detection**: The project contains both Java and Kotlin implementations of a rule-based accident detection system. The system processes vehicle data and applies rules to detect accidents and trigger the reconstruction process.

2. **Backend API**: The Django-based backend exposes APIs to manage accident data, enabling the frontend to retrieve and display the reconstructed accidents.

3. **Frontend Accident Visualization**: The frontend UI allows users to visualize the reconstructed accident events. It includes a map view and other components that help illustrate the sequence of events leading up to an accident.

4. **Deployment with Kubernetes**: Kubernetes and Kustomize configurations are provided to deploy the entire system (backend, frontend, and database) to a development or production environment.

5. **Database Integration**: PostgreSQL is used to store accident data, with predefined schemas and tables. Accident data is inserted into the database and can be queried through the backend API.

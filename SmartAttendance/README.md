# Smart Attendance System

A Python-based university attendance management system built with **Flask** and **SQLite**. The application allows teachers to manage classroom attendance through secure, time-limited sessions while students can check in by scanning QR codes directly from their browsers.

Designed to simplify attendance tracking, reduce manual work, and provide an efficient way to manage student participation in university courses.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Mobile Network Access](#mobile-network-access)

---

## Overview

The system provides two main interfaces:

- **Student Portal:** Students can log in and mark their attendance by scanning a QR code using their device's camera.
- **Teacher Dashboard:** Teachers can manage attendance sessions, generate access codes, and import student rosters.

Attendance sessions are automatically managed by the backend, ensuring students can only check in during the permitted time window.

---

## System Architecture

### Backend — Flask

The Python `app.py` file serves as the main application server, responsible for:

- Handling HTTP requests and application routes.
- Processing student authentication.
- Creating and validating attendance sessions.
- Managing database operations.
- Providing teacher dashboard functionality.

### Database — SQLite

The application uses SQLite for lightweight relational data storage.

The database (`database.db`) contains three main tables:

| Table | Description |
|---|---|
| `students` | Stores student information. |
| `classes` | Stores classroom and course information. |
| `student_courses` | Manages student enrollment across multiple courses. |

### Frontend — HTML, CSS & JavaScript

The frontend uses HTML, CSS, and JavaScript, with pages rendered through Flask templates.

The student portal utilizes the browser's native camera capabilities and `BarcodeDetector` API to scan QR codes without requiring a separate mobile application.

---

## Key Features

### QR Code Attendance

- Browser-native QR code scanning.
- Camera access through `navigator.mediaDevices`.
- QR recognition using the `BarcodeDetector` API.
- Supports compatible desktop and mobile browsers.

### Automated Attendance Sessions

- Generates unique 6-digit attendance codes.
- Automatically expires sessions after 30 minutes.
- Prevents late attendance submissions.
- Validates attendance through the Flask backend.

### Student Management

- SQLite-based student records.
- Multiple course enrollment support.
- Relational database structure.

### Teacher Dashboard

- Dedicated teacher authentication.
- Attendance session management.
- Bulk student registration through CSV imports.
- Efficient management of large student rosters.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Relational database |
| HTML5 | Frontend structure |
| CSS3 | Frontend styling |
| JavaScript | Client-side functionality |
| BarcodeDetector API | QR code recognition |
| MediaDevices API | Camera access |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/elyas-hassan/smart-attendance.git
cd smart-attendance
```

### 2. Install Dependencies

```bash
pip install Flask
```

---

## Configuration

### Teacher Password

The default teacher password is `12345`. It is strongly recommended to change it before running the application.

**Windows PowerShell:**

```powershell
$env:TEACHER_PASSWORD="YourNewPassword"
```

**macOS / Linux:**

```bash
export TEACHER_PASSWORD="YourNewPassword"
```

Alternatively, for local testing, modify the `TEACHER_PASSWORD` variable in `app.py`.

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Access the application through your browser:

| Interface | URL |
|---|---|
| Student Portal | http://127.0.0.1:5000 |
| Teacher Dashboard | http://127.0.0.1:5000/teacher/login |

---

## Mobile Network Access

To test QR code scanning using your phone's camera, both your computer and phone must be connected to the same Wi-Fi network.

By default, Flask uses `127.0.0.1`, which only allows connections from the local machine.

### 1. Update the Flask Host

In `app.py`, locate the `app.run()` statement and change it to:

```python
app.run(debug=False, host="0.0.0.0", port=5000)
```

### 2. Restart the Server

```bash
python app.py
```

### 3. Find Your Computer's IP Address

On Windows, open Command Prompt:

```cmd
ipconfig
```

Find your local IPv4 address (for example, `192.168.1.15`).

### 4. Access the Application from Your Phone

Open your phone's browser and navigate to:

`http://192.168.1.15:5000`

Replace the IP address with your computer's actual IPv4 address.

**Note:** Browser camera access generally requires HTTPS or localhost. Accessing the application through a local HTTP IP address may prevent camera scanning from working. For testing over the network, use an HTTPS tunneling service such as [ngrok](https://ngrok.com/) (`ngrok http 5000`).



# [betterbetterKAU](https://betbetkau.web.app/)

A client-side web application built for King Abdulaziz University students to plan, build, and export optimized weekly class schedules. 

Originally developed as an enhanced iteration of [BetterKAU](https://betterkau.com), this project features a dynamic time-grid renderer, local storage persistence, custom event scheduling, and real-time PNG exports.
## Key Features

* **Dynamic Time Grid:** Automatically calculates the earliest start time and latest end time across all enrolled courses to resize the visual schedule grid without dead space.
* **Pre-built Plan Loader:** Supports instant loading of pre-configured schedule templates for academic tracks.
* **Custom Event Modal:** Allows students to add a custom course if it wasn't in the site with custom times, days, and sections.
* **Theme-Aware Color Engine:** Assigns distinct HSL color profiles to course groups with synchronized dynamic color picker support.
* **Schedule Image Export:** Renders the schedule grid into a clean, high-resolution PNG file using `html2canvas` while temporarily stripping out interactive UI controls.
* **Local Storage Synchronization:** Automatically saves and restores course selections, total credit hours, custom events, and dark/light mode preferences.

## Technical Overview

### 1. Dynamic Grid Bounds Calculation (`updateGridBounds`)
Rather than relying on a hardcoded 8:00 AM – 5:00 PM timeline, the application converts all class start and end timestamps into absolute minutes from midnight. It evaluates the global minimum start time and maximum end time across the schedule array, floors/ceils the hour boundaries, and dynamically updates the DOM column heights.

### 2. Time-Block Coordinate Rendering (`renderEvent`)
Class blocks are dynamically placed within day columns using calculated CSS offsets. Using a fixed hour height variable (`HOUR_HEIGHT = 100px`)

### 3. Synchronized State Management
Courses containing multiple time blocks (such as separate lectures and labs) share a unique `groupId`. Deleting an event or changing its display color instantly synchronizes across all linked DOM elements and updates the global credit hour total.

## Tech Stack

* **Frontend:** HTML5, CSS3 (CSS Variables), JavaScript (Vanilla ES6+)
* **Libraries:** `html2canvas` (Canvas Image Export)
* **Storage:** Browser `localStorage` API

## Local Setup

Since this is a lightweight, pure client-side application, no backend server or Node.js environment is required

1. just Clone the repository
2. Open index.html directly in any modern browser.

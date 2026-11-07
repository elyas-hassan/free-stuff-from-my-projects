# AutoDraw:

A Python-based desktop application that converts standard images into optimized black-and-white line art and automatically renders them onto any digital canvas using OS-level mouse macros. 

## Technical Overview
The system processes images using OpenCV for noise reduction and edge detection, translating the resulting pixels into a spatial coordinate map. A Tkinter overlay acts as a transparent bounding box to establish the screen space, and PyAutoGUI executes the rendering in two passes (outlines and scanline fills).

## Features
* **Computer Vision Pipeline:** Converts images to grayscale, applies a Gaussian Blur for noise reduction, and utilizes Canny Edge Detection (thresholds 50, 150) to generate clean line paths.
* **Two-Pass Rendering Engine:** 
  * *Pass 1 (Outlines):* Uses `cv2.findContours` to trace continuous smooth borders.
  * *Pass 2 (Fills):* Implements a horizontal scanline algorithm to drag and fill internal shapes efficiently.
* **Spatial Bounding UI:** A semi-transparent Tkinter window that users physically drag over their target drawing area; the app calculates all starting coordinates and offsets relative to this window's geometry.
* **Hardware Fail-safes:** Built-in cooldowns (pausing 2.5 seconds every 100 actions) and standard PyAutoGUI fail-safes to prevent OS control lockouts.

## Tech Stack
* **Image Processing:** OpenCV (`cv2`), Pillow (PIL), NumPy
* **Automation:** PyAutoGUI
* **GUI:** Tkinter

## Usage
1. Execute `run_drawer_app.py`.
2. Select an image and define the output width and brush offset (step size).
3. Click Preview: The UI window will resize to the exact output dimensions.
4. Drag the transparent UI window over your target canvas (e.g., MS Paint, web canvas).
5. Click Start Drawing. Do not touch the mouse until the sequence completes.

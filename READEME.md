# Falling Lambs

A computer vision game where you use hand gestures to catch falling lambs and avoid wolves using your webcam.

## Overview

This project combines hand tracking with OpenCV to create an interactive game. Use your thumb and index finger to create a "pinching" gesture that acts as a catching mechanism to grab lambs (gain points) and avoid wolves (lose points).

## Requirements

- Python 3.7+
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- NumPy

## Installation

1. Install the required dependencies:
```bash
pip install opencv-python mediapipe numpy
```

2. Prepare your image assets in an `Images/` folder:
   - `sheep.png` - Image of a lamb (will be resized to 40x40)
   - `wolf.png` - Image of a wolf (will be resized to 40x40)

## How to Play

1. Run the main game:
```bash
python FallingLambs.py
```

2. **Game Mechanics:**
   - Objects fall from the top of the screen every 2 seconds
   - Use your thumb and index finger to pinch/catch objects
   - **Catch lambs**: +1 point
   - **Catch wolves**: -1 point
   - **Miss a lamb**: -1 point
   - **Game Over**: When points drop below 0

3. **Controls:**
   - Position your thumb and index finger around falling objects
   - The line between your thumb and index finger is the catching zone

## File Structure

- `FallingLambs.py` - Main game loop and logic
- `HandTrackingModule.py` - Hand detection wrapper using MediaPipe
- `Images/` - Directory for game asset images

## Features

- Real-time hand tracking using MediaPipe
- FPS counter for performance monitoring
- Dynamic object spawning (lambs and wolves)
- Alpha channel support for transparent PNG images
- Game over detection

## Notes

- Ensure your webcam is connected and accessible
- Good lighting conditions improve hand detection accuracy
- The game requires a 640x480 resolution camera feed
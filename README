# Camera Position Calibration and Visualization

## Overview
This repository provides a framework for processing, calibrating, and visualizing camera positions based on ground truth data. It is designed to handle camera calibration sequences, estimate missing positions, correct orientations, and visualize results using an interactive UI.

## Features
- **JSON Handling**: Loads, saves, and updates calibration data in JSON format.
- **Data Processing**: Prepares camera data, applies transformations, and estimates missing positions.
- **Calibration**: Updates ground truth data and corrects camera orientations.
- **Interpolation**: Uses short-arc interpolation to estimate missing positions.
- **Visualization**: Generates interactive plots to analyze calibrated and uncalibrated positions.
- **User Interface**: Provides a UI for reviewing and modifying calibration data.

---

## Directory Structure
```
./
├── data                # Handles data loading, processing, and transformation
│   ├── json_handler.py         # Manages JSON loading, saving, and updating
│   ├── preprocessing.py        # Preprocesses sequences before analysis
│   └── sequence_handler.py     # Manages sequence structure and mapping
├── processing          # Algorithms for estimating positions and correcting errors
│   ├── angular_transform.py    # Converts angles to coordinate positions
│   ├── circle_estimator.py     # Estimates circular paths for camera movement
│   ├── cluster_calibrator.py   # Adjusts clusters of camera positions
│   ├── orientation_corrector.py# Corrects camera orientation based on data
│   ├── position_estimator.py   # Estimates missing positions using known data
│   └── short_arc_interpolator.py # Adjusts positions using interpolation
├── scripts             # Utility scripts for updating all sequences
│   └── update_all_sequences.py  # Script to update ground truth with new calibration data
├── ui                  # User interface components
│   ├── __init__.py     # UI initialization
│   ├── iu_helpers.py   # Helper functions for UI elements
│   ├── ui_callbacks.py # UI event handlers
│   └── ui_layout.py    # Layout definition for the Gradio UI
├── utils               # Utility functions and constants
│   ├── constants.py    # Stores global constants
│   ├── math_utils.py   # Mathematical utilities
│   └── time_utils.py   # Time-related utilities
├── visualization       # Data visualization components
│   ├── plotter.py      # Generates interactive plots
│   └── reference_points.py # Stores reference points for visual alignment
├── config.py           # Configuration file with paths and parameters
├── main.py             # Main script to launch the UI
└── __init__.py         # Package initialization
```

---

## Installation
### Prerequisites
Ensure you have Python installed (>= 3.7). Install required dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage
### Running the UI
Launch the interactive UI to visualize and edit calibration data:
```bash
python main.py
```

### Updating Ground Truth
To update camera positions using new calibrated data, run:
```bash
python scripts/update_all_sequences.py
```

---

## Core Components
### JSON Data Handling
- `data/json_handler.py` loads and saves ground truth data.
- `update_ground_truth()` updates calibrated cameras and marks others as uncalibrated.
- `transform_to_schema()` ensures JSON data follows a structured format.

### Processing and Calibration
- `angular_transform.py`: Converts angles into coordinates.
- `orientation_corrector.py`: Corrects camera orientations using computed offsets.
- `position_estimator.py`: Estimates missing positions based on timestamps.
- `short_arc_interpolator.py`: Adjusts uncalibrated positions using interpolation.

### Visualization
- `plotter.py`: Generates plots to analyze calibration results.
- `reference_points.py`: Stores known reference locations.

### User Interface
- `ui_layout.py`: Defines UI components.
- `ui_callbacks.py`: Handles UI interactions and updates JSON files.

---


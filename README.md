# Pipewire Sample Rate Selector

A simple python app for Pipewire audio settings. With a simple GUI, allowing you to select sample rates and buffer sizes.

## Features

- Select allowed sample rates (44.1 kHz - 192kHz)
- Select buffer sizes (32 – 2048 samples)
- Apply changes instantly
- Simple, intuitive GUI

## Requirements

- Linux with Pipewire installed
- Python 3.12 or newer (Tkinter included)
- UV package manager (desired but optional)

## How to Use

1. Open a terminal.
2. Go to the project directory.
3. Run:

   With UV package manager

   ```bash
   uv run main.py
   ```

   Or directly run

   ```bash
   python3 main.py
   ```

4. In the window that appears, the current sample rate and buffer size are displayed.
5. Click your desired sample rate/buffer size.
6. Changes take effect immediately.
7. Enjoy your audio!

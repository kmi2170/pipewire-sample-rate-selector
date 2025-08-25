# Pipewire Sample Rate Selector

A simple python GUI widget for managing Pipewire audio sample rate and buffer (quantum) size settings for optimal sound quality.

## Features

- Select allowed sample rates (44.1 kHz - 192kHz)
- Select buffer sizes (32 – 2048 samples)
- Apply changes instantly
- Simple, intuitive GUI with the use of ttk (Themed TK) for a more modern look and feel
- GUI consists of 4 parts

  - Display the current sample rate and buffer size
  - The button group for selecting sample rate
  - The button group for selecting buffer size
  - The control buttons:

    Exit: Terminate the app

    Sync: Synchronize the displayed sample rate and buffer size with the actual ones (You normally don't need to use this. Just in case for the sample rate and buffer size has changed by other ways)

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

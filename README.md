# VBAN Desktop

A lightweight desktop application to manage VBAN streams with a GUI and system tray integration. Built with **Python**, **PyQt5**, **pystray**, and **Pillow**.  

 ⚠️ **Currently, this application only supports Linux. Windows support is not yet implemented.**



## Features

- Run and stop a VBAN receiver (`vban_receptor`) from a desktop app.
- Configure host, port, stream, and executable path via a GUI.
- Minimized to system tray with a tray icon menu:
  - Open configuration window
  - Quit application
- Simple configuration persistence via `vban_config.py`.



## Requirements

- Python 3.8 or higher
- Linux system
- VBAN Receiver executable (`vban_receptor`) installed and accessible in your PATH.
- Audio backend: `alsa`
- Dependencies listed in `requirements.txt`:

## Installation


1. Clone this repository:

```bash
git clone https://github.com/leandrofus/vban-desktop.git
cd vban-desktop
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```pip install -r requirements.txt```

4. Configure VBAN path and settings in vban_config.py, or via the GUI.

## Usage


Run the application:

```bash
python main.py
```

* The application will start the VBAN receiver automatically.

* The tray icon allows quick access to configuration and quitting the app.

* Any changes in the configuration window will restart the VBAN receiver.
```bash
git checkout -b feature/my-feature
git push origin feature/my-feature
```
* Use Pull Requests to merge changes into main.

## License


MIT License © 2025 Leandro Fusco

## Contact


For questions or issues, reach out to Leandro Fusco or open an issue in the GitHub repository.

# ContainerExecuter

A GUI tool for intuitive Docker container management.
Built with PyQt5, it allows you to start, stop, and attach to containers, as well as perform bulk deletion of containers and their base images.

[日本語版はこちら (README_ja.md)](README_ja.md)

## Key Features

- **Container Management**: Display running containers and perform Start/Stop operations.
- **Shell Access**: Open a container shell in a new terminal with a single click.
- **Bulk Deletion**: Toggle to "Edit Mode" to delete a container and its base image simultaneously.
- **Visuals**: Modern GUI with random background images.
- **CLI Integration**: Provides `ce` (Launch GUI) and `dock` (Quick attach via fzf) commands.

## UI Modes

### Standard Mode
Used for daily operations like starting, stopping, and accessing the shell.
![Standard Mode](docs/standard_mode.png)

### Edit Mode
Used for cleaning up your environment by deleting containers and images.
![Edit Mode](docs/edit_mode.png)

## Installation

Run the following command in the repository root:

```bash
bash install.sh
```

This script automatically handles:
1. Installation of common prerequisites (curl, etc.).
2. Docker installation (if missing).
3. NVIDIA Container Toolkit installation (if GPU is detected).
4. Application dependencies (PyQt5, fzf, gnome-terminal, etc.).
5. Adding aliases (`ce`) and helper functions (`dock`) to your `.bashrc`.

*Note: You may need to log out and log back in for the Docker group settings to take effect.*

## Usage

### Launch GUI
Type the following in your terminal:
```bash
ce
```

### Quick Attach via CLI
A helper function using `fzf` is provided to quickly select and enter a running container.
```bash
dock
```

## Requirements
- OS: Linux (Ubuntu recommended)
- Python 3.x
- Docker
- (Optional) NVIDIA GPU & Driver

## License
[MIT License](LICENSE)

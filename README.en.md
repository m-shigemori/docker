# ContainerExecuter

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

[JA](README.md) | [EN](README.en.md)

An intuitive GUI tool for Docker container management, specifically designed for use with ROS 2 Humble and Jazzy.
Built with PyQt5, it streamlines starting, stopping, and attaching to containers, while also providing a simplified way to perform bulk deletions of containers and their base images.

## Key Features

- **Container Management**: View running containers and easily perform Start/Stop operations.
- **Shell Access**: Open a container shell in a new terminal with a single click.
- **Bulk Deletion**: Use "Edit Mode" to delete containers and their base images simultaneously.
- **Visuals**: Modern GUI with random background images.
- **CLI Integration**: Includes `ce` (Launch GUI) and `dock` (Quick attach via fzf) commands.

## UI Modes

| Standard Mode | Edit Mode |
| :---: | :---: |
| <img src="docs/standard_mode.png" width="400"> | <img src="docs/edit_mode.png" width="400"> |
| Daily operations such as starting, stopping, and accessing the shell. | Environment cleanup and management. |

## Installation

Run the following command in the repository root:

```bash
bash install.sh
```

This script automatically handles Docker/NVIDIA setup, dependency installation, and CLI alias configuration.

*Note: Please log out and back in after installation to apply the changes.*

## Usage

### Launch GUI
```bash
ce
```

### Quick Attach via CLI
Use the provided helper function to quickly select and enter a running container via `fzf`.
```bash
dock
```

## Docker Container Setup

You can easily build optimized Docker containers for each project using the scripts in `container/Dockerfiles`.

### 1. Project Naming (Copy Directory)
Copy the `container` directory to match your project name. This name will be used as the Docker image and container (project) name.

```bash
cp -r container/ <project_name>/
```

### 2. Configuration (.env)
Edit `<project_name>/Dockerfiles/.env` to configure settings such as ROS distribution and GPU usage.

```bash
# Example: .env
ROS_DISTRO=jazzy
USE_GPU=true
```

### 3. Launch Container
Run the following script to build and start the container.

```bash
bash <project_name>/Dockerfiles/up.sh
```

## Requirements

- OS: Linux (Ubuntu recommended)
- Python 3.x
- Docker

## License

[MIT License](LICENSE)

## Special Thanks

Background images are from "[Gakuen Idolmaster](https://gakuen.idolmaster-official.jp/)".

[contributors-shield]: https://img.shields.io/github/contributors/m-shigemori/docker?style=for-the-badge
[contributors-url]: https://github.com/m-shigemori/docker/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/m-shigemori/docker?style=for-the-badge
[forks-url]: https://github.com/m-shigemori/docker/network/members
[stars-shield]: https://img.shields.io/github/stars/m-shigemori/docker?style=for-the-badge
[stars-url]: https://github.com/m-shigemori/docker/stargazers
[issues-shield]: https://img.shields.io/github/issues/m-shigemori/docker?style=for-the-badge
[issues-url]: https://github.com/m-shigemori/docker/issues
[license-shield]: https://img.shields.io/github/license/m-shigemori/docker?style=for-the-badge
[license-url]: https://github.com/m-shigemori/docker/blob/main/LICENSE

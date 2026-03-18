# ContainerExecuter

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

[JA](README.md) | [EN](README.en.md)

An intuitive GUI tool for Docker container management.
Built with PyQt5, it streamlines starting, stopping, and attaching to containers, while also providing a simplified way to perform bulk deletions of containers and their base images.

## Key Features

- **Container Management**: View running containers and easily perform Start/Stop operations.
- **Shell Access**: Open a container shell in a new terminal with a single click.
- **Bulk Deletion**: Use "Edit Mode" to delete containers and their base images simultaneously.
- **Visuals**: Modern GUI with random background images.
- **CLI Integration**: Includes `ce` (Launch GUI) and `dock` (Quick attach via fzf) commands.

## UI Modes

### Standard Mode
Daily operations such as starting, stopping, and accessing the shell.
![Standard Mode](docs/standard_mode.png)

### Edit Mode
Environment cleanup and management.
![Edit Mode](docs/edit_mode.png)

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

## Requirements

- OS: Linux (Ubuntu recommended)
- Python 3.x
- Docker

## License

[MIT License](LICENSE)

[contributors-shield]: https://img.shields.io/github/contributors/m-shigemori/docker.svg?style=for-the-badge
[contributors-url]: https://github.com/m-shigemori/docker/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/m-shigemori/docker.svg?style=for-the-badge
[forks-url]: https://github.com/m-shigemori/docker/network/members
[stars-shield]: https://img.shields.io/github/stars/m-shigemori/docker.svg?style=for-the-badge
[stars-url]: https://github.com/m-shigemori/docker/stargazers
[issues-shield]: https://img.shields.io/github/issues/m-shigemori/docker.svg?style=for-the-badge
[issues-url]: https://github.com/m-shigemori/docker/issues
[license-shield]: https://img.shields.io/github/license/m-shigemori/docker.svg?style=for-the-badge
[license-url]: LICENSE

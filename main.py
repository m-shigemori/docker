import sys
from PyQt5.QtWidgets import QApplication
from src.config.settings import StyleConfig
from src.infrastructure.docker_repository import DockerRepository
from src.application.use_cases.container_use_cases import ContainerService
from src.interfaces.gui.main_window import MainWindow

def main():
    config = StyleConfig()
    docker_repo = DockerRepository()
    container_service = ContainerService(docker_repo)
    app = QApplication(sys.argv)
    window = MainWindow(container_service, config)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

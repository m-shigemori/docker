import sys
import os
import signal

os.environ["QT_LOGGING_RULES"] = "qt.core.socketnotifier=false"

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QLoggingCategory, pyqtRemoveInputHook
    
    pyqtRemoveInputHook()
    
    QLoggingCategory.setFilterRules("qt.core.socketnotifier=false")
    
    from src.config.settings import StyleConfig
    from src.infrastructure.docker_repository import DockerRepository
    from src.application.use_cases.container_use_cases import ContainerService
    from src.interfaces.gui.main_window import MainWindow
    
    config = StyleConfig()
    docker_repo = DockerRepository()
    container_service = ContainerService(docker_repo)
    
    stderr_fd = sys.stderr.fileno()
    with os.fdopen(os.dup(stderr_fd), 'w') as old_stderr:
        with open(os.devnull, 'w') as devnull:
            os.dup2(devnull.fileno(), stderr_fd)
            try:
                app = QApplication(sys.argv)
            finally:
                os.dup2(old_stderr.fileno(), stderr_fd)
    
    window = MainWindow(container_service, config)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

#Tryton/tests/test_app.py
import unittest
from unittest.mock import patch, MagicMock
from src.app import manage_containers, main
from src.container_manager import ContainerManager
from src.docker_manager import DockerManager

class TestApp(unittest.TestCase):

    @patch('src.container_manager.ContainerManager.check_if_container_exists')
    @patch('src.container_manager.ContainerManager.check_if_container_stopped')
    @patch('src.container_manager.ContainerManager.start_container')
    @patch('src.container_manager.ContainerManager.create_and_start_container')
    @patch('src.container_manager.ContainerManager.setup_tryton_database')
    def test_manage_containers(self, mock_setup_db, mock_create_start, mock_start, mock_check_stopped, mock_check_exists):
        mock_check_exists.side_effect = [True, False]
        mock_check_stopped.return_value = True

        container_manager = ContainerManager()
        containers = ["tryton-postgres", "tryton"]

        manage_containers(container_manager, containers)
        
        mock_check_exists.assert_any_call("tryton-postgres")
        mock_check_exists.assert_any_call("tryton")
        mock_check_stopped.assert_called_once_with("tryton")
        mock_start.assert_called_once_with("tryton")
        mock_create_start.assert_not_called()
        mock_setup_db.assert_not_called()

    @patch('src.docker_manager.DockerManager.initialize_docker')
    @patch('src.container_manager.ContainerManager.check_if_container_exists')
    @patch('src.container_manager.ContainerManager.check_if_container_stopped')
    @patch('src.container_manager.ContainerManager.start_container')
    @patch('src.container_manager.ContainerManager.create_and_start_container')
    @patch('src.container_manager.ContainerManager.setup_tryton_database')
    def test_main(self, mock_setup_db, mock_create_start, mock_start, mock_check_stopped, mock_check_exists, mock_initialize_docker):
        mock_initialize_docker.return_value = None
        mock_check_exists.side_effect = [True, False]
        mock_check_stopped.return_value = True

        main()

        mock_initialize_docker.assert_called_once()
        mock_check_exists.assert_any_call("tryton-postgres")
        mock_check_exists.assert_any_call("tryton")
        mock_check_stopped.assert_called_once_with("tryton")
        mock_start.assert_called_once_with("tryton")
        mock_create_start.assert_not_called()
        mock_setup_db.assert_not_called()

if __name__ == '__main__':
    unittest.main()

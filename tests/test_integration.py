#Tryton/tests/test_integration.py
import unittest
from unittest.mock import patch, MagicMock
from src.app import main
from src.docker_manager import DockerManager
from src.container_manager import ContainerManager

class TestIntegration(unittest.TestCase):

    @patch('src.docker_manager.DockerManager.check_docker')
    @patch('src.docker_manager.DockerManager.is_docker_running')
    @patch('src.container_manager.ContainerManager.check_if_container_exists')
    @patch('src.container_manager.ContainerManager.check_if_container_stopped')
    @patch('src.container_manager.ContainerManager.start_container')
    @patch('src.container_manager.ContainerManager.create_and_start_container')
    @patch('src.container_manager.ContainerManager.setup_tryton_database')
    def test_full_integration(self, mock_setup_db, mock_create_start, mock_start, mock_check_stopped, mock_check_exists, mock_is_running, mock_check_docker):
        mock_check_docker.return_value = None
        mock_is_running.return_value = True
        mock_check_exists.side_effect = [False, False]
        mock_check_stopped.side_effect = [False, False]

        main()

        mock_check_docker.assert_called_once()
        mock_is_running.assert_called_once()
        mock_check_exists.assert_any_call("tryton-postgres")
        mock_check_exists.assert_any_call("tryton")
        mock_check_stopped.assert_any_call("tryton-postgres")
        mock_check_stopped.assert_any_call("tryton")
        mock_create_start.assert_any_call("tryton-postgres")
        mock_create_start.assert_any_call("tryton")
        mock_setup_db.assert_called_once()

if __name__ == '__main__':
    unittest.main()

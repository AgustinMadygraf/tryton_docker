#Tryton/tests/test_container_manager.py
import unittest
from unittest.mock import patch, MagicMock
from src.container_manager import ContainerManager

class TestContainerManager(unittest.TestCase):

    @patch('src.container_manager.subprocess.run')
    def test_check_if_container_exists(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'tryton-postgres\n', stderr=b'')
        container_manager = ContainerManager()
        exists = container_manager.check_if_container_exists('tryton-postgres')
        self.assertTrue(exists)

    @patch('src.container_manager.subprocess.run')
    def test_check_if_container_stopped(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'tryton-postgres\n', stderr=b'')
        container_manager = ContainerManager()
        stopped = container_manager.check_if_container_stopped('tryton-postgres')
        self.assertTrue(stopped)

    @patch('src.container_manager.subprocess.run')
    def test_start_container(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'Success', stderr=b'')
        container_manager = ContainerManager()
        container_manager.start_container('tryton-postgres')
        mock_run.assert_called_once()

    @patch('src.container_manager.subprocess.run')
    def test_create_and_start_container(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'Success', stderr=b'')
        container_manager = ContainerManager()
        container_manager.create_and_start_container('tryton-postgres')
        mock_run.assert_called_once()

    @patch('src.container_manager.subprocess.run')
    def test_setup_tryton_database(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'Success', stderr=b'')
        container_manager = ContainerManager()
        container_manager.setup_tryton_database()
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()

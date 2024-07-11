#Tryton\tests\test_docker_manager.py
import subprocess
import unittest
from unittest.mock import patch, MagicMock
from src.docker_manager import DockerManager

class TestDockerManager(unittest.TestCase):

    @patch('src.docker_manager.subprocess.run')
    def test_check_docker(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'Docker version 20.10.7', stderr=b'')
        docker_manager = DockerManager()
        docker_manager.check_docker()
        mock_run.assert_called_with(['docker', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @patch('src.docker_manager.subprocess.run')
    def test_is_docker_running(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'Server: Docker Engine', stderr=b'')
        docker_manager = DockerManager()
        result = docker_manager.is_docker_running()
        self.assertTrue(result)

    @patch('src.docker_manager.subprocess.run')
    def test_initialize_docker(self, mock_run):
        mock_run.side_effect = [MagicMock(stdout=b'Docker version 20.10.7', stderr=b''), MagicMock(stdout=b'Server: Docker Engine', stderr=b'')]
        docker_manager = DockerManager()
        docker_manager.initialize_docker()
        self.assertTrue(mock_run.called)

if __name__ == '__main__':
    unittest.main()



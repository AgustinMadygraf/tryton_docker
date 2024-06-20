# tests/test_docker_operations.py
import subprocess
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from ..src.docker_operations import run_docker_command, check_if_container_exists, create_and_start_container, setup_tryton_database

class TestDockerOperations(unittest.TestCase):
    
    @patch('src.docker_operations.subprocess.run')
    def test_run_docker_command_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'Success', stderr=b'')
        output = run_docker_command(['docker', '--version'], "Docker está instalado.", "Docker no está instalado o no está en el PATH.")
        self.assertEqual(output, 'Success')
    
    @patch('src.docker_operations.subprocess.run')
    def test_run_docker_command_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd='docker --version', stderr=b'Error')
        with self.assertRaises(subprocess.CalledProcessError):
            run_docker_command(['docker', '--version'], "Docker está instalado.", "Docker no está instalado o no está en el PATH.")
    
    @patch('src.docker_operations.subprocess.run')
    def test_check_if_container_exists(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'tryton-postgres\n', stderr=b'')
        exists = check_if_container_exists('tryton-postgres')
        self.assertTrue(exists)
    
    @patch('src.docker_operations.subprocess.run')
    def test_create_and_start_container(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b'Success', stderr=b'')
        create_and_start_container('tryton-postgres')
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()

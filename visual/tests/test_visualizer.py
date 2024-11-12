import main  # Импортируйте ваш основной модуль
import unittest
import os
from unittest.mock import patch, mock_open, MagicMock
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDependencyVisualizer(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='path/to/plantuml,path/to/repo,path/to/output/image.png')
    def test_read_config(self, mock_file):
        visualizer_path, repository_path, output_image_path = main.read_config('fake_config.csv')
        self.assertEqual(visualizer_path, 'path/to/plantuml')
        self.assertEqual(repository_path, 'path/to/repo')
        self.assertEqual(output_image_path, 'path/to/output/image.png')

    @patch('git.Repo')
    def test_get_commits(self, mock_repo):
        # Создаем мок для проверки с веткой main и master
        mock_commit = MagicMock()
        mock_commit.hexsha = '123456'
        mock_commit.parents = []
        mock_repo.return_value.iter_commits.return_value = [mock_commit]

        commits = main.get_commits('path/to/repo')
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].hexsha, '123456')

    def test_generate_plantuml(self):
        mock_commit1 = MagicMock()
        mock_commit1.hexsha = 'commit1'
        mock_commit1.parents = []
        mock_commit2 = MagicMock()
        mock_commit2.hexsha = 'commit2'
        mock_commit2.parents = [mock_commit1]

        commits = [mock_commit1, mock_commit2]
        result = main.generate_plantuml(commits)
        expected = "@startuml\ncommit1 -> commit2\n@enduml"
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_plantuml_to_file(self, mock_file):
        content = "@startuml\ncommit1 -> commit2\n@enduml"
        main.save_plantuml_to_file(content, 'output.txt')
        mock_file().write.assert_called_once_with(content)

    @patch('subprocess.run')
    def test_visualize_graph(self, mock_run):
        visualizer_path = '/path/to/plantuml'
        plantuml_file = 'output.txt'
        output_image_path = 'image.png'

        mock_run.return_value.returncode = 0  # Эмулируем успешное выполнение
        main.visualize_graph(visualizer_path, plantuml_file, output_image_path)
        mock_run.assert_called_once_with([visualizer_path, plantuml_file, "-o", output_image_path], capture_output=True, text=True)

if __name__ == '__main__':
    unittest.main()

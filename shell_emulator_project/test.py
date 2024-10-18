import unittest
from main import ShellEmulator  # Импорт ShellEmulator из файла main.py

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.shell = ShellEmulator("test_user", "test_fs.zip", "test_log.xml")
        self.shell.filesystem = {
            "/file1.txt": "Content of file1",
            "/file2.txt": "Content of file2",
            "/dir1/": "",
        }

    def test_ls(self):
        result = self.shell.ls()
        self.assertIn("/file1.txt", result)

    def test_cd(self):
        self.shell.cd("/dir1/")
        self.assertEqual(self.shell.current_dir, "/dir1/")

    def test_cat(self):
        result = self.shell.cat("/file1.txt")
        self.assertEqual(result, "Content of file1")

    def test_rm(self):
        self.shell.rm("/file1.txt")
        self.assertNotIn("/file1.txt", self.shell.filesystem)

    def test_exit(self):
        result = self.shell.exit()
        self.assertEqual(result, "Exiting shell.")


if __name__ == "__main__":
    unittest.main()

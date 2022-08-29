import os.path
import unittest

from terravacuum import rpath


class TestRPath(unittest.TestCase):
    def test_set(self):
        if os.path.isdir('data_tests/rpath/testdir/'):
            os.rmdir('data_tests/rpath/testdir/')

        rpath.set_dir('data_tests/rpath/testdir/')
        self.assertTrue(os.path.isdir('data_tests/rpath/testdir/'))
        rpath.set_dir('data_tests/rpath/testdir_persistent/')
        self.assertTrue(os.path.isdir('data_tests/rpath/testdir_persistent/'))

    def test_get(self):
        if os.path.isdir('data_tests/rpath/testdir_persistent/test_file.yml'):
            os.remove('data_tests/rpath/testdir_persistent/test_file.yml')

        rpath.set_dir('data_tests/rpath/testdir_persistent/')
        path = rpath.get()
        self.assertTrue(os.path.isdir(path))

        path = rpath.get('test_file.yml')
        with open(path, 'w') as file:
            file.write('A')
        self.assertTrue(os.path.isfile(path))

    def test_cd(self):
        if os.path.isdir('data_tests/rpath/testdir_persistent/child'):
            os.rmdir('data_tests/rpath/testdir_persistent/child')

        rpath.set_dir('data_tests/rpath')
        rpath.cd('child')
        path = rpath.get('test_file.yml')
        with open(path, 'w') as file:
            file.write('A')
        self.assertTrue(os.path.isfile(path))

    def test_default(self):
        rpath.reset()
        self.assertEqual(os.path.join(os.getcwd(), ''), rpath.get())

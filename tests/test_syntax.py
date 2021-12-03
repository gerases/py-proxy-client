"""Test syntax compliance"""

import glob
import os
import unittest

import sh

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
SOURCE = f'{PROJECT_ROOT}/pyproxy'
SETUP_CFG = f'{PROJECT_ROOT}/setup.cfg'
TESTS = f'{PROJECT_ROOT}/tests'


# pylint: disable=no-self-use
class SyntaxTest(unittest.TestCase):
    """Test syntax compliance"""

    def test_pylint(self):
        """Test pylint compliance"""
        pylint = sh.Command('pylint')
        args = ['--rcfile', SETUP_CFG]
        args += glob.glob(f'{SOURCE}/**/*.py', recursive=True)
        args += glob.glob(f'{TESTS}/**/*.py', recursive=True)
        pylint(*args)

    def test_flake8(self):
        """Test flake8 compliance"""
        flake8 = sh.Command('flake8')
        flake8('--config', SETUP_CFG, SOURCE, TESTS)

    def test_isort(self):
        """Test isort compliance"""
        isort = sh.Command('isort')
        args = ['-c']
        args += glob.glob(f'{SOURCE}/**/*.py', recursive=True)
        args += glob.glob(f'{TESTS}/**/*.py', recursive=True)
        isort(*args)

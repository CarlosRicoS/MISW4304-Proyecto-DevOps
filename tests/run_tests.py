#!/usr/bin/env python3
"""
Simple test runner to avoid pytest version conflicts
"""
import sys
import os
import unittest

# Add the project root and src directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

if __name__ == "__main__":
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)  # Current directory (tests)
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with non-zero code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)

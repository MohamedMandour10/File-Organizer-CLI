import unittest
import os
import shutil
from unittest.mock import patch
from file_organizer import get_category, organize_files

class TestFileOrganizer(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and files for testing."""
        self.test_dir = "temp_test_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        # Create dummy files
        self.files_to_create = [
            "test_image.jpg",
            "test_document.pdf",
            "test_video.mp4",
            "unknown_file.xyz",
            "script.py"
        ]
        for filename in self.files_to_create:
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write("dummy content")

    def tearDown(self):
        """Remove the temporary directory and its contents after tests."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_get_category(self):
        """Test that get_category returns the correct category for various file types."""
        # Arrange
        test_cases = {
            "image.jpg": "Images",
            "document.pdf": "Documents",
            "video.mp4": "Videos",
            "archive.zip": "Archives",
            "code.py": "Code",
            "unknown.xyz": "Others"
        }

        for filename, expected_category in test_cases.items():
            with self.subTest(filename=filename):
                # Act
                category = get_category(filename)
                # Assert
                self.assertEqual(category, expected_category)

    @patch('file_organizer.logging')
    def test_organize_files_simulation_mode(self, mock_logging):
        """Test that simulation mode logs planned actions without moving files."""
        # Arrange
        initial_file_count = len(os.listdir(self.test_dir))

        # Act
        organize_files(self.test_dir, simulate=True)

        # Assert
        # Check that no files were moved
        self.assertEqual(len(os.listdir(self.test_dir)), initial_file_count)
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Images")))

        # Check that the correct log messages were generated
        self.assertIn("[SIMULATE] Move 'test_image.jpg' to 'Images/'", [call[0][0] for call in mock_logging.info.call_args_list])
        self.assertIn("[SIMULATE] Move 'test_document.pdf' to 'Documents/'", [call[0][0] for call in mock_logging.info.call_args_list])

    def test_organize_files_actual_move(self):
        """Test that files are correctly moved to their respective category folders."""
        # Act
        with patch('file_organizer.logging'): # Suppress logging output for this test
            organize_files(self.test_dir, simulate=False)

        # Assert
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Images", "test_image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "test_document.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Videos", "test_video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Code", "script.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Others", "unknown_file.xyz")))
        # Check that original files are gone
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "test_image.jpg")))

    @patch('shutil.move', side_effect=PermissionError("Permission Denied"))
    @patch('file_organizer.logging')
    def test_organize_files_permission_error(self, mock_logging, mock_move):
        """Test that permission errors are handled gracefully."""
        # Act
        organize_files(self.test_dir, simulate=False)

        # Assert
        # Ensure shutil.move was called
        self.assertTrue(mock_move.called)
        # Check that a warning was logged
        mock_logging.warning.assert_called()
        self.assertIn("Could not move", mock_logging.warning.call_args[0][0])

    @patch('file_organizer.logging')
    def test_organize_empty_directory(self, mock_logging):
        """Test that the script runs without errors on an empty directory."""
        # Arrange
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)

        # Act
        organize_files(empty_dir)

        # Assert
        # Check summary log for no files moved
        log_calls = [call[0][0] for call in mock_logging.info.call_args_list]
        self.assertIn("No files were found to organize.", "".join(log_calls))

if __name__ == '__main__':
    unittest.main()

import pytest
from pathlib import Path
import shutil
from src.project_management_software.core.archive_project import archive_project

@pytest.fixture
def temp_project_dir(tmp_path):
    """Fixture to create a temporary project directory."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / "test_file.txt").write_text("This is a test file.")
    yield project_dir
    if project_dir.exists():
        shutil.rmtree(project_dir)

@pytest.fixture
def temp_archive_dir(tmp_path):
    """Fixture to create a temporary archive directory."""
    archive_dir = tmp_path / "archive"
    archive_dir.mkdir()
    yield archive_dir
    if archive_dir.exists():
        shutil.rmtree(archive_dir)

def test_archive_project(temp_project_dir, temp_archive_dir):
    """Test the archive_project function."""
    archive_project(
        project_path=temp_project_dir,
        archive_path=temp_archive_dir
    )

    # Check if the zip file was created in the archive directory
    zip_file = temp_archive_dir / "test_project.zip"
    assert zip_file.exists()

    # Check if the project directory was deleted
    assert not temp_project_dir.exists()

    # Ensure no leftover data
    shutil.rmtree(temp_archive_dir)
    assert not temp_archive_dir.exists()

# External imports
import pytest
from pathlib import Path
import shutil
import os

# Internal imports
from src.project_management_software.core.create_project import create_project

@pytest.fixture
def temp_project_dir(tmp_path):
    """Fixture to create a temporary project directory."""
    project_dir = tmp_path / "test_project"
    yield project_dir
    if project_dir.exists():
        os.system('rmdir /S /Q "{}"'.format(str(project_dir)))

@pytest.fixture
def temp_template_dir(tmp_path):
    """Fixture to create a temporary template directory."""
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    (template_dir / "PROJECT_NAME_file.txt").write_text("This is a PROJECT_NAME content.")
    yield template_dir
    if template_dir.exists():
        os.system('rmdir /S /Q "{}"'.format(str(template_dir)))

def test_create_project(temp_project_dir, temp_template_dir):
    """Test the create_project function."""
    create_project(
        project_path=temp_project_dir,
        template_dirs=[temp_template_dir],
        use_git=False,
    )

    # Check if the project directory was created
    assert temp_project_dir.exists()

    # Check if the template files were copied
    replaced_file = temp_project_dir / "test_project_file.txt"
    assert replaced_file.exists()

    # Check if the content of the copied file is correct
    assert replaced_file.read_text() == "This is a test_project content."

def test_create_project_with_git(temp_project_dir, temp_template_dir):
    """Test the create_project function with git initialization."""
    create_project(
        project_path=temp_project_dir,
        template_dirs=[temp_template_dir],
        use_git=True,
    )

    # Check if the project directory was created
    assert temp_project_dir.exists()

    # Check if a .git directory was created
    git_dir = temp_project_dir / ".git"
    assert git_dir.exists() and git_dir.is_dir()
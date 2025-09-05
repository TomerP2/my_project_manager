from pathlib import Path
import shutil

def archive_project(project_path: Path, archive_path: Path):
    """
    Archives a project by zipping it, moving the zip file to the archive folder, and deleting the original folder.

    Args:
        project_path (Path): The path to the project folder to archive.
        archive_path (Path): The path to the archive folder where the zip file will be stored.
    """
    # Ensure the project path exists
    if not project_path.exists() or not project_path.is_dir():
        raise FileNotFoundError(f"The project path {project_path} does not exist or is not a directory.")

    # Ensure the archive path exists
    archive_path.mkdir(parents=True, exist_ok=True)

    # Step 1: Create zip file of the selected project folder
    zip_file_path = archive_path / f"{project_path.name}.zip"
    shutil.make_archive(str(zip_file_path.with_suffix('')), 'zip', str(project_path))

    # Step 2: Delete the original project folder
    shutil.rmtree(project_path)

    print(f"Project {project_path.name} has been archived to {zip_file_path}.")

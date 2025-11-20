import os
from pathlib import Path

# Give access to env variables
from dotenv import load_dotenv
load_dotenv()   # factorize env variables loading for all functions

def get_project_name():
    """
    Retrieves the project name from the 'PROJECT_NAME' environment variable.

    Returns:
        str: The value of the PROJECT_NAME environment variable.

    Raises:
        ValueError: If the PROJECT_NAME environment variable is not set or is empty.
    """
    project_name = os.getenv('PROJECT_NAME')
    if not project_name:
        raise ValueError("The 'PROJECT_NAME' environment variable is not set or is empty.")
    return project_name

def get_project_root_path(current_path: Path = None, markers=('docker-compose.yml', '.git')) -> Path:
    """
    Traverse up the directory tree until a folder containing one of the specified marker files is found,
    indicating the root of the project.

    Args:
        current_path (Path): The starting path for the search. Defaults to the script's directory.
        markers (tuple): Filenames or directory names that signify the project root.

    Returns:
        Path: The path to the project root directory.

    Raises:
        FileNotFoundError: If none of the marker files are found.
    """
    
    if current_path is None:
        current_path = Path(__file__).resolve().parent

    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in markers):
            return parent

    raise FileNotFoundError(f"Could not find project root starting from {current_path}")


def get_parent_path(dir_path) -> Path:
    """
    Returns the parent directory of the given path.

    Args:
        dir_path (str or Path): The path to a directory or file.

    Returns:
        Path: The parent directory path.
    """
    return Path(dir_path).resolve().parent


def get_dir_name(path_obj):
    """
    Returns the directory or the file name for the given path.

    Args:
        path_obj (Path): The path to a directory or file.

    Returns:
        str: The name of the directory.
    """
    return os.path.basename(str(path_obj).rstrip('/'))
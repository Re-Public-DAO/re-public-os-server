import os
import json
from importlib import util
from git import Repo
from git.exc import GitCommandError

from django.conf import settings


def get_connector_action(republic_id, function_name):
    # The base path where connectors directories are stored
    base_path = os.path.join(settings.BASE_DIR, 'republic_os/connectors/installed')

    # Building path to the directory based on `republic_id`
    connector_dir = os.path.join(base_path, republic_id)

    # Check if the directory exists
    if os.path.isdir(connector_dir):
        # Path to the functions.py file in the connector directory
        actions_file_path = os.path.join(connector_dir, 'actions.py')

        # Check if functions.py file exists in the directory
        if os.path.isfile(actions_file_path):
            # Dynamically import the module
            spec = util.spec_from_file_location("actions", actions_file_path)
            functions = util.module_from_spec(spec)
            spec.loader.exec_module(functions)

            # Check if the function exists in the module
            if hasattr(functions, function_name):
                # Call the function and return its value
                return getattr(functions, function_name)

    # Return a default value or None if the directory or function does not exist
    return None


def get_raw_data_directory(republic_id):
    directory = os.path.join(settings.BASE_DIR, '..', 're_public_os_raw_data', republic_id)
    return os.path.normpath(directory)


def commit_changes_to_git(republic_id, task_id):
    directory = get_raw_data_directory(republic_id)

    try:
        repo = Repo(directory)

        # Check if there are any uncommitted changes
        changed_files = [item.a_path for item in repo.index.diff(None)] + repo.untracked_files
        if not changed_files:
            print("No changes to commit.")
            return

        # Stage all changes
        repo.git.add(all=True)

        repo.index.commit(f'Updated from task {task_id}')

    except GitCommandError as e:
        print(f"Git command error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_dict_to_json_file(data_dict, republic_id, filename):
    """
    Write a dictionary to a JSON file.

    :param data_dict: Dictionary to be written to file.
    :param file_path: Path of the file where the JSON data will be saved.
    """
    directory = get_raw_data_directory(republic_id)
    file_path = os.path.join(directory, f'{filename}.json')

    # Check if the directory exists, create it if not
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print(f"An error occurred while creating the directory: {e}")
            return

    git_folder = os.path.join(directory, '.git')

    if not os.path.exists(git_folder):
        Repo.init(directory)

    try:
        with open(file_path, 'w') as file:
            json.dump(data_dict, file, indent=4)
        print(f"Data successfully written to {file_path}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
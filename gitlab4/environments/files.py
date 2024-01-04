import base64
import os
import re
from pathlib import Path
from typing import Callable, List, Dict, Any

from rich.pretty import pprint

from gitlab4.clients import GitlabClient
from gitlab4.helpers import load_environment_vars
from gitlab4.schemas import ProjectVariable


def encode(clear_text: str, encoding: str) -> str:
    encrypted_content = base64.b64encode(clear_text.encode(encoding)).decode(encoding)
    return encrypted_content


def decode(encrypted_text: str, encoding: str) -> str:
    clear_content = base64.b64decode(encrypted_text.encode(encoding)).decode(encoding)
    return clear_content


def save_project_var(variable: ProjectVariable, file_path: Path, encryption_function: Callable[[str, str], str] | None):
    if encryption_function is not None:
        content = encryption_function(variable.value, 'utf-8')
    else:
        content = variable.value

    if file_path.is_file():
        var_file = file_path
    else:
        var_file = file_path / f'{variable.key}.txt'
    with open(var_file, 'w') as f:
        f.write(content)
    return var_file


def parse_environment_file(file_path: Path) -> Dict[str, Any]:
    var_regexp_str = re.compile(r"^(?P<var_name>[A-Z0-9_]+)\s*=\s*(?P<var_value>.*)")
    var_regexp = re.compile(var_regexp_str)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    var_dict = {}
    for line in lines:
        line = line.strip('\n')
        match = var_regexp.match(line)
        if match:
            var_dict[match.group('var_name')] = match.group('var_value')
    return var_dict


def save_multiple_variables(folder: Path, environment_vars: List[str]):
    for env in environment_vars:
        var = client.get_variable(project_id=PROJECT_ID, variable_name=env.strip())

        var_file = save_project_var(variable=var[0], file_path=folder, encryption_function=decode)

        print(var_file)


def set_files_to_variables(folder: Path, pattern: str):
    txt_files = folder.glob(pattern)
    for txt_file in txt_files:
        print(txt_file.stem)
        push = input(f'Push {txt_file} to {project_info.name}: ')
        if push.lower() == 'y':
            with open(txt_file, 'r') as f:
                clear_value = f.read()
            encrypted_content = encode(clear_value, 'utf-8')
            project_var = ProjectVariable(key=txt_file.stem, value=encrypted_content)
            pprint(project_var)
            print('-' * 70)
            client.set_variable(project_id=PROJECT_ID, value=project_var)


if __name__ == '__main__':
    load_environment_vars()

    TOKEN = os.getenv('PRIVATE-TOKEN')
    PROJECT_ID = os.getenv('PROJECT_ID_2')
    # PROJECT_ID = os.getenv('PROJECT_ID_1')
    env_vars = os.getenv('GITLAB4_ENVIRONMENT_VARS').split(',')
    print(f'Token: {TOKEN}')

    client = GitlabClient(gitlab_token=TOKEN)

    project_info = client.get_project_info(project_id=PROJECT_ID)
    print(f'Project name: {project_info.name} id: {PROJECT_ID} path {project_info.path}')
    output_folder = Path(__file__).parent.parent.parent / 'output'
    print(output_folder, output_folder.exists())
    read_folder = output_folder / project_info.path
    # file_pattern ='*_STAGING.txt'
    # set_files_to_variables(folder=read_folder, pattern=file_pattern)

    # save_multiple_variables()
    staging_django_file = read_folder / 'ENVIRONMENT_DJANGO_STAGING.txt'
    staging_vars_dict = parse_environment_file(staging_django_file)
    pprint(staging_vars_dict)

    prod_django_file = read_folder / 'ENVIRONMENT_DJANGO_PRODUCTION.txt'
    prod_vars_dict = parse_environment_file(staging_django_file)
    pprint(prod_vars_dict)

    print(set(prod_vars_dict.keys()) == set(staging_vars_dict.keys()))

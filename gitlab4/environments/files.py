import base64
import os
from pathlib import Path
from typing import Callable, List

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


def save_multiple_variables(folder: Path, environment_vars:List[str]):
    for env in environment_vars:
        var = client.get_variable(project_id=PROJECT_ID, variable_name=env.strip())

        var_file = save_project_var(variable=var[0], file_path=folder, encryption_function=decode)

        print(var_file)


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
    txt_files = read_folder.glob('*_STAGING.txt')
    for txt_file in txt_files:
        print(txt_file.stem)
        with open(txt_file, 'r') as f:
            clear_value = f.read()
        encrypted_content = encode(clear_value, 'utf-8')
        project_var = ProjectVariable(key=txt_file.stem, value=encrypted_content)
        pprint(project_var)
        print('-'*70)
        client.create_variable(project_id=PROJECT_ID, value=project_var)

    # save_multiple_variables()

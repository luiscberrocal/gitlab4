from pprint import pprint
from typing import List

from gitlab4.schemas import ProjectVariable


def load_environment_vars():
    from dotenv import load_dotenv
    from pathlib import Path
    environment_folder = Path(__file__).parent.parent / '.envs'
    environment_file = environment_folder / 'environment_vars.txt'
    pprint(f'{environment_file} {environment_file.exists()}')
    load_dotenv(dotenv_path=environment_file)


def exclude_variables(variables: List[ProjectVariable], exclude: str = 'ENVIRONMENT') -> List[ProjectVariable]:
    clean_list = []
    c = 1
    i = 1
    for variable in variables:
        if exclude in variable.key:
            print(f'Excluded {c}. {variable.key}')
            c += 1
        else:
            #  print(f'Added {i}. {variable.key}')
            i += 1
            clean_list.append(variable)
    return clean_list

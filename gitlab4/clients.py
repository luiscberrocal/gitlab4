import os
from pprint import pprint
from typing import List, Dict

import requests


class GitlabClient:
    def __init__(self, gitlab_token: str):
        self.headers = {'PRIVATE-TOKEN': gitlab_token}
        self.host = 'https://gitlab.com'

    def get_ci_project_variables(self, project_id: str, variables: List[str]) -> Dict[str, str]:
        base_url = f"{self.host}/api/v4/projects/{project_id}/variables"
        variable_data = dict()
        for variable in variables:
            variable_url = f'{base_url}/{variable}'
            response = requests.get(variable_url, headers=self.headers)
            variable_data[variable] = response.json()
        return variable_data


    def list_variables(self, project_id: int | str):
        """https://docs.gitlab.com/ee/api/project_level_variables.html
        GET /projects/:id/variables
        """
        url = f"{self.host}/api/v4/projects/{project_id}/variables"
        print(f'Url: {url}')
        url = "https://gitlab.com/api/v4/projects/42957523/variables"
        print(f'headers: {self.headers}')
        # headers = {'PRIVATE-TOKEN': 'glpat-jsfwgbTy_jU8_9hMns1K'}
        # assert headers == self.headers
        response = requests.get(url=url, headers=self.headers)
        var_data = response.json()
        return var_data


def load_environment_vars():
    from dotenv import load_dotenv
    from pathlib import Path
    environment_folder = Path(__file__).parent.parent / '.envs'
    environment_file = environment_folder / 'environment_vars.txt'
    pprint(f'{environment_file} {environment_file.exists()}')
    load_dotenv(dotenv_path=environment_file)


if __name__ == '__main__':
    load_environment_vars()

    TOKEN = os.getenv('PRIVATE-TOKEN')
    PROJECT_ID_1 = os.getenv('PROJECT_ID_1')

    print(f'Token: {TOKEN}')
    print(f'Project id: {PROJECT_ID_1}')

    client = GitlabClient(gitlab_token=TOKEN)
    response_data = client.list_variables(project_id=PROJECT_ID_1)

    c = 1
    i = 1
    for variable in response_data:
        if 'ENVIRONMENT' in variable['key']:
            print(f'-- {c}. {variable["key"]}')
            c += 1
        else:
            print(f'{i}. {variable["key"]}')
            i += 1




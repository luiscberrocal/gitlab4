import os
from pprint import pprint
from typing import List, Dict

import requests

from gitlab4.schemas import ProjectVariable, Project


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

    def list_variables(self, project_id: int | str) -> List[ProjectVariable]:
        """https://docs.gitlab.com/ee/api/project_level_variables.html
        GET /projects/:id/variables
        """
        url = f"{self.host}/api/v4/projects/{project_id}/variables"
        response = requests.get(url=url, headers=self.headers)
        var_data = response.json()
        var_list = []
        if response.status_code == 200:
            for var in var_data:
                var_list.append(ProjectVariable(**var))
        return var_list

    def set_variable(self, project_id: int | str, value: ProjectVariable):
        """https://docs.gitlab.com/ee/api/project_level_variables.html#update-a-variable
        TODO Change the return for Pydantic model.
        """
        url = f"{self.host}/api/v4/projects/{project_id}/variables/{value.key}"
        payload = value.model_dump()
        response = requests.put(url, data=payload, headers=self.headers)
        print(f'>>>> {response.status_code}')
        response_data = response.json()
        return response_data

    def create_variable(self, project_id: int | str, value: ProjectVariable) -> ProjectVariable | None:
        """https://docs.gitlab.com/ee/api/project_level_variables.html#create-a-variable
        """
        url = f"{self.host}/api/v4/projects/{project_id}/variables"
        payload = value.model_dump()
        response = requests.post(url, data=payload, headers=self.headers)
        print(f'>>>> {response.status_code}')
        if response.status_code == 201:
            response_data = response.json()
            project_var = ProjectVariable(**response_data)
            return project_var
        else:
            return None

    def get_project_info(self, project_id: str) -> Project | None:
        base_url = f"{self.host}/api/v4/projects/{project_id}"
        response = requests.get(base_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return Project(**data)
        else:
            return None


def load_environment_vars():
    from dotenv import load_dotenv
    from pathlib import Path
    environment_folder = Path(__file__).parent.parent / '.envs'
    environment_file = environment_folder / 'environment_vars.txt'
    pprint(f'{environment_file} {environment_file.exists()}')
    load_dotenv(dotenv_path=environment_file)


def exclude_variables(variables: List[ProjectVariable], value: str = 'ENVIRONMENT') -> List[ProjectVariable]:
    clean_list = []
    c = 1
    i = 1
    for variable in variables:
        if value in variable.key:
            print(f'Excluded {c}. {variable.key}')
            c += 1
        else:
            #  print(f'Added {i}. {variable.key}')
            i += 1
            clean_list.append(variable)
    return clean_list


if __name__ == '__main__':
    load_environment_vars()

    TOKEN = os.getenv('PRIVATE-TOKEN')
    PROJECT_ID_1 = os.getenv('PROJECT_ID_1')
    PROJECT_ID_2 = os.getenv('PROJECT_ID_2')

    print(f'Token: {TOKEN}')

    client = GitlabClient(gitlab_token=TOKEN)
    project_info = client.get_project_info(project_id=PROJECT_ID_1)
    print(f'Project name: {project_info.name} id: {PROJECT_ID_1} ')

    project_info = client.get_project_info(project_id=PROJECT_ID_2)
    print(f'Project name: {project_info.name} id: {PROJECT_ID_2} ')

    project_variables = client.list_variables(project_id=PROJECT_ID_1)

    clean_vars = exclude_variables(variables=project_variables)

    for var in clean_vars:
        pprint(f'Pushing {var.key}')
        new_var = client.create_variable(project_id=PROJECT_ID_2, value=var)
        print(f'Pushed {new_var.key}')

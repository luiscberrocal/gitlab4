import os
from pprint import pprint
from typing import List

import requests

from gitlab4.helpers import load_environment_vars, exclude_variables
from gitlab4.schemas import ProjectVariable, Project


class GitlabClient:
    def __init__(self, gitlab_token: str):
        self.headers = {'PRIVATE-TOKEN': gitlab_token}
        self.host = 'https://gitlab.com'

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

    def get_variable(self, project_id: int | str, variable_name: str) -> List[ProjectVariable]:
        """https://docs.gitlab.com/ee/api/project_level_variables.html
        GET /projects/:id/variables
        """
        url = f"{self.host}/api/v4/projects/{project_id}/variables/{variable_name}"
        response = requests.get(url=url, headers=self.headers)
        var_data = response.json()
        var_list = []
        if response.status_code == 200:
            if isinstance(var_data, list):
                for var in var_data:
                    var_list.append(ProjectVariable(**var))
            else:
                var_list.append(ProjectVariable(**var_data))
        return var_list

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


def copy_environment_files(source_project_id: str, target_project_id: str, exclude='ENVIRONMENT'):
    project_variables = client.list_variables(project_id=source_project_id)

    clean_vars = exclude_variables(variables=project_variables, exclude=exclude)

    for var in clean_vars:
        pprint(f'Pushing {var.key}')
        new_var = client.create_variable(project_id=target_project_id, value=var)
        print(f'Pushed {new_var.key}')


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

import logging
import os

import requests

from .page import Page
from .project import Project
from .wiki import Wiki

logger = logging.getLogger(__name__)


class AzureDevOps:

    def __init__(self, organization, pat):
        self.organization = organization
        self._pat = pat
        self._auth = ("", self._pat)

    def get_projects(self, project_name=None):
        # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/projects/list?view=azure-devops-rest-6.0
        url = f"https://dev.azure.com/{self.organization}/_apis/projects?api-version=6.0"
        logger.info(url)
        # https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page
        response = requests.get(url, auth=self._auth)
        response.raise_for_status()
        projects = []
        for item in response.json()["value"]:
            _id = item["id"]
            name = item["name"]
            if name.strip().upper() == (project_name if project_name is not None else name).strip().upper():
                projects.append(Project(_id, name))

        for project in projects:
            project.wikis = self._get_wikis(project.id)
            for wiki in project.wikis:
                wiki.pages = self._get_pages(project.id, wiki.id)

        return projects

    def _get_wikis(self, project_id):
        # https://docs.microsoft.com/en-us/rest/api/azure/devops/wiki/wikis/list?view=azure-devops-rest-6.0
        url = f"https://dev.azure.com/{self.organization}/{project_id}/_apis/wiki/wikis?api-version=6.0"
        logger.info(url)
        response = requests.get(url, auth=self._auth)
        response.raise_for_status()
        return list(map(lambda item: Wiki(item["id"], item["name"]),
                        filter(lambda item: item["type"] == "projectWiki", response.json()["value"])))

    def _get_pages(self, project_id, wiki_id, continuation_token=None):
        # https://docs.microsoft.com/en-us/rest/api/azure/devops/wiki/pages%20batch/get?view=azure-devops-rest-6.1
        url = f"https://dev.azure.com/{self.organization}/{project_id}/_apis/wiki/wikis/{wiki_id}/pagesbatch" \
              f"?api-version=6.1-preview.1"
        logger.info(url)
        json = {"top": 10}
        if continuation_token is not None:
            json["continuationToken"] = continuation_token
        response = requests.post(url, auth=self._auth, json=json)
        response.raise_for_status()

        def create_page(item):
            page_id = item["id"]
            order, is_parent, content = self._get_page_details(project_id, wiki_id, page_id)
            return Page(page_id, item["path"], order, is_parent, content)

        pages = list(map(lambda item: create_page(item), response.json()["value"]))
        continuation_token = response.headers.get("x-ms-continuationtoken")
        if continuation_token is not None:
            pages.extend(self._get_pages(project_id, wiki_id, continuation_token))
        return pages

    def _get_page_details(self, project_id, wiki_id, page_id):
        # https://docs.microsoft.com/en-us/rest/api/azure/devops/wiki/pages/get%20page%20by%20id?view=azure-devops-rest-6.1
        url = f"https://dev.azure.com/{self.organization}/{project_id}/_apis/wiki/wikis/{wiki_id}/pages/{page_id}" \
              f"?api-version=6.1-preview.1"
        logger.info(url)
        params = {"includeContent": True, "recursionLevel": "none"}
        response = requests.get(url, auth=self._auth, params=params)
        response.raise_for_status()
        json_data = response.json()
        return int(json_data["order"]), json_data.get("isParentPage", False), json_data["content"]

    def download_attachment(self, project_id, wiki_id, attachment, directory):
        url = f"https://dev.azure.com/{self.organization}/{project_id}/_apis/git/repositories/{wiki_id}/Items" \
              f"?path={attachment}"
        logger.info(url)
        with requests.get(url, auth=self._auth, stream=True) as r:
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.error(f"Exception occurred downloading {url}", exc_info=True)
                if e.response.status_code != requests.codes.not_found:
                    raise
                return
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, attachment.split("/")[-1])
            with open(file_path, "wb") as f:
                for chunk in r.iter_content():
                    f.write(chunk)

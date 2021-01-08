from datetime import timedelta
import logging
from timeit import default_timer as timer
import os
import sys

import jsonpickle

from azure_devops import AzureDevOps
from hugo import Hugo
import debug


def main(project_name=None):
    organization = os.environ["ORGANIZATION"]
    pat = os.environ["PAT"]
    azure_devops = AzureDevOps(organization, pat)

    projects = azure_devops.get_projects(project_name)

    if debug.is_debug_active():
        json_data = jsonpickle.encode(projects)
        with open("data.json", mode="w", encoding="utf-8") as f:
            f.write(json_data)

    # with open("data.json", mode="r") as f:
    #     json_data = f.read()
    #     projects = jsonpickle.decode(json_data)

    hugo = Hugo(azure_devops)
    site_directory = sys.argv[1]
    hugo.create_content(projects, site_directory)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start = timer()
    main()
    end = timer()
    logging.info(timedelta(seconds=end - start))

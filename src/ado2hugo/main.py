from datetime import timedelta
import logging
from timeit import default_timer as timer
import os
import sys

import jsonpickle

from .azure_devops import AzureDevOps
from .hugo import Hugo
from .utilities import is_debug_active, get_environment_variable


def main():
    logging.basicConfig(level=logging.INFO)
    start = timer()

    site_directory = sys.argv[1]
    if not os.path.exists(site_directory):
        logging.error(f"{site_directory} does not exist.")
        return

    project_name = None
    if len(sys.argv) == 3:
        project_name = sys.argv[2]

    organization = get_environment_variable("ORGANIZATION")
    if organization is None:
        logging.error("ORGANIZATION environment variable not found.")
        return

    pat = get_environment_variable("PAT")
    if pat is None:
        logging.error("PAT environment variable not found.")
        return

    azure_devops = AzureDevOps(organization, pat)

    projects = azure_devops.get_projects(project_name)

    if is_debug_active():
        json_data = jsonpickle.encode(projects)
        with open("data.json", mode="w", encoding="utf-8") as f:
            f.write(json_data)

    # with open("data.json", mode="r") as f:
    #     json_data = f.read()
    #     projects = jsonpickle.decode(json_data)

    hugo = Hugo(azure_devops)
    hugo.create_content(projects, site_directory)

    end = timer()
    logging.info(timedelta(seconds=end - start))


if __name__ == '__main__':
    main()

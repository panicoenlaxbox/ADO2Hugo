import logging
import os
import sys
from argparse import ArgumentParser

# https://mypy.readthedocs.io/en/latest/running_mypy.html#missing-imports
import jsonpickle  # type: ignore

from .azure_devops import AzureDevOps
from .hugo import Hugo
from .utilities import is_debug_active, get_environment_variable, timer

logging.basicConfig(level=logging.INFO)


@timer
def main():
    parser = ArgumentParser()
    parser.add_argument("--organization", help="Organization")
    parser.add_argument("--pat", help="Personal access token")
    parser.add_argument("--project", help="Project name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
    parser.add_argument("site_dir", help="Site directory")

    args = parser.parse_args()

    if args.verbose:
        logging.info(f"__name__: {__name__}, __package__: {__package__}, __file__: {__file__}")
        logging.info("\n".join(sys.path))

    site_dir: str = args.site_dir
    if not os.path.exists(site_dir):
        logging.error(f"{site_dir} does not exist.")
        return

    project_name: str = args.project

    organization = args.organization or get_environment_variable("ORGANIZATION")
    if organization is None:
        logging.error("ORGANIZATION not valid.")
        return

    pat = args.pat or get_environment_variable("PAT")
    if pat is None:
        logging.error("PAT not valid.")
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
    hugo.create_content(projects, site_dir)


if __name__ == '__main__':
    main()

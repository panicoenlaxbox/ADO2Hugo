import logging
import os
import sys
from argparse import ArgumentParser

# https://mypy.readthedocs.io/en/latest/running_mypy.html#missing-imports
import jsonpickle  # type: ignore

from ._utils import get_environment_variable, is_debug_active, timer
from .azure_devops import AzureDevOps
from .hugo import Hugo


@timer
def main():
    parser = ArgumentParser(prog="ado2hugo")
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

    if not os.path.exists(os.path.join(site_dir, "content")):
        logging.error(f"{site_dir} does not look a Hugo site.")
        return

    project_name: str = args.project

    organization = args.organization or get_environment_variable("ORGANIZATION")
    if organization is None:
        logging.error("ORGANIZATION is not valid.")
        return

    pat = args.pat or get_environment_variable("PAT")
    if pat is None:
        logging.error("PAT is not valid.")
        return

    azure_devops = AzureDevOps(organization, pat)

    projects = azure_devops.get_projects(project_name)

    if is_debug_active():
        json_data = jsonpickle.encode(projects)
        with open("projects.json", mode="wt", encoding="utf-8") as f:
            f.write(json_data)

    # with open("projects.json", mode="r") as f:
    #     json_data = f.read()
    #     projects = jsonpickle.decode(json_data)

    hugo = Hugo(azure_devops)
    hugo.create_content(projects, site_dir)


if __name__ == "__main__":  # with ado2hugo command line, __name__ will be 'ado2hugo.__main__'
    main()

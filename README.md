![Upload Python Package](https://github.com/panicoenlaxbox/ADO2Hugo/workflows/Upload%20Python%20Package/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# ADO2Hugo

With this program you will be able to export [Azure DevOps](https://azure.microsoft.com/es-es/services/devops/) wikis to [Hugo](https://gohugo.io/)

Azure DevOps offers two kinds of wiki: Project (managed by the platform) or "Wiki as code" (publish directly markdown files from a branch in your repository).

Currently, only wiki projects are supported, and it does not have sense to support the "wiki as code" option.

The program uses the Azure DevOps API to iterate over an organization's projects and, in accordance with Hugo's folder structure, exports all wiki pages with their corresponding attachments.

I have used [Geekdoc theme](https://themes.gohugo.io/hugo-geekdoc/).

## Installation

```pip install ado2hugo```

## Usage

```bash
ado2hugo -h
usage: ado2hugo [-h] [--organization ORGANIZATION] [--pat PAT] [--project PROJECT] [-v] site_dir

positional arguments:
  site_dir              Site directory

optional arguments:
  -h, --help            show this help message and exit
  --organization ORGANIZATION
                        Organization
  --pat PAT             Personal access token
  --project PROJECT     Project name
  -v, --verbose         Verbose
```

`ORGANIZATION` and `PAT` options, can be also an environment variable.

```bash
ado2hugo --organization <YOUR_ORGANIZATION> --pat <YOUR_PAT> <YOUR_SITE_DIRECTORY>
```

> Be carefully because this program deletes before its execution, all files in the /static and /content folders of supplied path

## Development

You must run the following commands to develop localy:
- Create a pipenv local environment with `pipenv install --dev` 
- Install pre-commit hooks with `pre-commit install`

For executing `__main__.py`, you must use `python -m src.ado2hugo`, so relative imports will work, if you use `python __main__.py` you will receive the error `ImportError: attempted relative import with no known parent package`, 
more information in https://napuzba.com/a/import-error-relative-no-parent

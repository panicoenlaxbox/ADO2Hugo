# ADO2Hugo

With this program you will be able to export [Azure DevOps](https://azure.microsoft.com/es-es/services/devops/) wikis to [Hugo](https://gohugo.io/)

Azure DevOps offers two kinds of wiki: Project (managed by the platform) or "Wiki as code" (publish directly markdown files from a branch in your repository).

Currently, only wiki projects are supported, and it does not have sense to support the "wiki as code" option.

The program uses the Azure DevOps API to iterate over an organization's projects and, in accordance with Hugo's folder structure, exports all wiki pages with their corresponding attachments.

I have used [Geekdoc theme](https://themes.gohugo.io/hugo-geekdoc/).

You will have to supply, both, an organization name and a PAT (Personal Access Token) like environment variables.

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

## Development

You must run the following commands to develop localy:
- Create a pipenv local environment
- `pre-commit install`

For executing `__main__.py`, you must use `python -m src.ado2hugo`, so relative imports will work, if you use `python __main__.py` you will recieve the error `ImportError: attempted relative import with no known parent package`, 
more information in https://napuzba.com/a/import-error-relative-no-parent
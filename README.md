# ADO2Hugo

With this program you will be able to export [Azure DevOps](https://azure.microsoft.com/es-es/services/devops/) wikis to [Hugo](https://gohugo.io/)

Azure DevOps offers two kinds of wiki: Project (managed by the platform) or "Wiki as code" (publish directly markdown files from a branch in your repository).

Currently, only wiki projects are supported, and it does not have sense to support the "wiki as code" option.

The program uses the Azure DevOps API to iterate over an organization's projects and, in accordance with Hugo's folder structure, exports all wiki pages with their corresponding attachments.

I have used [Geekdoc theme](https://themes.gohugo.io/hugo-geekdoc/).

You will have to supply, both, an organization name and a PAT (Personal Access Token) like environment variables.

## Install

```pip install ado2hugo```

## Usage

```
set ORGANIZATION=<YOUR_ORGANIZATION>
set PATH=<YOUR_PATH>
ado2hugo C:\Hugo\Sites\example.com\content
```
import logging
import os
import re
import shutil
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class Hugo:

    def __init__(self, azure_devops):
        self._azure_devops = azure_devops

    def create_content(self, projects, site_directory):
        content_directory = os.path.join(site_directory, "content")
        self.__class__._empty_directory(content_directory)

        static_directory = os.path.join(site_directory, "static")
        self.__class__._empty_directory(static_directory)

        for project in projects:
            project_directory = os.path.join(content_directory, self.__class__._sanitize_path(project.name))

            for wiki in project.wikis:
                wiki_directory = os.path.join(project_directory, self.__class__._sanitize_path(wiki.name))

                for page in wiki.pages:
                    if not page.content:
                        continue

                    page_directories = list(map(
                        lambda item: self.__class__._sanitize_path(item), page.path.split("/")
                    ))

                    if page.is_parent:
                        page_directory = os.path.join(wiki_directory, *page_directories)
                        file_path = os.path.join(page_directory, "_index.md")
                    else:
                        page_directory = os.path.join(wiki_directory, *page_directories[:-1])
                        file_path = os.path.join(page_directory, f"{page_directories[-1]}.md")

                    self._extract_attachments(project.id, wiki.id, page.content, static_directory)
                    content = self.__class__._update_attachments(page.content, "/")

                    content = self.__class__._get_front_matter(page.title, page.is_parent) + content

                    self.__class__._create_file(file_path, content)

        self.__class__._create_index_page(content_directory, self._azure_devops.organization)
        for root, dirs, files in os.walk(content_directory):
            for _dir in dirs:
                self.__class__._create_index_page(os.path.join(root, _dir))

    @staticmethod
    def _get_front_matter(title, collapse=False):
        title = title.replace('"', '\\"')
        front_matter = f"""---
title: "{title}"
date: {datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")}
draft: true
"""
        if collapse:
            front_matter += "geekdocCollapseSection: true\n"
        front_matter += "---" + ("\n" * 2)
        return front_matter

    @classmethod
    def _create_index_page(cls, directory, title=None):
        index_path = os.path.join(directory, "_index.md")
        if os.path.exists(index_path):
            return
        logger.info(f"Creating {index_path}")
        with open(index_path, "x", encoding="utf-8") as f:
            title = title if title else os.path.basename(directory)
            content = cls._get_front_matter(title, True) + "{{< toc-tree >}}"
            f.write(content)

    @staticmethod
    def _empty_directory(directory):
        logger.info(f"Emptying {directory}")
        if not os.path.exists(directory):
            return
        for _dir in os.listdir(directory):
            path = os.path.join(directory, _dir)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)

    @staticmethod
    def _create_file(file_path, content):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        logger.info(f"Creating {file_path}")
        with open(file_path, mode="x", encoding="utf-8") as f:
            f.write(content)

    def _extract_attachments(self, project_id, wiki_id, content, directory):
        pattern = r"\(\/?\.attachments\/.+?\)"
        for attachment in re.findall(pattern, content, re.MULTILINE):
            attachment = attachment[1:-1]
            if attachment.startswith("/"):
                attachment = attachment[1:]
            self._azure_devops.download_attachment(project_id, wiki_id, attachment, directory)

    @staticmethod
    def _update_attachments(content, location):
        pattern = r"\/?\.attachments\/"
        return re.sub(pattern, location, content)

    @staticmethod
    def _sanitize_path(path):
        # https://docs.microsoft.com/es-es/windows/win32/fileio/naming-a-file
        pattern = r'[<>:"/\\|?*]'
        return re.sub(pattern, "__", path)

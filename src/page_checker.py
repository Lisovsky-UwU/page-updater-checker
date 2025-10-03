import difflib
import os
import re

import requests
from bs4 import BeautifulSoup


class PageUpdaterChecker:

    def __init__(self, page_save_path: str, page_url: str, timeout: int) -> None:
        self._page_save_path = page_save_path
        self._page_url = page_url
        self._timeout = timeout
        if os.path.exists(self._page_save_path):
            with open(page_save_path, mode="r") as file:
                self._current_page_text = file.read()
        else:
            self._current_page_text = self._parse_page()
            with open(self._page_save_path, mode="w") as file:
                file.write(self._current_page_text)

    @property
    def page_url(self) -> str:
        return self._page_url

    def _parse_page(self) -> str:
        """
        Парсит страницу и возвращает ее содержимое.
        """
        html_text = requests.get(self._page_url, timeout=self._timeout).text
        soup = BeautifulSoup(html_text, "html.parser")
        text = soup.get_text()
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"(?m)^[ \t]*\r?\n", "", text)
        return "\n".join(line.strip() for line in text.splitlines())

    def _set_new_page_text(self, new_text: str) -> None:
        with open(self._page_save_path, mode="w") as file:
            file.write(new_text)
        self._current_page_text = new_text

    def check_update(self) -> str | None:
        new_page_text = self._parse_page()
        if new_page_text != self._current_page_text:
            diffenert_text = ""
            for line in difflib.unified_diff(
                self._current_page_text.splitlines(keepends=True),
                new_page_text.splitlines(keepends=True),
                fromfile="Предыдущая страница",
                tofile="Новая страница",
            ):
                diffenert_text += f"{line}"

            self._set_new_page_text(new_page_text)
            return diffenert_text

        return None


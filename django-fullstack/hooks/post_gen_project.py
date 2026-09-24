#!/usr/bin/env python
"""Clean up conditional files and finish the generated project."""
import shutil
from datetime import date
from pathlib import Path

PROJECT = Path.cwd()

USE_AUTH = "{{ cookiecutter.use_authentication }}"
USE_DOCKER = "{{ cookiecutter.use_docker }}"
USE_TAILWIND = "{{ cookiecutter.use_tailwind }}"
USE_HTMX = "{{ cookiecutter.use_htmx }}"
USE_TESTS = "{{ cookiecutter.use_tests }}"
DEP_MANAGER = "{{ cookiecutter.dependency_manager }}"
LICENSE = "{{ cookiecutter.license }}"
AUTHOR = "{{ cookiecutter.author_name }}"
PROJECT_NAME = "{{ cookiecutter.project_name }}"


def remove(path):
    target = PROJECT / path
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()


def remove_block(path, start, end):
    target = PROJECT / path
    if not target.exists():
        return
    content = target.read_text()
    if start in content and end in content:
        target.write_text(content.split(start)[0] + content.split(end, 1)[1])


def handle_docker():
    if USE_DOCKER == "no":
        for path in (
            "Dockerfile",
            "docker-compose.yml",
            ".dockerignore",
            "scripts/entrypoint.sh",
        ):
            remove(path)


def handle_tailwind():
    if USE_TAILWIND == "no":
        for path in ("package.json", "tailwind.config.js", "static/src"):
            remove(path)


def handle_htmx():
    if USE_HTMX == "no":
        remove("static/js/htmx.min.js")
        remove_block("core/templates/base.html", "<!-- htmx:start -->", "<!-- htmx:end -->")


def handle_authentication():
    if USE_AUTH == "no":
        remove("apps/accounts")
        remove_block("core/templates/base.html", "<!-- auth:start -->", "<!-- auth:end -->")


def handle_tests():
    if USE_TESTS == "no":
        remove("pytest.ini")
        remove("apps/accounts/tests")


def handle_dependency_manager():
    if DEP_MANAGER == "poetry":
        remove("requirements.txt")
        remove("requirements-dev.txt")


def write_license():
    if LICENSE == "Proprietary":
        return
    year = date.today().year
    if LICENSE == "MIT":
        text = f"""MIT License

Copyright (c) {year} {AUTHOR}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    elif LICENSE == "BSD-3-Clause":
        text = f"""BSD 3-Clause License

Copyright (c) {year}, {AUTHOR}
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED.
"""
    else:
        text = (
            "This project is licensed under the GNU General Public License v3.0.\n"
            "See https://www.gnu.org/licenses/gpl-3.0.txt for the full text.\n"
        )
    (PROJECT / "LICENSE").write_text(text)


def main():
    handle_docker()
    handle_tailwind()
    handle_htmx()
    handle_authentication()
    handle_tests()
    handle_dependency_manager()
    write_license()

    print(
        f"""
Setup completo! Projeto '{PROJECT_NAME}' gerado.

Próximos passos:
  1. cd {PROJECT.name}
  2. cp .env.example .env  (e ajuste DJANGO_SECRET_KEY)
"""
        + (
            "  3. make install && make migrate\n"
            if DEP_MANAGER == "pip"
            else "  3. poetry install && make migrate\n"
        )
        + (
            "  4. make tailwind   # compila o CSS\n"
            if USE_TAILWIND == "yes"
            else ""
        )
        + "  5. make run\n"
        + "\nHappy Coding! :)\n"
    )


if __name__ == "__main__":
    main()

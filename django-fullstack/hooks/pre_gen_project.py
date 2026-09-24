#!/usr/bin/env python
"""Validate user answers before generating the project."""
import re
import sys

slug = "{{ cookiecutter.project_slug }}"

if not re.fullmatch(r"[a-z][a-z0-9_]*", slug):
    print(
        f"ERROR: invalid project_slug '{slug}'. "
        "Use lowercase letters, digits and underscore, starting with a letter."
    )
    sys.exit(1)

if "{{ cookiecutter.use_htmx }}" == "yes" and "{{ cookiecutter.use_tailwind }}" == "no":
    print(
        "WARNING: use_htmx=yes but use_tailwind=no. "
        "HTMX will be included; Tailwind will not."
    )

#!/usr/bin/env python3
"""
Init script to rename project.
"""

import os
import re
import subprocess


def read(prompt, regex, default):
    """
    Read a string from command line.

    The string has to match the given regular expression.
    """
    if default:
        prompt += f" [{default}]"
    prompt += ": "

    while True:
        ret = input(prompt)
        if not ret and default:
            ret = default
        match = re.match(regex, ret)
        if match is not None:
            return ret
        print(f"the project name has to match the regular expression: {regex}")


def git_config_get(attr):
    """
    Get a git config value.
    """
    try:
        return subprocess.check_output(["git", "config", "--get", attr]).decode().strip()
    except subprocess.CalledProcessError:
        return None


def main():
    """
    Rename the project.
    """

    author = git_config_get("user.name")
    email = git_config_get("user.email")
    origin = git_config_get("remote.origin.url")
    url, project = None, None

    if origin is not None:
        match = re.match(r"^.*[:/]([^:/]*)/([^/]*)(\.git)?$", origin)
        if match is not None:
            org, project = match.group(1), match.group(2)
            url = f"https://github.com/{org}/{project}/"
            project = project.replace("-", "_")

    project = read("project name", r"^[a-z][a-z0-9_]*$", project)
    author = read("author", r".+", author)
    email = read("email", r".+", email)
    url = read("url", r".+", url)

    replacements = {
        "author@fillname.org": email,
        "Author Fillname": author,
        "https://fillname.org/": url,
        "fillname": project,
    }

    def replace(filepath):
        with open(filepath, "r", encoding="utf-8") as hnd:
            content = hnd.read()
            for key, val in replacements.items():
                content = content.replace(key, val)
        with open(filepath, "w", encoding="utf-8") as hnd:
            hnd.write(content)

    dirs = [os.path.join("src", "fillname"), "tests", "docs"]
    files = [
        ".pre-commit-config.yaml",
        "mkdocs.yml",
        "noxfile.py",
        "pyproject.toml",
        "CHANGES.md",
        "CONTRIBUTING.md",
        "DEPLOYMENT.md",
        "DEVELOPMENT.md",
        "LICENSE",
        "README.md",
    ]

    for rootpath in dirs:
        for dirpath, _, filenames in os.walk(rootpath):
            for filename in filenames:
                if not filename.endswith(".py") and not filename.endswith(".md"):
                    continue
                filepath = os.path.join(dirpath, filename)
                replace(filepath)

    for filepath in files:
        replace(filepath)

    os.rename(os.path.join("src", "fillname"), os.path.join("src", project))


if __name__ == "__main__":
    main()

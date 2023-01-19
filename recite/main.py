import os
import subprocess
import sys
from typing import Callable

import toml
import typer
from rich import print as rprint

app = typer.Typer()


def check_on_main():
    """Make sure you're on main/master branch."""
    res = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True
    )
    current_branch = res.stdout.decode().strip()
    return current_branch == "main" or current_branch == "master"


def check_clean_git():
    """Make sure git is clean."""
    return subprocess.check_output(["git", "status", "--porcelain"]).decode() == ""


def run_tests():
    """Run test-suite."""
    return subprocess.run(["nox", "-r"]).returncode == 0


def check_changelog():
    """Make sure changelog was updated."""
    paths = [
        "CHANGELOG",
        "CHANGELOG.md",
        "CHANGELOG.rst",
    ]
    cl_path = None
    for p in paths:
        if os.path.isfile(p):
            cl_path = p
            break
    if cl_path is None:
        raise RuntimeError(f"Could not find Changelog in paths {paths}")
    current_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
    if current_version == "0.1.0":
        if os.path.getsize(cl_path) > 0:
            # there is a changelog file and it contains something
            return True
        else:
            raise RuntimeError(f"Changelog file '{cl_path}' empty")
    # check if there is a diff
    res = subprocess.check_output(
        ["git", "diff", current_version, "--", cl_path], capture_output=True
    )
    return len(res.stdout.decode()) > 0


def run_steps(steps: Callable):
    message_prefix = "recite > "
    rprint(
        f"{message_prefix} Checking everything to make sure you are ready to release"
    )
    for number, step in enumerate(steps, start=1):
        success = step()
        message = step.__doc__[:-1]  # remove dot
        if success:
            rprint(
                f"{message_prefix}[green]✓ [/green]{number}: [green]{message}: success[/green]"
            )
        else:
            rprint(
                f"{message_prefix}[red]✘ [/red]{number}: [red]{message}: failed[/red]"
            )
            sys.exit(1)


@app.command()
def main():
    run_steps([check_on_main, check_clean_git, run_tests, check_changelog])


if __name__ == "__main__":
    app()

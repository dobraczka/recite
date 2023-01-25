import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Optional

import toml
from git import Repo


@dataclass
class Result:
    success: bool
    messages: Optional[Iterable[str]] = None


@dataclass
class StepMixin:
    project_dir: str
    short_name: str
    description: str


class Step(ABC, StepMixin):
    @abstractmethod
    def run(self) -> Result:
        raise NotImplementedError


class GitStep(Step):
    def __post_init__(self):
        self.repo = Repo(self.project_dir)


@dataclass
class CheckPyProjectStep(Step):
    short_name: str = "check_pyproject_toml"
    description: str = "Make sure you have a (non-empty) pyproject.toml"

    def run(self) -> Result:
        success = (
            os.path.isfile("pyproject.toml") and os.path.getsize("pyproject.toml") > 0
        )
        return Result(success=success)


@dataclass
class CheckOnMainStep(GitStep):
    short_name: str = "check_on_main"
    description: str = "Make sure you're on main/master branch"

    def run(self) -> Result:
        current_branch = self.repo.active_branch.name
        success = current_branch == "main" or current_branch == "master"
        return Result(success=success)


@dataclass
class CheckCleanGitStep(GitStep):
    short_name: str = "check_clean_git"
    description: str = "Make sure git is clean"

    def run(self) -> Result:
        if self.repo.is_dirty():
            return Result(success=False, messages=["You have an unclean working tree!"])
        res = self.repo.git.status("--branch", "--porcelain")
        lines = str.splitlines(res)
        if len(lines) > 0 and "[ahead " in lines[0]:
            return Result(success=False, messages=["Local and remote not synced!"])
        return Result(success=True)


@dataclass
class RunTestsStep(Step):
    short_name: str = "run_tests"
    description: str = "Run test-suite"

    def run(self) -> Result:
        success = subprocess.run(["nox", "-r"]).returncode == 0
        return Result(success=success)


@dataclass
class CheckChangelogStep(GitStep):
    short_name: str = "check_changelog"
    description: str = "Make sure changelog was updated"

    def run(self) -> Result:
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
            return Result(
                success=False,
                messages=["Could not find Changelog in paths:", f"{paths}"],
            )
        current_version: str = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
        if current_version == "0.1.0":
            if os.path.getsize(cl_path) > 0:
                # there is a changelog file and it contains something
                return Result(success=True)
            else:
                return Result(
                    success=False, messages=[f"Changelog file '{cl_path}' empty"]
                )
        # check if there is a diff
        res = self.repo.git("diff", current_version, "--", cl_path)
        success = len(res.stdout.decode()) > 0
        return Result(success=success)

import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

import toml


@dataclass
class Result:
    success: bool
    messages: Iterable[str] = None


@dataclass
class Step(ABC):
    short_name: str
    description: str

    @abstractmethod
    def run(self) -> Result:
        raise NotImplementedError


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
class CheckOnMainStep(Step):
    short_name: str = "check_on_main"
    description: str = "Make sure you're on main/master branch"

    def run(self) -> Result:
        res = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True
        )
        current_branch = res.stdout.decode().strip()
        success = current_branch == "main" or current_branch == "master"
        return Result(success=success)


@dataclass
class CheckCleanGitStep(Step):
    short_name: str = "check_clean_git"
    description: str = "Make sure git is clean"

    def run(self) -> Result:
        success = (
            subprocess.check_output(["git", "status", "--porcelain"]).decode() == ""
        )
        return Result(success=success)


@dataclass
class RunTestsStep(Step):
    short_name: str = "run_tests"
    description: str = "Run test-suite"

    def run(self) -> Result:
        success = subprocess.run(["nox", "-r"]).returncode == 0
        return Result(success=success)


@dataclass
class CheckChangelogStep(Step):
    short_name: str = "check_changelog"
    description: str = "Make sure changelog was updated"

    def run(self) -> bool:
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
        current_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
        if current_version == "0.1.0":
            if os.path.getsize(cl_path) > 0:
                # there is a changelog file and it contains something
                return Result(success=True)
            else:
                return Result(
                    success=False, messages=[f"Changelog file '{cl_path}' empty"]
                )
        # check if there is a diff
        res = subprocess.check_output(
            ["git", "diff", current_version, "--", cl_path], capture_output=True
        )
        success = len(res.stdout.decode()) > 0
        return Result(success=success)

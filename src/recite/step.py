import os
import subprocess
from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Iterable, Optional

import toml
import typer
from git import Repo
from git.exc import GitCommandError

VersionBump = namedtuple("VersionBump", ["previous_version", "new_version"])


@dataclass(kw_only=True)
class Result:
    success: bool
    messages: Optional[Iterable[str]] = None
    return_value: Any = None


@dataclass(kw_only=True)
class StepMixin:
    short_name: str
    description: str
    skip: bool = False
    project_dir: Optional[str] = None


class Step(ABC, StepMixin):
    @abstractmethod
    def run(self) -> Result:
        raise NotImplementedError  # pragma: no cover


class GitStep(Step):
    @abstractmethod
    def _run(self) -> Result:
        raise NotImplementedError  # pragma: no cover

    def run(self):
        self.repo = Repo(self.project_dir)  # pragma: no cover
        return self._run()


class DynamicVersionDescriptionGitStep(GitStep):
    _new_version: str
    prefix: str

    @property
    def new_version(self) -> str:
        return self._new_version

    @new_version.setter
    def new_version(self, new_v: str):
        self.description += f" [blue]{self.prefix}{new_v}[/blue]"
        self._new_version = new_v


@dataclass(kw_only=True)
class CheckPyProjectStep(Step):
    short_name: str = "check_pyproject_toml"
    description: str = "Make sure you have a (non-empty) pyproject.toml"

    def run(self) -> Result:
        success = (
            os.path.isfile("pyproject.toml") and os.path.getsize("pyproject.toml") > 0
        )
        return Result(success=success)


@dataclass(kw_only=True)
class CheckOnMainStep(GitStep):
    short_name: str = "check_on_main"
    description: str = "Make sure you're on main/master branch"

    def _run(self) -> Result:
        current_branch = self.repo.active_branch.name
        success = current_branch == "main" or current_branch == "master"
        return Result(success=success)


@dataclass(kw_only=True)
class CheckCleanGitStep(GitStep):
    short_name: str = "check_clean_git"
    description: str = "Make sure git is clean"
    allow_untracked_files: bool = False

    def _run(self) -> Result:
        if self.repo.is_dirty(untracked_files=self.allow_untracked_files):
            return Result(success=False, messages=["You have an unclean working tree!"])
        self.repo.git.fetch()
        res = self.repo.git.status("--branch", "--porcelain")
        lines = str.splitlines(res)
        if len(lines) > 0:
            if "[ahead " in lines[0] or "[behind " in lines[0]:
                return Result(success=False, messages=["Local and remote not synced!"])
        return Result(success=True)


@dataclass(kw_only=True)
class RunTestsStep(Step):
    short_name: str = "run_tests"
    description: str = "Run test-suite"

    def run(self) -> Result:
        success = subprocess.run(["nox", "-r"]).returncode == 0
        return Result(success=success)


@dataclass(kw_only=True)
class CheckChangelogStep(GitStep):
    short_name: str = "check_changelog"
    description: str = "Make sure changelog was updated"
    prefix: str = "v"

    def _run(self) -> Result:
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
        res = self.repo.git.diff(f"{self.prefix}{current_version}", "--", cl_path)
        success = len(res) > 0
        return Result(success=success)


@dataclass(kw_only=True)
class BumpVersionStep(Step):
    bump_rule: str
    short_name: str = "bumpversion"
    description: str = "Bump version"

    def run(self, dry_run: bool = False) -> Result:
        command = ["poetry", "version", self.bump_rule]
        if dry_run:
            command.append("--dry-run")
        res = subprocess.run(command, capture_output=True)
        if res.returncode == 0:
            bump_message = res.stdout.decode().strip()
            previous_version = bump_message.split(" ")[3]
            new_version = bump_message.split(" ")[5]
            part_message = f"version from [yellow]{previous_version}[/yellow] to [blue]{new_version}[/blue]"
            if dry_run:
                return Result(
                    success=True,
                    messages=[f"Would bump {part_message}"],
                    return_value=VersionBump(
                        previous_version=previous_version, new_version=new_version
                    ),
                )
            return Result(success=True, messages=[f"Bumped {part_message}"])
        return Result(success=False, messages=str.splitlines(res.stderr.decode()))


@dataclass(kw_only=True)
class CommitVersionBumpStep(GitStep):
    short_name: str = "commitbump"
    description: str = "Commit version bump"
    remote: str = "origin"
    commit_message: str = "Bumped version"

    def _run(self) -> Result:
        try:
            self.repo.git.add("pyproject.toml")
            self.repo.git.commit("-m", self.commit_message)
            self.repo.git.push(self.remote)
        except GitCommandError as e:
            return Result(success=False, messages=[e.stderr.strip()])
        return Result(success=True)


@dataclass(kw_only=True)
class GitTagStep(DynamicVersionDescriptionGitStep):
    short_name: str = "gittag"
    description: str = "Create git tag"
    prefix: str = "v"

    def _run(self) -> Result:
        if not hasattr(self, "_new_version"):
            return Result(
                success=False, messages=["Can't tag if no new version is provided"]
            )
        try:
            self.repo.git.tag(f"{self.prefix}{self.new_version}")
        except GitCommandError as e:
            return Result(success=False, messages=[e.stderr.strip()])
        return Result(success=True)


@dataclass(kw_only=True)
class PushTagStep(DynamicVersionDescriptionGitStep):
    short_name: str = "pushtag"
    description: str = "Push git tag"
    remote: str = "origin"
    prefix: str = "v"

    def _run(self) -> Result:
        if self.new_version is None:
            return Result(
                success=False, messages=["Can't tag if no new version is provided"]
            )
        try:
            self.repo.git.push(self.remote, f"{self.prefix}{self.new_version}")
        except GitCommandError as e:
            return Result(success=False, messages=[e.stderr.strip()])
        return Result(success=True)


@dataclass(kw_only=True)
class PoetryPublishStep(Step):
    short_name: str = "publish"
    description: str = "Build and publish with poetry"
    pypy_token_name: str = "PYPI_TOKEN"

    def run(self) -> Result:
        command = ["poetry", "publish", "--build"]
        if os.getenv(self.pypy_token_name):
            token = os.getenv(self.pypy_token_name)
            assert token  # for mypy
            command.extend(["--username", "__token__", "--password", token])
        else:
            user_name = typer.prompt("Please enter your PyPI username")
            password = typer.prompt("Please enter your PyPI password", hide_input=True)
            command.extend(["--username", user_name, "--password", password])
        res = subprocess.run(command)
        if res.returncode != 0:
            return Result(success=False, messages=[res.stderr.decode().strip()])
        return Result(success=True, messages=["Build and published successfully!"])


@dataclass(kw_only=True)
class GithubReleaseReminderStep(Step):
    short_name: str = "githubreleasreminder"
    description: str = "Remind you to upload build as github release"

    def run(self) -> Result:
        gh_released = typer.confirm(
            "Please create a github release now! Did you do it?"
        )
        if not gh_released:
            return Result(
                success=False,
                messages=["You did not want to create a github release..."],
            )
        return Result(success=True)

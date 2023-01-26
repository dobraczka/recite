import os
import pathlib
from collections import namedtuple
from dataclasses import dataclass
from typing import Optional
from unittest import mock

import pytest
import toml

from recite.step import (
    CheckChangelogStep,
    CheckCleanGitStep,
    CheckOnMainStep,
    CheckPyProjectStep,
    RunTestsStep,
)


def create_file(
    my_tmp_path: pathlib.Path, file_name: str, content: Optional[str] = None
):
    # create a file "myfile" in "mydir" in temp folder
    filepath = my_tmp_path / file_name
    with filepath.open("w", encoding="utf-8") as f:
        if content is not None:
            f.write(content)


def create_versioned_pyproject_toml(my_tmp_path: pathlib.Path, version: str):
    create_file(
        my_tmp_path,
        "pyproject.toml",
        toml.dumps({"tool": {"poetry": {"version": version}}}),
    )


@dataclass
class MockGit:
    unsynced: bool = False
    has_diff: bool = False

    def status(self, branch: str, porcelain_str: str) -> str:
        if self.unsynced:
            return "## main...origin/main [ahead 1]"
        return ""

    def diff(self, *args) -> str:
        if self.has_diff:
            return "diff --git just a test"
        return ""


@dataclass
class MockBranch:
    name: str


@dataclass
class MockRepo:

    git: Optional[MockGit] = None
    dirty: bool = False
    active_branch: Optional[MockBranch] = None

    def is_dirty(self) -> bool:
        return self.dirty


def mock_post_init(self):
    self.repo = MockRepo()


@pytest.mark.parametrize("create, e_success", [(True, True), (False, False)])
def test_check_pyproject_step(create, e_success, tmp_path):
    os.chdir(tmp_path)
    if create:
        create_file(tmp_path, "pyproject.toml", "test")
    assert CheckPyProjectStep(tmp_path).run().success == e_success


@mock.patch("recite.step.CheckOnMainStep.__post_init__", mock_post_init)
@pytest.mark.parametrize(
    "branch_name, e_success",
    [
        ("main", True),
        ("master", True),
        ("hotfix", False),
    ],
)
def test_check_on_main(branch_name, e_success, tmp_path):
    step = CheckOnMainStep(tmp_path)
    step.repo.active_branch = MockBranch(name=branch_name)
    assert step.run().success == e_success


@mock.patch("recite.step.CheckCleanGitStep.__post_init__", mock_post_init)
@pytest.mark.parametrize(
    "is_dirty, unsynced, e_success",
    [
        (True, False, False),
        (False, False, True),
        (False, True, False),
    ],
)
def test_check_git_dirty(is_dirty, unsynced, e_success, tmp_path):
    step = CheckCleanGitStep(tmp_path)
    step.repo.dirty = is_dirty
    step.repo.git = MockGit(unsynced=unsynced)
    assert step.run().success == e_success


@mock.patch("recite.step.subprocess")
@pytest.mark.parametrize("ret_code, e_success", [(True, True), (False, False)])
def test_run_test_suite(mock_subproc, ret_code, e_success):
    def mock_run(*args):
        # some object that has the right returncode
        returncode = 0 if e_success else 1
        return namedtuple("ReturnObject", ["returncode"])(returncode)

    mock_subproc.run = mock_run
    step = RunTestsStep("somedir")
    assert step.run().success == e_success


@mock.patch("recite.step.CheckChangelogStep.__post_init__", mock_post_init)
@pytest.mark.parametrize(
    "file_name, content, current_version, has_diff, e_success",
    [
        (None, None, "0.1.0", False, False),
        ("CHANGELOG", None, "0.1.0", False, False),
        ("CHANGELOG", "Changes", "0.1.0", False, True),
        ("CHANGELOG.md", "Changes", "0.1.0", False, True),
        ("CHANGELOG.rst", "Changes", "0.1.0", False, True),
        ("CHANGELOG", "Changes", "0.2.0", False, False),
        ("CHANGELOG", "Changes", "0.2.0", True, True),
    ],
)
def test_check_changelog(
    file_name, e_success, content, current_version, has_diff, tmp_path
):
    create_versioned_pyproject_toml(tmp_path, current_version)
    if file_name:
        create_file(tmp_path, file_name, content)
    os.chdir(tmp_path)
    step = CheckChangelogStep(tmp_path)
    step.repo.git = MockGit(has_diff=has_diff)
    assert step.run().success == e_success

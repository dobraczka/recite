import os
from collections import namedtuple
from unittest import mock

import pytest
import toml
from git import Repo

from recite.step import (
    BumpVersionStep,
    CheckChangelogStep,
    CheckCleanGitStep,
    CheckOnMainStep,
    CheckPyProjectStep,
    CommitVersionBumpStep,
    GithubReleaseReminderStep,
    GitTagStep,
    Result,
    RunTestsStep,
    VersionBump,
)

from .mocks import MockBranch, MockGit, MockRepo, mock_run
from .utils import create_file, create_versioned_pyproject_toml


@pytest.mark.parametrize("create, e_success", [(True, True), (False, False)])
def test_check_pyproject_step(create, e_success, tmp_path):
    os.chdir(tmp_path)
    if create:
        create_file(tmp_path, "pyproject.toml", "test")
    assert CheckPyProjectStep().run().success == e_success


@mock.patch("recite.step.GitStep.run", mock_run)
@pytest.mark.parametrize(
    "branch_name, e_success",
    [
        ("main", True),
        ("master", True),
        ("hotfix", False),
    ],
)
def test_check_on_main(branch_name, e_success, tmp_path):
    step = CheckOnMainStep(project_dir=tmp_path)
    repo = MockRepo()
    repo.active_branch = MockBranch(name=branch_name)
    assert step.run(repo=repo).success == e_success


@mock.patch("recite.step.GitStep.run", mock_run)
@pytest.mark.parametrize(
    "is_dirty, unsynced, e_success",
    [
        (True, False, False),
        (False, False, True),
        (False, True, False),
    ],
)
def test_check_git_dirty(is_dirty, unsynced, e_success, tmp_path):
    step = CheckCleanGitStep(project_dir=tmp_path)
    repo = MockRepo(dirty=is_dirty)
    git = MockGit(unsynced=unsynced)
    assert step.run(repo=repo, git=git).success == e_success


@mock.patch("recite.step.subprocess")
@pytest.mark.parametrize("ret_code, e_success", [(True, True), (False, False)])
def test_run_test_suite(mock_subproc, ret_code, e_success):
    def mock_run(*args):
        # some object that has the right returncode
        returncode = 0 if e_success else 1
        return namedtuple("ReturnObject", ["returncode"])(returncode)

    mock_subproc.run = mock_run
    step = RunTestsStep()
    assert step.run().success == e_success


@mock.patch("recite.step.GitStep.run", mock_run)
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
    step = CheckChangelogStep(project_dir=tmp_path)
    git = MockGit(has_diff=has_diff)
    assert step.run(git=git).success == e_success


@pytest.mark.parametrize(
    "current_version, bump_rule, is_dry, expected_in_toml, expected_result",
    [
        (
            "0.1.0",
            "patch",
            True,
            "0.1.0",
            Result(success=True, return_value=VersionBump("0.1.0", "0.1.1")),
        ),
        (
            "0.1.0",
            "patch",
            False,
            "0.1.1",
            Result(success=True),
        ),
        (
            "0.1.0",
            "nonexisting command",
            False,
            "0.1.0",
            Result(success=False),
        ),
    ],
)
def test_bump_version(
    current_version, bump_rule, is_dry, expected_in_toml, expected_result, tmp_path
):
    create_versioned_pyproject_toml(tmp_path, current_version)
    os.chdir(tmp_path)
    step = BumpVersionStep(bump_rule=bump_rule)
    result = step.run(dry_run=is_dry)
    if is_dry:
        assert result.return_value == expected_result.return_value
    assert result.success == expected_result.success
    assert (
        expected_in_toml
        == toml.load(tmp_path / "pyproject.toml")["tool"]["poetry"]["version"]
    )


@mock.patch("recite.step.GitStep.run", mock_run)
def test_git_tag_step_fails():
    assert not GitTagStep().run().success


def test_failed_version_bump(tmp_path):
    os.chdir(tmp_path)
    Repo.init(tmp_path)
    assert not CommitVersionBumpStep(project_dir=tmp_path).run().success


@mock.patch("typer.confirm", return_value=False)
def test_no_gh_reminder(mocked):
    assert not GithubReleaseReminderStep().run().success

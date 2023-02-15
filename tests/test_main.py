import os
from unittest import mock

import pytest
from typer.testing import CliRunner

from recite.main import app

from .mocks import MockStep, mock_run

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


@mock.patch("recite.step.GitStep.run", mock_run)
def test_list_checks(tmpdir):
    os.chdir(tmpdir)
    result = runner.invoke(app, ["list-checks"])
    assert result.exit_code == 0
    assert "Available Checks" in result.stdout


def test_main_fail(tmpdir):
    os.chdir(tmpdir)
    result = runner.invoke(app, ["release", "patch"])
    assert "✘ Make sure you have a (non-empty) pyproject.toml" in result.stdout
    assert result.exit_code == 1


@mock.patch("typer.confirm")
@pytest.mark.parametrize("release_type", ["patch", "initial"])
def test_main(mock_typer, release_type, tmpdir, mocker):
    os.chdir(tmpdir)
    mock_typer.return_value = True
    mocker.patch("recite.main.BumpVersionStep", MockStep)
    mocker.patch("recite.main.CheckChangelogStep", MockStep)
    mocker.patch("recite.main.CheckCleanGitStep", MockStep)
    mocker.patch("recite.main.CheckOnMainStep", MockStep)
    mocker.patch("recite.main.CheckPyProjectStep", MockStep)
    mocker.patch("recite.main.CommitVersionBumpStep", MockStep)
    mocker.patch("recite.main.GithubReleaseReminderStep", MockStep)
    mocker.patch("recite.main.GitTagStep", MockStep)
    mocker.patch("recite.main.PoetryPublishStep", MockStep)
    mocker.patch("recite.main.PushTagStep", MockStep)
    mocker.patch("recite.main.RunTestsStep", MockStep)
    result = runner.invoke(app, ["release", release_type])
    assert result.exit_code == 0

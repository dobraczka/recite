import os
from dataclasses import dataclass
from unittest import mock

import click
import pytest

from recite.console import ReciteConsole
from recite.runner import CheckStepRunner, PerformReleaseRunner
from recite.step import (
    BumpVersionStep,
    CommitVersionBumpStep,
    GithubReleaseReminderStep,
    GitTagStep,
    PushTagStep,
    Result,
    VersionBump,
)

from .mocks import MockStep, mock_run
from .utils import create_versioned_pyproject_toml


@dataclass(kw_only=True)
class MockBumpVersionStep(BumpVersionStep):
    short_name: str = "mockstep"
    description: str = "Mock a step"
    bump_rule: str = "patch"
    success: bool
    previous_version: str = "0.1.0"
    new_version: str = "0.1.0"

    def run(self, dry_run: bool = False) -> Result:
        return Result(
            success=self.success,
            messages=["some msg"],
            return_value=VersionBump(
                previous_version=self.previous_version, new_version=self.new_version
            ),
        )


@mock.patch("typer.confirm", return_value=True)
@pytest.mark.parametrize("successes", [([True, True]), ([False])])
@pytest.mark.parametrize("runner_cls", [CheckStepRunner, PerformReleaseRunner])
def test_runner(mocked, successes, runner_cls):
    steps = [MockBumpVersionStep(success=s) for s in successes]
    runner = runner_cls(steps=steps, console=ReciteConsole())
    assert all(successes) == runner.run_steps()


@mock.patch("typer.confirm", return_value=False)
def test_release_runner_no_confirm(mocked):
    runner = PerformReleaseRunner(
        steps=[MockBumpVersionStep(success=True)], console=ReciteConsole()
    )
    with pytest.raises(click.exceptions.Abort):
        runner.run_steps()


@mock.patch("typer.confirm", return_value=True)
@mock.patch("recite.step.GitStep.run", mock_run)
@pytest.mark.parametrize("bump_rule, current_version", [("patch", "0.1.0")])
def test_full_release_runner(mocked, bump_rule, current_version, tmp_path):
    create_versioned_pyproject_toml(tmp_path, current_version)
    os.chdir(tmp_path)
    # do not include poetry publish step
    steps = [
        BumpVersionStep(bump_rule=bump_rule),
        CommitVersionBumpStep(),
        GitTagStep(),
        PushTagStep(),
        GithubReleaseReminderStep(),
    ]
    runner = PerformReleaseRunner(steps=steps, console=ReciteConsole())
    runner.run_steps()


@pytest.fixture
def mock_step_list():
    return [
        MockStep(short_name="first", description="A desc"),
        MockStep(short_name="second", description="Another desc"),
        MockStep(short_name="third", description="Yet another desc"),
    ]


@pytest.mark.parametrize(
    "skip, expected",
    [
        (None, ["first", "second", "third"]),
        ("second", ["first", "third"]),
        ("wrong", None),
        ("first,second", ["third"]),
        ("first,second,wrong", None),
        ("first,second,third", []),
    ],
)
def test_skipped_checks(skip, expected, mock_step_list):
    runner = CheckStepRunner(
        beginning_message="",
        console=ReciteConsole(),
        steps=mock_step_list,
        skip_steps=skip,
    )
    res = runner.run_steps()
    if expected is None:
        assert not res
    else:
        assert expected == [step.short_name for step in runner.steps if step.was_run]

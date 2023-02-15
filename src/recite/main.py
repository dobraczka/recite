import os
from typing import Optional

import typer

from .console import ReciteConsole
from .runner import CheckStepRunner, PerformReleaseRunner
from .step import (
    BumpVersionStep,
    CheckChangelogStep,
    CheckCleanGitStep,
    CheckOnMainStep,
    CheckPyProjectStep,
    CommitVersionBumpStep,
    GithubReleaseReminderStep,
    GitTagStep,
    PoetryPublishStep,
    PushTagStep,
    RunTestsStep,
)

console = ReciteConsole()
app = typer.Typer()


def _setup(allow_untracked_files: bool = False, skip_checks: Optional[str] = None):
    project_dir = os.getcwd()
    console = ReciteConsole()
    checks = CheckStepRunner(
        steps=[
            CheckPyProjectStep(),
            CheckOnMainStep(project_dir=project_dir),
            CheckCleanGitStep(
                project_dir=project_dir, allow_untracked_files=allow_untracked_files
            ),
            RunTestsStep(),
            CheckChangelogStep(project_dir=project_dir),
        ],
        console=console,
        skip_steps=skip_checks,
    )
    return project_dir, console, checks


@app.command()
def list_checks():
    _, console, checks = _setup()
    console.print_checks_table(checks.steps)


@app.command()
def release(
    release_type: str = typer.Argument(
        ..., help="What type of release is this? For initial release use 'initial'"
    ),
    allow_untracked_files: bool = typer.Option(
        False, help="Allow files not tracked by git"
    ),
    remote: str = typer.Option("origin", help="Where should the tag be pushed?"),
    commit_message: str = typer.Option(
        "Bumped version", help="Commit message for version bump"
    ),
    git_tag_prefix: str = typer.Option("v", help="Prefix for git tag"),
    skip_checks: str = typer.Option(
        None,
        help="Comma-seperated list of checks referenced by their shortnames. You can print a list of checks with 'recite list-checks'",
    ),
):
    project_dir, console, checks = _setup(
        allow_untracked_files=allow_untracked_files, skip_checks=skip_checks
    )
    successful = checks.run_steps()
    if not successful:
        raise typer.Exit(code=1)
    else:
        is_initial = False
        if release_type == "initial":
            steps = [
                GitTagStep(prefix=git_tag_prefix),
                PushTagStep(remote=remote, prefix=git_tag_prefix),
                PoetryPublishStep(),
                GithubReleaseReminderStep(),
            ]
            is_initial = True
        else:
            steps = [
                BumpVersionStep(bump_rule=release_type),
                CommitVersionBumpStep(commit_message=commit_message),
                GitTagStep(prefix=git_tag_prefix),
                PushTagStep(remote=remote, prefix=git_tag_prefix),
                PoetryPublishStep(),
                GithubReleaseReminderStep(),
            ]
        PerformReleaseRunner(
            steps=steps,
            console=console,
            is_initial=is_initial,
        ).run_steps()


if __name__ == "__main__":
    app()  # pragma: no cover

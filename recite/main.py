from typing import Iterable
import os

import typer

from .console import ReciteConsole
from .step import (
    CheckChangelogStep,
    CheckCleanGitStep,
    CheckOnMainStep,
    CheckPyProjectStep,
    RunTestsStep,
    Step,
)

console = ReciteConsole()
app = typer.Typer()


def run_steps(steps: Iterable[Step]) -> bool:
    console.print_message(
        message=":eyes: Checking everything to make sure you are ready to release :eyes:"
    )
    for number, step in enumerate(steps, start=1):
        result = step.run()
        if result.success:
            console.print_success(message=step.description, number=number)
        else:
            console.print_failure(message=step.description, number=number)
            if result.messages is not None:
                console.print_multiple_messages(
                    messages=result.messages, indent_count=1, color="bad"
                )
            return False
        if result.messages is not None:
            console.print_multiple_messages(
                messages=result.messages, indent_count=1, color="good"
            )
    return True


@app.command()
def main(
    allow_untracked_files: bool = typer.Option(
        False, help="Allow files not tracked by git"
    )
):
    project_dir = os.getcwd()
    successful = run_steps(
        [
            CheckPyProjectStep(project_dir=project_dir),
            CheckOnMainStep(project_dir=project_dir),
            CheckCleanGitStep(project_dir=project_dir, allow_untracked_files=allow_untracked_files),
            RunTestsStep(project_dir=project_dir),
            CheckChangelogStep(project_dir=project_dir),
        ]
    )
    if not successful:
        typer.Exit(code=1)


if __name__ == "__main__":
    app()

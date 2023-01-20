import sys
from typing import Iterable

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


def run_steps(steps: Iterable[Step]):
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
            sys.exit(1)


@app.command()
def main():
    run_steps(
        [
            CheckPyProjectStep(),
            CheckOnMainStep(),
            CheckCleanGitStep(),
            RunTestsStep(),
            CheckChangelogStep(),
        ]
    )


if __name__ == "__main__":
    app()

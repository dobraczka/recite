import sys
from typing import Iterable

import typer

from .console import ReciteConsole
from .step import (
    CheckChangelogStep,
    CheckCleanGitStep,
    CheckOnMainStep,
    RunTestsStep,
    Step,
)

console = ReciteConsole()
app = typer.Typer()


def run_steps(steps: Iterable[Step]):
    console.print(message="Checking everything to make sure you are ready to release")
    for number, step in enumerate(steps, start=1):
        result = step.run()
        if result.success:
            console.print_success(message=step.description, number=number)
        else:
            console.print_failure(message=step.description, number=number)
            if result.messages is not None:
                for msg in result.messages:
                    console.print_error(message=msg, indent_count=1)
            sys.exit(1)


@app.command()
def main():
    run_steps(
        [CheckOnMainStep(), CheckCleanGitStep(), RunTestsStep(), CheckChangelogStep()]
    )


if __name__ == "__main__":
    app()

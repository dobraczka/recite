from dataclasses import dataclass
from typing import Iterable, Optional

import typer

from recite.console import ReciteConsole
from recite.step import BumpVersionStep, DynamicVersionDescriptionGitStep, Step


@dataclass(kw_only=True)
class StepRunner:
    beginning_message: str
    console: ReciteConsole
    steps: Iterable[Step]
    skip_steps: Optional[str] = None

    def _validate_skipped(self):
        if self.skip_steps is None:
            return True
        skip_list = self.skip_steps.split(",")
        for step in self.steps:
            if step.short_name in skip_list:
                step.skip = True
                skip_list.remove(step.short_name)
        if len(skip_list) > 0:
            self.console.print_multiple_messages(
                messages=[
                    f"Unknown step(s) to skip: {skip_list}",
                    "You can get the list of available checks via [italic]`recite list-checks`[/italic]",
                ],
                indent_count=1,
                color="red",
            )
            return False
        return True

    def pre_run(self):
        pass  # pragma: no cover

    def post_run(self):
        pass  # pragma: no cover

    def run_steps(self) -> bool:
        if not self._validate_skipped():
            return False
        self.pre_run()
        self.console.print_message(message=self.beginning_message)
        for number, step in enumerate(self.steps, start=1):
            if step.skip:
                self.console.print_message(
                    message=f"Skipping {step.short_name} ~",
                    color="italic",
                    indent_count=1,
                    indent_whitespace=" ",
                    indent_char="~",
                )
                continue
            result = step.run()
            if result.success:
                self.console.print_success(message=step.description, number=number)
            else:
                self.console.print_failure(message=step.description, number=number)
                if result.messages is not None:
                    self.console.print_multiple_messages(
                        messages=result.messages, indent_count=1, color="bad"
                    )
                return False
            if result.messages is not None:
                self.console.print_multiple_messages(
                    messages=result.messages, indent_count=1, color="good"
                )
        self.post_run()
        return True


@dataclass(kw_only=True)
class CheckStepRunner(StepRunner):
    beginning_message: str = (
        ":eyes: Checking everything to make sure you are ready to release :eyes:"
    )

    def post_run(self):
        self.console.print_message(
            message=":nerd_face: Everything looks perfect! :nerd_face:"
        )


@dataclass(kw_only=True)
class PerformReleaseRunner(StepRunner):
    beginning_message: str = ":sparkles: Performing release :sparkles:"
    is_initial: bool = False

    def pre_run(self):
        self.console.print_message("I will perform the following steps:")
        new_version = "0.1.0" if self.is_initial else ""
        for step in self.steps:
            msg = step.description
            if isinstance(step, BumpVersionStep):
                result = step.run(dry_run=True)
                msg = result.messages[0]
                new_version = result.return_value.new_version
            elif isinstance(step, DynamicVersionDescriptionGitStep):
                step.new_version = new_version
                # update msg with updated description
                msg = step.description
            self.console.print_message(message=msg, indent_count=1)
        proceed = typer.confirm("Do you want to proceed?")
        if not proceed:
            raise typer.Abort()

    def post_run(self):
        self.console.print_message(
            message=":rocket: Congrats to your release! :rocket:"
        )

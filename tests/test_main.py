from dataclasses import dataclass

import pytest

from recite.main import run_steps
from recite.step import Result, Step


@dataclass
class MockStep(Step):

    short_name: str = "mockstep"
    description: str = "Mocks step execution"
    should_succeed: bool = False

    def run(self) -> Result:
        return Result(success=self.should_succeed)


@pytest.mark.parametrize(
    "steps_param, e_success",
    [([True] * 3, True), ([False] * 5, False), ([True, True, False], False)],
)
def test_run_steps(steps_param, e_success):
    fake_dir = "we don't need a dir"
    steps = [
        MockStep(project_dir=fake_dir, should_succeed=should_succeed)
        for should_succeed in steps_param
    ]
    # smoketest for running steps
    assert run_steps(steps) == e_success

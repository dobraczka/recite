import os
from dataclasses import dataclass
from unittest import mock

import pytest

from recite.step import CheckCleanGitStep, CheckPyProjectStep


def create_file(my_tmp_path, file_name, content):
    # create a file "myfile" in "mydir" in temp folder
    filepath = my_tmp_path.join(file_name)
    with filepath.open("w", encoding="utf-8") as f:
        f.write("test")


@pytest.mark.parametrize("create, e_success", [(True, True), (False, False)])
def test_check_pyproject_step(create, e_success, tmpdir):
    os.chdir(tmpdir)
    if create:
        create_file(tmpdir, "pyproject.toml", "test")
    assert CheckPyProjectStep(tmpdir).run().success == e_success


@dataclass
class MockGit:
    unsynced: bool = False

    def status(self, branch: str, porcelain_str: str) -> str:
        if self.unsynced:
            return "## main...origin/main [ahead 1]"
        return ""


@dataclass
class MockRepo:

    git: MockGit = None
    dirty: bool = False

    def is_dirty(self) -> bool:
        return self.dirty


def mock_post_init(self):
    self.repo = MockRepo()


@mock.patch("recite.step.CheckCleanGitStep.__post_init__", mock_post_init)
@pytest.mark.parametrize(
    "is_dirty, unsynced, e_success",
    [
        (True, False, False),
        (False, False, True),
        (False, True, False),
    ],
)
def test_check_on_main_dirty(is_dirty, unsynced, e_success, tmpdir):
    step = CheckCleanGitStep(tmpdir)
    step.repo.dirty = is_dirty
    step.repo.git = MockGit(unsynced=unsynced)
    assert step.run().success == e_success

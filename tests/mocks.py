from dataclasses import dataclass, field
from typing import List, Optional

from recite.step import Result


@dataclass
class MockGit:
    unsynced: bool = False
    has_diff: bool = False
    added: List[str] = field(default_factory=list)
    commit_messages: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    pushes: List = field(default_factory=list)

    def status(self, branch: str, porcelain_str: str) -> str:
        if self.unsynced:
            return "## main...origin/main [ahead 1]"
        return ""

    def diff(self, *args) -> str:
        if self.has_diff:
            return "diff --git just a test"
        return ""

    def add(self, file_name: str):
        self.added.append(file_name)

    def commit(self, flag: str, msg: str):
        self.commit_messages.append(msg)

    def tag(self, tag: str):
        self.tags.append(tag)

    def push(self, remote: str, tag: Optional[str] = None):
        self.pushes.append((remote, tag))


@dataclass
class MockBranch:
    name: str


@dataclass
class MockRepo:

    git: Optional[MockGit] = None
    dirty: bool = False
    active_branch: Optional[MockBranch] = None

    def is_dirty(self, untracked_files: bool) -> bool:
        return self.dirty


class MockStep:
    def __init__(
        self,
        short_name: str = "mockstep",
        description: str = "mocks a step",
        skip: bool = False,
        was_run: bool = False,
        *args,
        **kwargs
    ):
        self.short_name = short_name
        self.description = description
        self.skip = skip
        self.was_run = was_run
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.was_run = True
        return Result(success=True)


def mock_run(self, repo: MockRepo = None, git: MockGit = None):
    if repo is None:
        self.repo = MockRepo()
    else:
        self.repo = repo
    if self.repo is not None:
        if git is None:
            self.repo.git = MockGit()
        else:
            self.repo.git = git
    return self._run()

def mock_subprocess_run(command):
    class Object(object):
        pass
    res = Object()
    res.returncode = 0
    return res


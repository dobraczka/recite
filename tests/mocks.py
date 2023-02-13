from dataclasses import dataclass, field
from typing import List, Optional


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


def mock_post_init(self):
    self.repo = MockRepo()


def mock_post_init_with_git(self):
    self.repo = MockRepo()
    self.repo.git = MockGit()

import subprocess
from functools import wraps
from typing import TYPE_CHECKING, ParamSpec, TypeVar, cast

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


P = ParamSpec("P")
R = TypeVar("R")


class GitClient:
    def __init__(self, repo_path: Path, target_branch: str = "master") -> None:
        self.repo_path = repo_path
        self.target_branch = target_branch
        self._validated = False

    def _validate(self) -> None:
        """Perform first git call checks to ensure that the system git target_branch is set correctly"""
        self._check_origin_exists()
        self._check_branch_valid()
        self._ensure_branch_checked_out()
        self._validated = True

    def _check_origin_exists(self) -> None:
        self._git("remote", "get-url", "origin")

    def _check_branch_valid(self) -> None:
        self._git("show-ref", "--verify", f"refs/heads/{self.target_branch}")

    def _ensure_branch_checked_out(self) -> None:
        if (
            self._git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
            != self.target_branch
        ):
            self._git("checkout", self.target_branch)

    def _git(self, *args: str | Path):
        return subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            check=True,
            capture_output=True,
            text=True,
        )

    @staticmethod
    def _requires_validation(func: Callable[P, R]) -> Callable[P, R]:
        """Decorator pattern to check that git is able to commit and push new data to the target branch at an origin"""

        @wraps(func)
        def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            instance = cast("GitClient", args[0])
            if not instance._validated:  # noqa: SLF001
                instance._validate()  # noqa: SLF001
            return func(*args, **kwargs)

        return _wrapper

    @_requires_validation
    def add(self, file_path: Path) -> None:
        """Add a new file on the target path"""
        self._git("add", file_path)

    @_requires_validation
    def commit(self, message: str) -> None:
        """Commit added files to the respository"""
        self._git("commit", "-m", message)

    @_requires_validation
    def pull(self) -> None:
        """Pull the latest version of the repo"""
        self._git("pull", "origin", self.target_branch)

    @_requires_validation
    def push(self) -> None:
        """Push commit to origin"""
        self._git("push", "origin", self.target_branch)

from pathlib import Path
import subprocess
from functools import wraps
from typing import Callable


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
        if self._git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip() != self.target_branch:
            self._git("checkout", self.target_branch)

    def _git(self, *args):
        return subprocess.run(
            ["git"] + list(args),
            cwd=self.repo_path,
            check=True,
            capture_output=True,
            text=True
        )

    @staticmethod
    def requires_validation(func) -> Callable:
        """Decorator pattern to check that git is able to commit and push new data to the target branch at an origin"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self._validated:
                self._validate()
            return func(self, *args, **kwargs)
        return wrapper

    @requires_validation
    def add(self, file_path: Path) -> None:
        """Add a new file on the target path"""
        self._git("add", file_path)

    @requires_validation
    def commit(self, message: str) -> None:
        """Commit added files to the respository"""
        self._git("commit", "-m", message)

    @requires_validation
    def pull(self) -> None:
        """pull the latest version of the repo"""
        self._git("pull", "origin", self.target_branch)

    @requires_validation
    def push(self) -> None:
        """Push commit to origin"""
        self._git("push", "origin", self.target_branch)

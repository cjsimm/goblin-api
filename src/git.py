import logging
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeVar, cast

import git

if TYPE_CHECKING:
    from collections.abc import Callable


P = ParamSpec("P")
R = TypeVar("R")


class GitClient:
    def __init__(self, repo_path: Path, target_branch: str = "master") -> None:
        self.repo_path = repo_path
        self.target_branch = target_branch
        self.repo = git.Repo(str(repo_path))
        self._validated = False

    def _validate(self) -> None:
        """Perform first git call checks to ensure that the system git target_branch is set correctly"""
        self._check_origin_exists()
        if self._is_unborn_head():
            gitkeep = ".gitkeep"
            placeholder = Path(self.repo_path) / gitkeep
            placeholder.touch()
            self.repo.index.add([gitkeep])
            self.repo.index.commit("Initial commit")
            self._create_and_checkout_local_branch(self.target_branch)
            self._push_branch_to_origin_and_set_upstream(self.target_branch)
        else:
            logging.info("Fetching origin for latest state")
            self.repo.remotes.origin.fetch()
            local_branch_exists = self._check_local_branch_exists(self.target_branch)
            remote_branch_exists = self._remote_branch_exists(self.target_branch)
            self._resolve_local_and_remote_branches(
                local_branch_exists, remote_branch_exists, self.target_branch
            )
        self._validated = True

    def _resolve_local_and_remote_branches(
        self, local_branch_exists: bool, remote_branch_exists: bool, target_branch: str
    ) -> None:
        """Align local and remote branches, if they both exist, otherwise create the branches in the missing location"""
        match (local_branch_exists, remote_branch_exists):
            case (True, True):
                target_head = self.repo.heads[target_branch]
                target_head.checkout()
                remote_ref = self.repo.remotes.origin.refs[target_branch]
                if (
                    target_head.tracking_branch is None
                    or target_head.tracking_branch != remote_ref
                ):
                    target_head.set_tracking_branch(remote_ref)
            case (True, False):
                self._push_branch_to_origin_and_set_upstream(target_branch)
            case (False, True):
                self.repo.git.checkout(target_branch)
            case (False, False):
                self._create_and_checkout_local_branch(target_branch)
                self._push_branch_to_origin_and_set_upstream(target_branch)

    def _create_and_checkout_local_branch(self, branch_name: str) -> git.Head:
        """Creates and checks out a new local branch."""
        logging.info(f"Creating and checking out new local branch '{branch_name}'...")
        new_head = self.repo.create_head(branch_name)
        new_head.checkout()
        return new_head

    def _is_unborn_head(self) -> bool:
        """Checks if the repository has an 'unborn' HEAD (no commits yet)."""
        return not self.repo.head.is_valid()

    def _check_local_branch_exists(self, branch_name: str) -> bool:
        """Checks if a branch with the given name exists in the repository's heads."""
        return branch_name in self.repo.heads

    def _check_origin_exists(self) -> None:
        self.repo.remote()

    def _remote_branch_exists(self, branch_name: str) -> bool:
        """Checks if the given branch name exists in remote origin"""
        return f"origin/{branch_name}" in self.repo.remotes.origin.refs

    def _ensure_branch_checked_out(self) -> None:
        if self.repo.active_branch.name != self.target_branch:
            self.repo.git.checkout(self.target_branch)

    def _push_branch_to_origin_and_set_upstream(self, branch_name: str) -> None:
        """Pushes the local branch to origin and sets it as the upstream tracking branch."""
        logging.info(
            f"Pushing local branch '{branch_name}' to origin and setting upstream..."
        )
        self.repo.git.push("--set-upstream", "origin", branch_name)

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
        self.repo.index.add([str(file_path)])

    @_requires_validation
    def commit(self, message: str) -> None:
        """Commit added files to the respository"""
        self.repo.index.commit(message)

    @_requires_validation
    def pull(self) -> None:
        """Pull the latest version of the repo"""
        origin = self.repo.remote()
        origin.pull(self.target_branch)

    @_requires_validation
    def push(self) -> None:
        """Push commit to origin"""
        origin = self.repo.remote()
        origin.push(self.target_branch)

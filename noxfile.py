import os
import tempfile
from types import TracebackType
from typing import Any

import nox
from nox.sessions import Session

nox.options.reuse_existing_virtualenvs = True

locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.7", "3.8", "3.9"])
def tests(session) -> Session:
    """Run the test suite (using Pytest)."""

    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install(session, "coverage[toml]", "pytest", "pytest-cov", "expects")
    session.run("pytest", *args)


@nox.session(python="3.7")
def format(session: Session) -> Session:
    """Run the code formatter (using Black)."""

    args = session.posargs or locations
    install(session, "black")
    session.run("black", *args)


# ===========================================================================
# Nox File Helpers
# ===========================================================================


class CustomNamedTemporaryFile:
    """
    Custom implementation of temporary files.

    This custom implementation is needed because of a specific limitation
    regarding the use of tempfile.NamedTemporaryFile. The limitation has to
    do with a situation where a given name can be used to open the file a
    second time *while the named temporary file is still open*. This works on
    POSIX systems but seems to fail on Windows. This custom implementation
    makes sure it works on both.
    """

    def __init__(self, mode: str = "wb", delete: bool = True):
        self._mode = mode
        self._delete = delete

    def __enter__(self) -> Any:
        """Generate and open random temporary file."""

        file_name = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        open(file_name, "x").close()

        self._tempfile = open(file_name, self._mode)

        return self._tempfile

    def __exit__(
        self, exc_type: type, exc_val: Exception, exc_tb: TracebackType
    ) -> None:
        """Close and remove all temporary files."""

        self._tempfile.close()

        if self._delete:
            os.remove(self._tempfile.name)


def install(session: Session, *args: str, **kwargs: Any) -> None:
    """
    This is a wrapper for session.install.

    The purpose is to generate a constraints file by running poetry export.
    That file can then be passed to pip using its --constraint option. The
    idea of constraints is that they are files which are requirements files,
    but that only control which version of a requirement is installed, not
    whether it is installed or not.

    The goal is to allow the installation of individual packages by using
    session.install but using Poetry's lock file to constrain their versions.

    Args:
        session: Instance of session currently executing.
        *args: Listing of packages to install.
        **kwargs: Keywords to provide execution options.
    """

    with CustomNamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)

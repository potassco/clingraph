import os

import nox

nox.options.sessions = "lint_pylint", "test"

EDITABLE_TESTS = True
PYTHON_VERSIONS = None
if "GITHUB_ACTIONS" in os.environ:
    PYTHON_VERSIONS = ["3.9", "3.11"]
    EDITABLE_TESTS = False


@nox.session
def dev(session):
    """
    Create a development environment in editable mode.

    Activate it by running `source .nox/dev/bin/activate`.
    """
    session.install("-e", ".[dev]")


@nox.session
def lint_pylint(session):
    """
    Run pylint.
    """
    session.install("-e", ".[lint_pylint,test]")
    session.run("pylint", "clingraph", "tests")


# @nox.session
# def typecheck(session):
#     """
#     Typecheck the code using mypy.
#     """
#     session.install("-e", ".[typecheck]")
#     session.run("mypy", "--strict", "-p", "clingraph", "-p", "tests")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """
    Run the tests.

    Accepts additional arguments which are passed to pytest.
    This can for example be used to selectively run test cases.
    """
    args = [".[test,gif,tex]"]
    if EDITABLE_TESTS:
        args.insert(0, "-e")
    session.install(*args)
    if session.posargs:
        session.run("pytest", "-v", *session.posargs)
    else:
        session.run("pytest", "-v")

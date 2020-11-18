import itertools
import os
import shlex
import sys

if sys.version_info >= (3, 9):
  List  = list
  Tuple = tuple
else:
  from typing import List
  from typing import Tuple

from pathlib import Path
from setuptools import setup
from subprocess import check_output

from typing import Optional


__here__ = Path(__file__).absolute().parent


version_file_path = __here__ / "candv" / "version.py"
exec(compile(version_file_path.read_text(), version_file_path, "exec"))


def maybe_get_shell_output(command: str) -> str:
  try:
    args = shlex.split(command)
    with open(os.devnull, "w") as devnull:
      return check_output(args, stderr=devnull).strip().decode()
  except Exception:
    pass


def maybe_get_current_branch_name() -> Optional[str]:
  return maybe_get_shell_output("git rev-parse --abbrev-ref HEAD")


def maybe_get_current_commit_hash() -> Optional[str]:
  return maybe_get_shell_output("git rev-parse --short HEAD")


def parse_requirements(file_path: Path) -> Tuple[List[str], List[str]]:
  requirements, dependencies = list(), list()

  with file_path.open("rt") as f:
    for line in f:
      line = line.strip()

      if not line or line.startswith("#"):
        continue

      if "://" in line:
        dependencies.append(line)

        line = line.split("#egg=", 1)[1]
        requirements.append(line)

      elif line.startswith("-r"):
        name = Path(line.split(" ", 1)[1])
        path = file_path.parent / name
        subrequirements, subdependencies = parse_requirements(path)
        requirements.extend(subrequirements)
        dependencies.extend(subdependencies)

      else:
        requirements.append(line)

  return requirements, dependencies


README = (__here__ / "README.rst").read_text()

STABLE_BRANCH_NAME  = "master"
CURRENT_COMMIT_HASH = maybe_get_current_commit_hash()
CURRENT_BRANCH_NAME = maybe_get_current_branch_name()
IS_CURRENT_BRANCH_STABLE = (CURRENT_BRANCH_NAME == STABLE_BRANCH_NAME)
BUILD_TAG = (
  f".{CURRENT_BRANCH_NAME}.{CURRENT_COMMIT_HASH}"
  if not IS_CURRENT_BRANCH_STABLE and CURRENT_COMMIT_HASH
  else ""
)

REQUIREMENTS_DIR_PATH = __here__ / "requirements"

TEST_REQUIREMENTS, TEST_DEPENDENCIES = parse_requirements(
  file_path=(REQUIREMENTS_DIR_PATH / "test.txt"),
)

setup(
  name="candv",
  version=VERSION,
  description=(
    "Constants and Values: create enum-like complext constants with the "
    "ability to attach arbitrary attributes to them, e.g. values, "
    "human-readable names, help texts and so on"
  ),
  long_description=README,
  long_description_content_type="text/x-rst",
  keywords=[
    "constants", "values", "structures", "choices", "enum",
  ],
  license="MIT",
  url=f"https://github.com/oblalex/candv/tree/v{VERSION}",

  author="Oleksandr Oblovatnyi",
  author_email="oblovatniy@gmail.com",

  packages=[
    "candv",
  ],

  python_requires=">=3.7",
  dependency_links=list(set(itertools.chain(
    TEST_DEPENDENCIES,
  ))),
  tests_require=TEST_REQUIREMENTS,
  test_suite="tests",

  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries",
  ],

  options={
    'egg_info': {
      'tag_build': BUILD_TAG,
      'tag_date':  False,
    },
  },

  zip_safe=True,
)

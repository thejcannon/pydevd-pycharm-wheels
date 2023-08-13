import os
import pathlib
import sys
import tarfile

# =====================
tar_gz_path = f'pydevd-pycharm-{sys.argv[1]}.tar.gz'
with tarfile.open(tar_gz_path, 'r:gz') as tar:
    for member in tar.getmembers():
        # Skip the first directory component
        member.path = '/'.join(member.path.split('/')[1:])
        tar.extract(member, path=".")

# =====================
setup_py = pathlib.Path("setup.py")

contents = setup_py.read_text()
contents = contents.replace(
  "name='pydevd-pycharm'",
  "name='pydevd-pycharm-wheels'",
)
contents = contents.replace(
  "url='https://github.com/JetBrains/intellij-community'",
  "url='https://github.com/thejcannon/pydevd-pycharm-wheels'",
)
contents = contents.replace(
  "long_description=README",
  "long_description='pydevd-pycharm uploaded with wheels.'",
)
contents = contents.replace(
    "import sys",
    "import sys; sys.path.append("")",
)

setup_py.write_text(contents)

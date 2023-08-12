import pathlib

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

setup_py.write_text(contents)

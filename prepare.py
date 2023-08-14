import pathlib
import sys
import tarfile

# =====================
tar_gz_path = 'pycharm.tar.gz'
with tarfile.open(tar_gz_path, 'r:gz') as tar:
    for member in tar.getmembers():
        if member.path.rsplit(".", 1)[-1] in {
            "dll", "pyd", "so", "dylib"
        }:
            continue

        if member.path.startswith(f"intellij-community-pycharm-{sys.argv[1]}/python/helpers/pydev"):
          member.path = '/'.join(member.path.split('/')[4:])
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
    "import sys; sys.path.append('')",
)
contents = contents.replace(
    """\
        args_with_binaries.update(dict(
            distclass=BinaryDistribution,
            ext_modules=[
                # In this setup, don't even try to compile with cython, just go with the .c file which should've
                # been properly generated from a tested version.
                Extension('_pydevd_frame_eval.pydevd_frame_evaluator', ['_pydevd_frame_eval/%s.c' % frame_eval_extension_name,])
            ]
        ))
""",
    """\
        args_with_binaries["ext_modules"].append(
            # In this setup, don't even try to compile with cython, just go with the .c file which should've
            # been properly generated from a tested version.
            Extension('_pydevd_frame_eval.pydevd_frame_evaluator', ['_pydevd_frame_eval/%s.c' % frame_eval_extension_name,])
        )
""",
)
contents = contents.replace(
    """setup(**args_with_binaries)""",
    """\
    args_with_binaries['distclass'] = BinaryDistribution
    args_with_binaries['ext_modules'] = args_with_binaries.get('ext_modules', []) + [
      Extension('pydevd_attach_to_process', ['pydevd_attach_to_process/dummy.c'])
    ]
    setup(**args_with_binaries)
""",
)
contents = contents.replace(
    "# Compile failed: just setup without compiling cython deps.",
    "raise",
)

setup_py.write_text(contents)

pathlib.Path("VERSION").write_text(sys.argv[1] + "\n")
pathlib.Path("pydevd_attach_to_process/dummy.c").write_text("")

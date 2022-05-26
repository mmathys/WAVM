from os import makedirs
from shutil import rmtree
from os.path import exists
from subprocess import run
from tasks.env import WAVM_BUILD_ROOT, WAVM_ROOT

from invoke import task


@task(default=True)
def cmake(
    ctx,
    clean=False,
    build="RelWithDebInfo",
    sanitiser="None",
    prof=False,
):
    """
    Configures the build
    """
    if clean and exists(WAVM_BUILD_ROOT):
        rmtree(WAVM_BUILD_ROOT)

    if not exists(WAVM_BUILD_ROOT):
        makedirs(WAVM_BUILD_ROOT)

    build_types = ["Release", "RelWithDebInfo", "Debug"]
    if build not in build_types:
        raise RuntimeError("Expected build to be in {}".format(build_types))

    cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE={}".format(build),
        WAVM_ROOT,
    ]

    run(" ".join(cmd), check=True, shell=True, cwd=WAVM_BUILD_ROOT)

    run("ninja", check=True, shell=True, cwd=WAVM_BUILD_ROOT)

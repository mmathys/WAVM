from subprocess import run
from os.path import join

from invoke import task
from tasks.env import WAVM_ROOT

WAVM_IMAGE_NAME = "wavm"
DOCKER_USER = "csegarragonz"


def _get_version():
    ver_file = join(WAVM_ROOT, "VERSION")

    with open(ver_file, "r") as fh:
        version = fh.read()

    version = version.strip()
    return version


def _get_docker_tag():
    ver = _get_version()
    return "{}/{}:{}".format(DOCKER_USER, WAVM_IMAGE_NAME, ver)


@task(default=True)
def build(ctx, nocache=False, push=False):
    """
    Build current version of faabric container
    """
    tag_name = _get_docker_tag()
    ver = _get_version()

    if nocache:
        no_cache_str = "--no-cache"
    else:
        no_cache_str = ""

    build_cmd = [
        "docker build",
        no_cache_str,
        "-t {}".format(tag_name),
        "-f Dockerfile",
        ".",
    ]
    build_cmd = " ".join(build_cmd)

    print(build_cmd)
    run(build_cmd, shell=True, check=True, cwd=WAVM_ROOT, env={"DOCKER_BUILDKIT": "1"})

    if push:
        push(ctx)


@task
def push(ctx):
    """
    Push current version of faabric container
    """
    tag_name = _get_docker_tag()

    cmd = "docker push {}".format(tag_name)
    print(cmd)
    run(cmd, shell=True, check=True)

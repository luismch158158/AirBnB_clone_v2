#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy"""

import os.path
from fabric.api import local, run, put, env
from datetime import datetime

env.hosts = ["52.73.82.123", "54.165.211.232"]


def do_pack():
    """generates a .tgz archive from
    the contents of the web_static"""

    try:
        local("mkdir -p versions")

        date = datetime.now().strftime("%Y%m%d%H%M%S")
        path = "versions/web_static_" + date + ".tgz"
        local("tar -cvzf {} web_static".format(path))
        return path

    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to
    your web servers"""

    if not os.path.exists(archive_path):
        return False

    try:

        # archive_path = versions/web_static_20170315003959.tgz

        # Only file with extension
        # web_static_20170315003959.tgz
        only_file = archive_path.split("/")[-1]

        # Only file without extension
        # web_static_20170315003959
        only_name = only_file.split(".")[0]

        # Path with file without extension
        # /data/web_static/releases/web_static_20170315003959/
        path = "/data/web_static/releases/" + only_name + "/"
        put(archive_path, "/tmp/")
        run("mkdir -p {:s}".format(path))
        run("tar -xzf /tmp/{:s} -C {:s}".format(only_file, path))
        run("rm /tmp/{:s}".format(only_file))
        run("mv {:s}web_static/* {:s}".format(path, path))
        run("rm -rf {:s}web_static".format(path))
        link = "/data/web_static/current"
        run("rm -rf {:s}".format(link))
        run("ln -s {:s} {:s}".format(path, link))
        print("New version deployed!")
        return True

    except Exception:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    path_file = do_pack()

    if path_file is None:
        return False

    return do_deploy(path_file)

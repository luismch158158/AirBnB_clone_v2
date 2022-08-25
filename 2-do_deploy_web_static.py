#!/usr/bin/python3
"""abric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using
the function do_deploy"""

import os.path
from fabric.api import run, put, env
env.hosts = ["52.73.82.123", "54.165.211.232"]


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

#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from
the contents of the web_static folder of your
AirBnB Clone repo, using the function do_pack"""


def do_pack():
    """generates a .tgz archive from
    the contents of the web_static"""

    from fabric.api import local
    from datetime import datetime

    try:
        local("mkdir -p versions")

        date = datetime.now().strftime("%Y%m%d%H%M%S")
        path = "versions/web_static_" + date + ".tgz"
        local("tar -cvzf {} web_static".format(path))
        return path

    except Exception:
        return None

"""
Environmental Switching Code:

    Assumptions here are that EFS is essentially a key to map off of
"""

from subprocess import Popen, PIPE

ENV = {
    "local": {"file_system_id": "fs-999BOGUS", "tools_path": ".."},  # used for testing
    "dev": {"file_system_id": "fs-203cc189"},
    "prod": {"file_system_id": "fs-75bc4edc"},
}


def df():
    """Gets df output"""

    p = Popen("df", stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    if rc == 0:
        return output
    return rc, err


def get_amazon_path(dfout):
    """Grab the amazon path out of a disk mount"""

    for line in dfout.split():
        if "amazonaws" in line:
            return line
    return False


def get_env_efsid(local=False):
    """Parses df to get env and efs id"""

    if local:
        return ("local", ENV["local"]["file_system_id"])
    dfout = df()
    path = get_amazon_path(dfout)
    for key, value in ENV.items():
        env = key
        efsid = value["file_system_id"]
        if path:
            if efsid in path:
                return (env, efsid)
    return False


def main():
    env, efsid = get_env_efsid()
    print "ENVIRONMENT: %s | EFS_ID: %s" % (env, efsid)


if __name__ == "__main__":
    main()

import json
import os
import sys

from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

if len(sys.argv) > 1:
    hostname = sys.argv[1]
else:
    hostname = 'localhost'

if ('--ssl' in sys.argv):
    ssl = "True"
else:
    ssl = "False"

kernel_json = {"argv": [sys.executable, "-m", "cqljupyter", "-f", "{connection_file}"],
               "display_name": "CQL",
               "language": "CQL",
               "codemirror_mode": "sql",
               "env": {"CASSANDRA_HOSTNAME": hostname, "SSL": ssl}
               }


def install_my_kernel_spec(user=True, ssl=False):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        # TODO: Copy resources once they're specified

        print(f'Installing IPython kernel spec to connect to cassandra host {hostname} ssl={ssl}')
        install_kernel_spec(td, 'CQL', user=user, replace=True)


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # assume not an admin on non-Unix platforms


def main(argv):
    user = '--user' in argv or not _is_root()
    ssl = '--ssl' in argv
    install_my_kernel_spec(user=user, ssl=ssl)


if __name__ == '__main__':
    main(argv=sys.argv)

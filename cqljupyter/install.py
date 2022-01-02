import os
import sys
import json
import argparse

from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

kernel_json = {"argv": [sys.executable, "-m", "cqljupyter", "-f", "{connection_file}"],
               "display_name": "CQL",
               "language": "CQL",
               "codemirror_mode": "sql",
               "env" : {}
               }


def install_my_kernel_spec(user=True):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        # TODO: Copy resources once they're specified

        install_kernel_spec(td, 'CQL', user=user, replace=True)


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # assume not an admin on non-Unix platforms


def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?')
    parser.add_argument('port', nargs='?')
    parser.add_argument('-u', type=str)
    parser.add_argument('-p', type=str)
    parser.add_argument('--ssl', action='store_true')
    args = parser.parse_args()

    kernel_json['env']['CASSANDRA_SSL']=str(args.ssl)
    if (args.host):
        kernel_json['env']['CASSANDRA_HOSTNAME']=args.host
    if (args.port):
        kernel_json['env']['CASSANDRA_PORT']=args.port
    if (args.u):
        kernel_json['env']['CASSANDRA_USER']=args.u
    if (args.p):
        kernel_json['env']['CASSANDRA_PWD']=args.p

    user = args.u if args.u else not _is_root()
    print(f'Installing IPython kernel spec to connect to cassandra ', kernel_json['env'])

    install_my_kernel_spec(user=user)


if __name__ == '__main__':
    main(argv=sys.argv)

A Jupyter kernel for the Apache Cassandra Database

To install::

    pip install cql_kernel
    python -m cql_kernel.install

To use it, run one of::

    ipython notebook
    # In the notebook interface, select CQL from the 'New' menu
    ipython qtconsole --kernel cql
    ipython console --kernel cql

To set the connection hostname:

either set the enviroment variable::

    CASSANDRA_HOSTNAME=<hostname>

Or in the kernel.json file for the cql kernel, set it as an env. To find the file type::

    ﻿jupyter kernelspec list

Below is a sample kernel.json with CASSANDRA_HOSTNAME set::

﻿{"argv": ["/usr/bin/python", "-m", "cql_kernel", "-f", "{connection_file}"], "codemirror_mode": "sql", "display_name": "CQL", "env": {"CASSANDRA_HOST": "mycluster"}, "language": "CQL"}


For details of how this works, see the Jupyter docs on `wrapper kernels
<http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html>`_, and
Pexpect's docs on the `replwrap module
<http://pexpect.readthedocs.org/en/latest/api/replwrap.html>`_

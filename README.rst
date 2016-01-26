A Jupyter kernel for the Apache Cassandra Database

To install::

    pip install cql_kernel
    python -m cql_kernel.install  [<cassandra hostname>]

You can always rerun the the above command to change the hostname.  It's best to restart Jupyter after running it.
You can get away with closing your notebook, and then refreshing the main Jupyter page too, but that's error-prone.

To use it, run one of::

    ipython notebook
    # In the notebook interface, select CQL from the 'New' menu
    ipython qtconsole --kernel cql
    ipython console --kernel cql


For details of how this works, see the Jupyter docs on `wrapper kernels
<http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html>`_, and
Pexpect's docs on the `replwrap module
<http://pexpect.readthedocs.org/en/latest/api/replwrap.html>`_

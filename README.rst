A simple IPython kernel for bash

This requires IPython 3.

To install::

    pip install cql_kernel
    python -m cql_kernel.install

To use it, run one of:

    ipython notebook
    # In the notebook interface, select CQL from the 'New' menu
    ipython qtconsole --kernel cql
    ipython console --kernel cql

For details of how this works, see the Jupyter docs on `wrapper kernels
<http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html>`_, and
Pexpect's docs on the `replwrap module
<http://pexpect.readthedocs.org/en/latest/api/replwrap.html>`_

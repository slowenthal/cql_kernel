A Jupyter kernel for the Apache Cassandra Database

To install::

    pip install cqljupyter
    python -m cqljupyter.install  [<cassandra hostname>]

You can always rerun the the above command to change the hostname.  It's best to restart Jupyter after running it.
You can get away with closing your notebook, and then refreshing the main Jupyter page too, but that's error-prone.

To use it, run one of::

    jupyter notebook
    # In the notebook interface, select CQL from the 'New' menu
    jupyter qtconsole --kernel cql
    jupyter console --kernel cql

Syntax
======

All regular cqlsh syntax is supported.

Auto-complete
-------------

Use the <TAB> key to invoke auto-complete

%%html magic
------------

If you start a cell with %%html, the html will be returned and rendered

For details of how this works, see the Jupyter docs on `wrapper kernels
<http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html>`_, and
Pexpect's docs on the `replwrap module
<http://pexpect.readthedocs.org/en/latest/api/replwrap.html>`_

How to Build::

    python setup.py sdist


Implementation Notes
====================

1. The subdirectory cqlshlib has been copied directly from
`cassandra-3.11/pylib/cqlshlib
<https://github.com/apache/cassandra/tree/cassandra-3.11/pylib/cqlshlib>`_

2. cqlsh.py is copied from

https://github.com/apache/cassandra/blob/cassandra-3.x/bin/cqlsh.py


Author
======
This package was written by Brad Schoening for Python 3. It is based upon earlier work
by Steve Lowenthal and uses the open source CQLSH library.

License
=======
This project is licensed under the terms of the
`Apache 2.0 license <https://www.apache.org/licenses/LICENSE-2.0>`_.
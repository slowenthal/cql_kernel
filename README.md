[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Downloads](https://pepy.tech/badge/cqljupyter)](https://pepy.tech/project/cqljupyer)
[![PyPI version](https://badge.fury.io/py/cqljupyter.svg)](https://badge.fury.io/py/cqljupyter)

A Jupyter kernel for the Apache Cassandra Database

To install:

    pip install cqljupyter

To configure the Cassandra host or IP address:

    python -m cqljupyter.install  [<hostname> <port>] [--ssl]

You can always rerun the above command to change the hostname. It's
best to restart Jupyter after running it. You can often get away with closing
your notebook, and then refreshing the main Jupyter page too, but that's
error-prone.

To use it:

    jupyter notebook

In the notebook interface, select **CQL** from the **New** menu

To run the sample CQL:

    jupyter notebook Sample.ipynb

Syntax
======

All regular CQL syntax is supported.

Auto-complete
-------------

Use the **TAB** key to invoke auto-complete

HTML
----

If you start a cell with **%%html**, the html will be returned and rendered

Build
=====
Build using:

    python -m build

Implementation Notes
====================

1.  The script cqlsh.py was ported from 3.11 and converted using 2to3 to python3
    syntax

    <https://github.com/apache/cassandra/blob/cassandra-3.11.10/bin/cqlsh.py>

For details of how this works, see the Jupyter docs on
* [wrapper kernels](http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html),
* [Making kernels for Jupyter](https://jupyter-client.readthedocs.io/en/stable/kernels.html)
* Pexpect's docs on the [replwrap module](http://pexpect.readthedocs.org/en/latest/api/replwrap.html)

Author
======

This package was developed by Brad Schoening for Python 3. It is based upon earlier work 
by Steve Lowenthal and uses the open source Apache Cassandra CQLSH library.

License
=======

This project is licensed under the terms of the [Apache 2.0
license](https://www.apache.org/licenses/LICENSE-2.0).

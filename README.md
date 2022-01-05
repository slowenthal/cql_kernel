[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Downloads](https://pepy.tech/badge/cqljupyter)](https://pepy.tech/project/cqljupyter)
[![PyPI version](https://badge.fury.io/py/cqljupyter.svg)](https://badge.fury.io/py/cqljupyter)

A Jupyter kernel for Apache Cassandra

To install:

    pip install cqljupyter

To configure the Cassandra host or IP address:

    python -m cqljupyter.install  [<hostname> <port>] [--ssl] [-u user] [-p password]

You can always rerun the above command to change the connection. It's best to restart Jupyter after running it. 
You can often get away with closing your notebook, and then refreshing the main Jupyter page too, but that's
error-prone.

then start the notebook:

    jupyter notebook

In the notebook interface, select **CQL** from the **New** menu

To run the sample CQL:

    jupyter notebook Sample.ipynb

Syntax
======

All standard CQL syntax is supported since this package reuses the CQLSH python module.

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

1.  The cqlsh.py script was ported from 3.11 and converted using 2to3 to python3
    syntax

    <https://github.com/apache/cassandra/blob/cassandra-3.11.10/bin/cqlsh.py>

    ToDo: upgrade to Cassandra 4.0 cqlsh

For details of how this works, see these Jupyter docs:
* [Making simple Python wrapper kernels](http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html)
* [Making kernels for Jupyter](https://jupyter-client.readthedocs.io/en/stable/kernels.html)

Author
======

This package was developed by Brad Schoening for Python 3. It is based upon earlier work 
by Steve Lowenthal and uses the open source Apache Cassandra CQLSH library.

License
=======

This project is licensed under the terms of the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0).

from setuptools import setup

setup(
    name='cql_jupyter',
    version='1.0.0',
    packages=['cqlshlib_cql_kernel', 'cqlshlib_cql_kernel.test', 'cql_kernel'],
    url='https://github.com/bschoening/cql_jupyter',
    license='Apache',
    author='Brad Schoening, Steven Lowenthal & Apache Cassandra Developers',
    install_requires = ['cassandra-driver>=3.25'],
    tests_require = ['jupyter_kernel_test','nose>=1.3.7'],
    description='CQL Kernel for Jupyter based on cqlsh'
)

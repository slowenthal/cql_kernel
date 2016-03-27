from setuptools import setup

setup(
    name='cql_kernel',
    version='3.0.1',
    packages=['cqlshlib_cql_kernel', 'cqlshlib_cql_kernel.test', 'cql_kernel'],
    url='https://github.com/slowenthal/cql_kernel',
    license='Apache',
    author='Steven Lowenthal & Apache Cassandra Developers',
    author_email='steve@datastax.com',
    tests_require = ['jupyter_kernel_test','nose>=1.3.7'],
    description='CQL Kernel for Jupyter based on cqlsh',
    package_data= {
        '':['lib/*.zip','doc/cql3/*']
    }
)

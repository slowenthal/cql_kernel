from distutils.core import setup

setup(
    name='cql_kernel',
    version='',
    packages=['cqlshlib', 'cqlshlib.test', 'cql_kernel'],
    url='',
    license='',
    author='Thomas Kluyver / Steven Lowenthal',
    author_email='steve@datastax.com',
    install_requires = ['cassandra-driver>=2.7.2'],
    tests_require = ['jupyter_kernel_test>=0.1','nose>=1.3.7'],
    description=''
)

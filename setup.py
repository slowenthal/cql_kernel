from setuptools import setup

setup(
    name='cqljupyter',
    version='0.9.8',
    packages=['cqlshlib', 'cqlshlib.test', 'cqljupyter'],
    url='https://github.com/bschoening/cqljupyter',
    license='Apache',
    author='Brad Schoening, Steven Lowenthal & Apache Cassandra Developers',
    install_requires = ['cassandra-driver>=3.25'],
    tests_require = ['jupyter_kernel_test','nose>=1.3.7'],
    description='CQL kernel for Jupyter based on Cassandra CQLSH',
    long_description='CQL kernel for Jupyter based on Cassandra 3.11.x CQLSH',
    classifiers=[
        'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" 
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',   # Again, pick a license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

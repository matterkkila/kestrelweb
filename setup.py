try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='kestrelweb',
    version='0.0.1',
    description='Kestrel Web UI',
    author='Matt Erkkila',
    author_email='matt@matterkkila.com',
    url='http://github.com/matterkkila/kestrelweb',
    install_requires=[
        'pykestrel>=0.0.6',
        'dream',
        'gevent>=0.13.5',
        'gunicorn>=0.12.1'
    ],
    setup_requires=[],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose>=0.11.4'],
    package_data={},
    zip_safe=False,
)

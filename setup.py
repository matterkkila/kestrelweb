try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='kestrelweb',
    version='0.5.0',
    description='Kestrel Web UI',
    author='Matt Erkkila',
    author_email='matt@matterkkila.com',
    url='http://github.com/matterkkila/kestrelweb',
    install_requires=[
        'decoroute>=0.8.1',
        'gevent>=0.13.6',
        'gunicorn>=0.13.4',
        'pykestrel>=0.5.1',
        'WebOb>=1.2b2',
    ],
    setup_requires=[],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={},
    zip_safe=False,
)

from setuptools import setup, find_packages

setup(
    name='openclass',
    version='0.1',
    description=('A Python library that provides a bridge to Pearson\'s OpenClass API'),
    author='Anson MacKeracher',
    author_email='anson@tophatmonocle.com',
    url='https://github.com/ClassOwl/openclass-python-api',
    packages=find_packages(),
    install_requires=['requests'],
    license='MIT License',
    keywords='openclass',
    zip_safe=True,
)
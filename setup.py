from setuptools import setup, find_packages

setup(
    name='openclass',
    version='0.1',
    description=('A Python library that provides a bridge to Pearson\'s OpenClass API'),
    author='Sam Purtill',
    author_email='sam@classowl.com',
    url='https://github.com/ClassOwl/openclass-python-api',
    packages=find_packages(),
    install_requires=['json', 'requests', 'urllib'],
    license='MIT License',
    keywords='openclass',
    zip_safe=True,
)
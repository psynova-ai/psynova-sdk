import setuptools
from distutils.core import setup

with open("README.md") as f:
    long_description = f.read()

with open("psynova/version.txt") as f:
    version = f.read().strip()

setup(
    name="psynova",
    version=version,
    description="A powerful and flexible AI agent framework in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "ai",
        "agent",
        "framework",
        "machine learning",
        "artificial intelligence",
    ],
    author="psynova-dev",
    author_email="dev@psynova.ai",
    packages=setuptools.find_packages(),
    package_data={"psynova": ["version.txt"]},
    install_requires=[
        "requests==2.31.0",
        "rich==13.9.4"
    ],
    dependency_links=[],
    python_requires=">=3.10",
    url="https://psynova.github.io/",
    entry_points={
        'console_scripts': ['psynova=psynova.__main__:main']
    }
)

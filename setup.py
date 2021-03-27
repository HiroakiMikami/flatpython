from setuptools import find_packages, setup

requires = []

extras = {
    "test": [
        "flake8",
        "autopep8",
        "black",
        "isort",
        "mypy",
        "pytest",
    ],
}

setup(
    name="flatpython",
    version="0.0.0",
    install_requires=requires,
    test_requires=extras["test"],
    extras_require=extras,
    packages=find_packages(),
)

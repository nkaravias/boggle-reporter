from setuptools import setup, find_packages

VERSION = "0.1.0"
version = "{version}"


setup(
    name="boggle_tracker",
    version=version.format(version=VERSION),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_require=["pytest-runner", "wheel", "setuptools>=68.0.0", "pip"],
    install_require=[
    ],
    tests_require=["pytest", "pytest-cov"],
    test_suite="test",
    cmdclass={
        "test": "pytest --cov=boggle_tracker --cov-report term --cov-report xml:cov.xml --junitxml=xunit-result.xml"
    },
)

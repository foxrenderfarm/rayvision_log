"""Describe our module distribution to Distutils."""
from setuptools import find_packages, setup


def parse_requirements(filename):
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


setup(
    name="rayvision_log",
    author="Shenzhen Rayvision Technology Co., Ltd",
    author_email="developer@rayvision.com",
    url="https://github.com/renderbus/rayvision_log",
    package_dir={"": "."},
    packages=find_packages("."),
    description="A Python-based API for Using Renderbus cloud rendering service.",
    entry_points={},
    install_requires=list(parse_requirements("requirements.txt")),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    package_data={"rayvision_log": ["*.yaml"]},
)

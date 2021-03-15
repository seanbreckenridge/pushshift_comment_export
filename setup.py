import io
from setuptools import setup, find_packages

requirements = ["logzero", "backoff", "requests", "click"]

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

pkg = "pushshift_comment_export"
setup(
    name=pkg,
    version="0.1.2",
    url="https://github.com/seanbreckenridge/pushshift_comment_export",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=(
        """Exports all accessible reddit comments for an account using pushshift"""
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(include=[pkg]),
    install_requires=requirements,
    package_data={pkg: ["py.typed"]},
    keywords="reddit data",
    entry_points={
        "console_scripts": ["ps_comments = pushshift_comment_export.__main__:main"]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)

import io
from setuptools import setup, find_packages

requirements = ["logzero", "backoff", "requests", "click"]

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

setup(
    name="pushshift_comment_export",
    version="0.1.0",
    url="https://github.com/seanbreckenridge/pushshift_comment_export",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=(
        """Exports all accessible reddit comments for an account using pushshift"""
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(include=["pushshift_comment_export"]),
    install_requires=requirements,
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

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jio-reboot",
    version="0.1.0",
    author="Gaurav Singh",
    author_email="hello@gauravsingh.co",
    description="A utility to reboot JioFiber router",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gauravsinghji06/router-reboot",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.3",
        "urllib3>=1.26.0",
    ],
    entry_points={
        "console_scripts": [
            "jioreboot=router_reboot.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

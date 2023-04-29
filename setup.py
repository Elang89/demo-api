import pathlib
import pkg_resources

from setuptools import setup, find_packages

# The parent directory that contains the setup.py file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Packages to install for a production version
with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="food",
    version="0.1.0",
    description="Food Automation API",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Ernesto Lang",
    author_email="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["tests.*"]),
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv",
        "uvicorn",
        "python-keycloak",
        "fastapi>=0.45.0",
        "pydantic>=1.2.0,<2.0.0",
        "starlette",
        "loguru>=0.5.1",
        "gunicorn>=20.0.4",
        "uvloop",
        "httptools",
        "h11",
        "ecdsa",
    ],
    scripts=["scripts/run.sh"],
)
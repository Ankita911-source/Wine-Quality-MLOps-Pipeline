import setuptools

__version__ = "0.0.0"

REPO_NAME = "Wine-Quality-MLOps-Project"
AUTHOR_USER_NAME = "Ankita911-source"
AUTHOR_EMAIL = "tiwariankita2610@gmail.com"
SRC_REPO = "mlProject"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)

from setuptools import setup, find_packages

with open("requirements.txt", mode="r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="SBReportGenerator",
    version="0.1.0",
    packages=find_packages(
        where="src"
    ), 
    package_dir={"": "src"},
    install_requires=requirements,
    exclude=("__pycache__",),
    description="SayBanana app user productions report generator.",
    author="Bronston Ashford",
    include_package_data=True,
    package_data={
        "SBReportGenerator": ["images/*.png", "data/user_productions_example.txt"],
    },
)

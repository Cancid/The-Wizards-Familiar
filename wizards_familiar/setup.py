from setuptools import setup, find_packages
import setuptools

with open('requirements.txt') as f:
	requirements = f.readlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
		name ="wizards-familiar-Cancid",
		version ="1.0.0",
		author ="Evan Hale",
		author_email ="efhale@gmail.com",
		description ="A Text Puzzle/Exploration Game",
		long_description = long_description,
		long_description_content_type ="text/markdown",
		url ="https://github.com/Cancid/The-Wizards-Familiar",
		classifiers =[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Topic :: Games/Entertainment :: Puzzle Games",
		],
		package_dir={"": "src"},
		packages=find_packages(where="src"),
		install_requires = requirements,
		include_package_data=True,
		python_requires=">=3.9",
)

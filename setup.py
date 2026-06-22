from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lobster-network",
    version="0.1.0",
    author="信电大虾",
    author_email="your-email@example.com",
    description="小龙虾网络：对话即创造的Agent协作网络",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/lobster-network",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
)

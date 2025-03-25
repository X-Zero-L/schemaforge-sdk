from setuptools import setup, find_packages
import os
import re


# 从版本文件中读取版本号
def get_version():
    with open("schemaforge/version.py", "r") as f:
        version_file = f.read()
    version_match = re.search(r'VERSION = ["\']([^"\']*)["\']', version_file)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("无法找到版本信息")


# 读取README文件
def get_long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="schemaforge",
    version=get_version(),
    description="SchemaForge Python SDK - AI数据结构化工具",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="SchemaForge Team",
    author_email="info@schemaforge.ai",
    url="https://github.com/X-Zero-L/schemaforge-sdk",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "mypy>=0.900",
            "isort>=5.10.0",
            "coverage>=6.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="ai, schema, pydantic, data-processing, nlp, json-schema",
    project_urls={
        "Documentation": "https://github.com/X-Zero-L/schemaforge-sdk",
        "Source": "https://github.com/X-Zero-L/schemaforge-sdk",
        "Bug Reports": "https://github.com/X-Zero-L/schemaforge-sdk/issues",
    },
) 
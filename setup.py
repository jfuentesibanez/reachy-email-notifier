"""Setup script for Reachy Email Notifier."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="reachy-email-notifier",
    version="1.0.0",
    author="Reachy Community",
    description="A cute email notification app for Reachy robots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/reachy-email-notifier",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Email",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "reachy-sdk>=1.0.0",
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-api-python-client>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "reachy-email-notifier=reachy_email_notifier.main:EmailNotifierApp.start",
        ],
    },
)

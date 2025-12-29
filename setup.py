"""Setup script for reachy-email-notifier."""
from setuptools import setup, find_packages

setup(
    name="reachy-email-notifier",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-api-python-client>=2.0.0",
    ],
    entry_points={
        "reachy_mini_apps": [
            "reachy_email_notifier = reachy_email_notifier.app:ReachyMiniEmailNotifier",
        ],
    },
)

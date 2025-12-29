"""Setup script for reachy-email-notifier."""
from setuptools import setup, find_packages

setup(
    name="reachy-email-notifier",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-api-python-client>=2.0.0",
        "pyttsx3>=2.90",
        "soundfile>=0.12.1",
        "scipy>=1.10.0",
    ],
    entry_points={
        "reachy_mini_apps": [
            "reachy_email_notifier = reachy_email_notifier.app:ReachyMiniEmailNotifier",
        ],
        "console_scripts": [
            "reachy-email-notifier = reachy_email_notifier.app:main",
        ],
    },
)

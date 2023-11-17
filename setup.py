from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tb_slack_reporter",
    author="Eloi Sans Gispert",
    version="0.0.1",
    description="Package to send tensorboard results to Slack",
    author_email="esansgis@gmail.com",
    python_requires=">=3.6",
    install_requires=["tbparse>=0.0.7", "slack-sdk>=3.24.0", "aiohttp>=3.8.6"],
    packages=find_packages(),
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
)

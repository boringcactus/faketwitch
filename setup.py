'''Sets up required dependencies to run the bot'''


from setuptools import setup, find_packages

setup(
    name="faketwitch",
    version="0.1.0",
    url="https://github.com/boringcactus/faketwitch",
    author="Melody Horn",
    author_email="melody@boringcactus.com",
    description="Pretend to be the Twitch chat API while secretly being Mixer or Youtube Live",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests", "tornado", "google-api-python-client", "google-auth-oauthlib", "google-auth", "aiofiles"]
)

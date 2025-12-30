from setuptools import setup, find_packages

setup(
    name="youtube-shorts-automation",
    version="1.0.0",
    author="Your Name",
    description="Automated YouTube Shorts Channel System",
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith('#')
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'youtube-automation=main:main',
            'youtube-scheduler=src.scheduler:start_scheduler'
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)

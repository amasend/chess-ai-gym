import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/amasend/chess-ai-gym/issues',
    'Source Code': 'https://github.com/amasend/chess-ai-gym'
}

setuptools.setup(
    name="chess_ai_gym",
    version=version,
    author="Amaedeusz Masny",
    author_email="amadeuszmasny@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'async-lichess-sdk',
        'numpy',
        'networkx',
        'pygraphviz',
        'scipy'
    ],
    url="https://github.com/amasend/chess-ai-gym",
    packages=setuptools.find_packages(exclude=["tests"]),
    license="Apache Software License",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

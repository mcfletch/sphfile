import setuptools

setuptools.setup(
    name="sphfile",
    version="1.0.3",
    url="https://github.com/mcfletch/sphfile",
    author="Mike C. Fletcher",
    author_email="mcfletch@vrplumber.com",
    description="Numpy-based NIST SPH audio-file reader",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gros_client_car",
    version="0.1.22",
    author='jax',
    author_email='ming.li@fftai.com',
    license='MIT',
    description="fourier car ctrl sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FFTAI/gros_client_py/tree/feat-car/0721",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests>=2.31.0', 'websocket-client>=1.6.2'],
    python_requires='>=3'
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gros_client",
    version="1.0.14",
    author='jax',
    author_email='ming.li@fftai.com',
    license='MIT',
    description="Fourier General Robotics OS - Client Library (python)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FFTAI/gros_client_py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests>=2.31.0', 'websocket-client>=1.6.2'],
    python_requires='>=3'
)

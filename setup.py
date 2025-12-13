from setuptools import setup, find_packages

setup(
    name="nexus_engine",
    version="3.0.0",
    packages=find_packages(),
    author="Seu Nome",
    author_email="seu@email.com",
    description="Motor de Jogo RPG Multiverso - Nexus Engine 7K",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu_usuario/nexus_engine", # Substitua pela URL do seu repositório
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

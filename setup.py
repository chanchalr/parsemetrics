from setuptools import setup, find_packages

setup(name='iterative_metrics', version='1.0',package_dir={"": "."}, 
    packages=find_packages(where="./"),  
    python_requires=">=3.7, <4",
)

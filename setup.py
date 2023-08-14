from setuptools import setup, find_packages

setup(name='iterative_metrics', version='1.0',package_dir={"": "src"}, 
    packages=find_packages(where="src"),  
    python_requires=">=3.7, <4",
)

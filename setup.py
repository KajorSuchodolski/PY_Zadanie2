from setuptools import setup, find_packages

setup(name='chase',
      version='1.0',
      packages=find_packages(include=['chase', 'chase.*']),
      python_requires='>=3',
      description='Simulation of a wolf chasing sheep',
      author='Kamila Topolska, Radoslaw Zyzik',
      )

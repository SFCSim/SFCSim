from setuptools import setup
import os
packages = ['sfcsim',
            'sfcsim.algorithms',
            'sfcsim.classes',
            'sfcsim.layout',
            'sfcsim.networks']
platforms = ["Linux", "Mac OSX", "Windows", "Unix"]
keywords = [
    "sfcsim",
    "Service Function Chain",
    "Network Function Virtualization",
    "resource allocation",
    "math",
    "heuristic algorithm"
]
classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
    ]
install_requires=["networkx>=2.4"]
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name='sfcsim',
      version='1.0',
      description='Network function virtualization resource allocation simulation tool',
      url='http://github.com/tongling/sfcsim',
      author='Xulingyi',
      author_email='xuly@bupt.edu.cn',
      classifiers=classifiers,
      long_description=long_description,
      packages =  packages,
      platforms=platforms,
      keywords=keywords,
      install_requires=install_requires,
      zip_safe=False)
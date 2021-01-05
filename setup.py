from setuptools import setup
packages =  ['sfcsim',
            'algorithms',
            'classes',
            'layout'
            'networks']
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
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
install_requires=["networkx>=2.4"],
setup(name='sfcsim',
      version='1.0',
      description='Network function virtualization resource allocation simulation tool',
      url='http://github.com/tongling/sfcsim',
      author='Xulingyi',
      author_email='xuly@bupt.edu.cn',
      classifiers=classifiers
      packages =  packages,
      platforms=platforms,
      keywords=keywords,
      install_requires=install_requires,
      zip_safe=False)
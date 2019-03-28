from pip.req import parse_requirements
from setuptools import setup, find_packages

def get_requirements(file_name):
    full_path = path.dirname(path.abspath(__file__))
    full_path = path.join(full_path, file_name)
    reqs = parse_requirements(full_path, session=False)
    return [str(ir.req) for ir in reqs]
    
requirements = get_requirements('requirements.txt')

setup(
    name='aspr',
    version='0.1.0',
    author="Karl Hornlund",
    author_email='karlhornlund@gmail.com',
    description="Exploration of a solution to the Assignment Problem (Graph Theory)",
    entry_points={
        'console_scripts': [
            'aspr_run=aspr.sim.experiment:cli',
            'aspr_spt=aspr.sim.spawntimes:cli',
            'aspr_train=aspr.model.cli:cli'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    packages=find_packages(include=['aspr']),
    test_suite='tests',
    url='https://github.com/khornlund/aspr',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)

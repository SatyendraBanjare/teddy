from setuptools import setup
setup(
    name='teddy',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'teddy=teddy:cli'
        ]
    }
)
from setuptools import setup

setup(
    name='pb_tool',
    version='0.1',
    py_modules=['pb_tool'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pb_tool=pb_tool:cli
    ''',
)

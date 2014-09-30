from setuptools import setup

setup(
    name='pb_tool',
    version='1.0a1',
    description='A tool to aid in QGIS Python plugin development',
    url='https://github.com/g-sherman/plugin_build_tool',
    author='Gary Sherman',
    author_email='gsherman@geoapt.com',
    license='GPL2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Topic :: Scientific/Engineering :: GIS'],

    keywords='QGIS PyQGIS',
    py_modules=['pb_tool'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pb_tool=pb_tool:cli
    ''',
)

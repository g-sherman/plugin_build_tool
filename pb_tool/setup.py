"""
/***************************************************************************
                             setup.py for pb_tool
                 A tool for building and deploying QGIS plugins
                              -------------------
        begin                : 2014-09-24
        copyright            : (C) 2014 by GeoApt LLC
        email                : gsherman@geoapt.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from setuptools import setup

setup(
    name='pb_tool',
    version='1.9.1',
    description='A tool to aid in QGIS Python plugin development',
    long_description='pb_tool provides commands to deploy and publish a QGIS Python plugin.',
    url='http://g-sherman.github.io/plugin_build_tool',
    author='Gary Sherman',
    author_email='gsherman@geoapt.com',
    maintainer='Gary Sherman',
    maintainer_email='gsherman@geoapt.com',
    license='GPL2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Topic :: Scientific/Engineering :: GIS'],
    keywords='QGIS PyQGIS',
    platforms=['Linux', 'Windows', 'OS X'],
    include_package_data=True,
    py_modules=['pb_tool'],
    install_requires=[
        'Click', 
        'Sphinx',
        'colorama'
    ],
    entry_points='''
        [console_scripts]
        pb_tool=pb_tool:cli
    ''',
)

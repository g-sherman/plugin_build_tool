__author__ = 'gsherman'
import os
import sys
import subprocess
import zipfile
import ConfigParser

import click

@click.group()
def cli():
    pass

@cli.command()
def echo():
    """Example script."""
    click.echo('Hello World!')

@cli.command()
def deploy():
    """Deploy the plugin using parameters in pb_tool.cfg"""
    # check for the config file
    if not os.path.exists('pb_tool.cfg'):
        click.echo("Configuration file pb_tool.cfg is missing.")
    else:
        # compile to make sure everything is fresh
        compile_files()
        click.echo('Deploying it')
        # get the cfg
        cfg = config()
        python_files = cfg.get('files', 'python_files').split()
        main_dialog = cfg.get('files', 'main_dialog').split()
        compiled_ui_files = cfg.get('files', 'compiled_ui_files').split()
        extras = cfg.get('files', 'extras').split()
        # merge the file lists
        install_files = python_files + main_dialog + compiled_ui() + compiled_resource() + extras
        click.echo(install_files)


@cli.command()
def dclean():
    """ Remove the deployed plugin from the .qgis2/python/plugins directory
    """
    click.echo('Removing from .qgis2/python/plugins')

@cli.command()
def clean():
    """ Remove compiled resource and ui files
    """
    click.echo('Cleaning resource and ui files')

@cli.command()
def compile():
    """
    Compile the resource and ui files
    """
    compile_files()

@cli.command()
def doc():
    """ Build the docs using sphinx"""
    click.echo('Building the help documentation')
    if sys.platform == 'win32':
        makeprg = 'make.bat'
    else:
        makeprg = 'make'
    os.chdir('help')
    subprocess.check_call([makeprg, 'html'])

@cli.command()
def zip():
    """ Package the plugin into a zip file
    suitable for uploading to the QGIS
    Pluging repository"""

    name = config().get('plugin', 'name', None)
    if name:
        zip = zipfile.ZipFile("{}.zip".format(name), "w")
    else:
        click.echo("Your config file is missing the plugin name (name=parameter)")


def validate():
    """
    Validate existence of needed commands
    """
    pass

def config():
    """
    Read the config file pb_tools.cfg and return it
    """
    cfg = ConfigParser.ConfigParser()
    cfg.read('pb_tool.cfg')
    #click.echo(cfg.sections())
    return cfg

def compiled_ui():
    cfg = config()
    uis = cfg.get('files', 'compiled_ui_files').split()
    compiled = []
    for ui in uis:
        (base, ext) = os.path.splitext(ui)
        compiled.append('{}.py'.format(base))
    #print "Compiled UI files: {}".format(compiled)
    return compiled

def compiled_resource():
    cfg = config()
    res_files = cfg.get('files', 'resource_files').split()
    compiled = []
    for res in res_files:
        (base, ext) = os.path.splitext(res)
        compiled.append('{}_rc.py'.format(base))
    #print "Compiled resource files: {}".format(compiled)
    return compiled

def compile_files():
    # Compile all ui and resource files
    # TODO add changed detection

    ui_files = config().get('files', 'compiled_ui_files').split()
    ui_count = 0
    for ui in ui_files:
        if os.path.exists(ui):
            (base, ext) = os.path.splitext(ui)
            output = "{}.py".format(base)
            print "Compiling {} to {}".format(ui, output)
            subprocess.check_call(['pyuic4', '-o', output, ui])
            ui_count += 1
        else:
            print "{} does not exist---skipped".format(ui)
    print "Compiled {} UI files".format(ui_count)

    res_files = config().get('files', 'resource_files').split()
    res_count = 0
    for res in res_files:
        if os.path.exists(res):
            (base, ext) = os.path.splitext(res)
            output = "{}_rc.py".format(base)
            print "Compiling {} to {}".format(res, output)
            subprocess.check_call(['pyrcc4', '-o', output, res])
            res_count += 1
        else:
            print "{} does not exist---skipped".format(res)
    print "Compiled {} resource files".format(res_count)



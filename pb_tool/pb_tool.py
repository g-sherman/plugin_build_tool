__author__ = 'gsherman'
import os
import sys
import subprocess
import shutil
import errno
import glob
import ConfigParser
from string import Template


import click


@click.group()
def cli():
    """Simple Python tool to compile and deploy a QGIS plugin.
    For help on a command use --help after the command:
    pb_tool deploy --help.

    pb_tool requires a configuration file (default: pb_tool.cfg) that
    declares the files and resources used in your plugin. Plugin Builder
    2.6.0 creates a config file when you generate a new plugin template.

    See
    https://github.com/g-sherman/plugin_build_tool/blob/master/test_plugin/pb_tool.cfg
    for an example config file. You can also use the create command to generate
    a best-guess config file for an existing project, then tweak as needed."""
    pass


def get_install_files(cfg):
    python_files = cfg.get('files', 'python_files').split()
    main_dialog = cfg.get('files', 'main_dialog').split()
    extras = cfg.get('files', 'extras').split()
    # merge the file lists
    install_files = python_files + main_dialog + compiled_ui(cfg) + compiled_resource(cfg) + extras
    #click.echo(install_files)
    return install_files


@cli.command()
def version():
    """Return the version of pb_tool and exit"""
    click.echo("1.0, 2014-10-01")


@cli.command()
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def deploy(config):
    """Deploy the plugin using parameters in pb_tool.cfg"""
    deploy_files(config)


def deploy_files(config):
    """Deploy the plugin using parameters in pb_tool.cfg"""
    # check for the config file
    if not os.path.exists(config):
        click.echo("Configuration file {} is missing.".format(config))
    else:
        print """Deploying will:
        * Remove your currently deployed version
        * Compile the ui and resource files
        * Build the help docs
        * Copy everything to your .qgis2/python/plugins directory
        """

        if click.confirm("Proceed?"):

            cfg = get_config(config)
            plugin_dir = os.path.join(get_plugin_directory(), cfg.get('plugin', 'name'))
            # clean the deployment
            clean_deployment(False, config)
            print "Deploying to {}".format(plugin_dir)
            # compile to make sure everything is fresh
            print 'Compiling to make sure install is clean'
            compile_files(cfg)
            build_docs()
            install_files = get_install_files(cfg)
            # make the plugin directory if it doesn't exist
            if not os.path.exists(plugin_dir):
                os.mkdir(plugin_dir)

            fail = False
            try:
                for file in install_files:
                    print "Copying {}".format(file)
                    shutil.copy(file, os.path.join(plugin_dir, file))
                # copy extra dirs
            except OSError as oops:
                print "Error copying files: {}, {}".format(file, oops.strerror)
                fail = True
            try:
                extra_dirs = cfg.get('files', 'extra_dirs').split()
                #print "EXTRA DIRS: {}".format(extra_dirs)
                for xdir in extra_dirs:
                    print "Copying contents of {} to {}".format(xdir, plugin_dir)
                    shutil.copytree(xdir, "{}/{}".format(
                        plugin_dir, xdir))
            except OSError as oops:
                print "Error copying directory: {}, {}".format(xdir, oops.strerror)
                fail = True
            try:
                help_src = cfg.get('help', 'dir')
                help_target = os.path.join(
                    get_plugin_directory(),
                    cfg.get('plugin', 'name'),
                    cfg.get('help', 'target'))
                print "Copying {} to {}".format(help_src, help_target)
                shutil.copytree(help_src, help_target)
            except OSError as oops:
                print "Error copying help files: {}, {}".format(help_src, oops.strerror)
                fail = True
            if fail:
                print "\nOne or more files/directories failed to deploy."
                print "To ensure proper deployment, try using dclean to delete"
                print "the plugin before deploying."


def clean_deployment(ask_first=True, config='pb_tool.cfg'):
    """ Remove the deployed plugin from the .qgis2/python/plugins directory
    """
    name = get_config(config).get('plugin', 'name')
    plugin_dir = os.path.join(get_plugin_directory(), name)
    if ask_first:
        proceed = click.confirm('Delete the deployed plugin from {}?'.format(plugin_dir))
    else:
        proceed = True

    if proceed:
        click.echo('Removing plugin from {}'.format(plugin_dir))
        try:
            shutil.rmtree(plugin_dir)
            return True
        except OSError as oops:
            print 'Plugin was not deleted: {}'.format(oops.strerror)
    else:
        click.echo('Plugin was not deleted')
    return False


@cli.command()
def clean_docs():
    """
    Remove the built HTML help files from the build directory
    """
    if os.path.exists('help'):
        click.echo('Removing built HTML from the help documentation')
        if sys.platform == 'win32':
            makeprg = 'make.bat'
        else:
            makeprg = 'make'
        cwd = os.getcwd()
        os.chdir('help')
        subprocess.check_call([makeprg, 'clean'])
        os.chdir(cwd)
    else:
        print "No help directory exists in the current directory"


@cli.command()
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def dclean(config):
    """ Remove the deployed plugin from the .qgis2/python/plugins directory
    """
    clean_deployment(True, config)


@cli.command()
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def clean(config):
    """ Remove compiled resource and ui files
    """
    cfg = get_config(config)
    files = compiled_ui(cfg) + compiled_resource(cfg)
    click.echo('Cleaning resource and ui files')
    for file in files:
        try:
            os.unlink(file)
            print "Deleted: {}".format(file)
        except OSError as oops:
            print "Couldn't delete {}: {}".format(file, oops.strerror)


@cli.command()
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def compile(config):
    """
    Compile the resource and ui files
    """
    compile_files(get_config(config))


@cli.command()
def doc():
    """ Build HTML version of the help files using sphinx"""
    build_docs()


def build_docs():
    """ Build the docs using sphinx"""
    if os.path.exists('help'):
        click.echo('Building the help documentation')
        if sys.platform == 'win32':
            makeprg = 'make.bat'
        else:
            makeprg = 'make'
        cwd = os.getcwd()
        os.chdir('help')
        subprocess.check_call([makeprg, 'html'])
        os.chdir(cwd)
    else:
        print "No help directory exists in the current directory"


@cli.command()
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def zip(config):
    """ Package the plugin into a zip file
    suitable for uploading to the QGIS
    plugin repository"""

    confirm = click.confirm('Do a dclean and deploy first?')
    if confirm:
        clean_deployment(False, config)
        deploy_files(config)

    name = get_config(config).get('plugin', 'name', None)
    confirm = click.confirm(
        'Create a packaged plugin ({}.zip) from the deployed files?'.format(name))
    if confirm:
        # delete the zip if it exists
        if os.path.exists('{}.zip'.format(name)):
            os.unlink('{}.zip'.format(name))
        if name:
            cwd = os.getcwd()
            os.chdir(get_plugin_directory())
            subprocess.check_call(['zip', '-r',
                                   os.path.join(cwd, '{}.zip'.format(name)),
                                   name])

            print ('The {}.zip archive has been created in the current directory'.format(name))
        else:
            click.echo("Your config file is missing the plugin name (name=parameter)")


@cli.command()
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def validate(config):
    """
    Check the pb_tool.cfg file for mandatory sections/files
    """
    valid = True
    cfg = get_config(config)
    if not check_cfg(cfg, 'plugin', 'name'):
        valid = False
    if not check_cfg(cfg, 'files', 'python_files'):
        valid = False
    if not check_cfg(cfg, 'files', 'main_dialog'):
        valid = False
    if not check_cfg(cfg, 'files', 'resource_files'):
        valid = False
    if not check_cfg(cfg, 'files', 'extras'):
        valid = False
    if not check_cfg(cfg, 'help', 'dir'):
        valid = False
    if not check_cfg(cfg, 'help', 'target'):
        valid = False

    if valid:
        print "Your {} file is valid and contains all mandatory items".format(config)
    else:
        print "Your {} file is invalid".format(config)


@cli.command()
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def list(config):
    """ List the contents of the configuration file """
    if os.path.exists(config):
        with open(config) as cfg:
            for line in cfg:
                print line[:-1]
    else:
        print "There is no {} file in the current directory".format(config)
        print "We can't do anything without it"


@cli.command()
@click.option('--name', default='pb_tool.cfg',
              help='Name of the config file to create if other than pb_tool.cfg')
def create(name):
    """
    Create a config file based on source files in the current directory
    """
    template = Template(config_template())
    # guess the plugin name
    try:
        metadata = ConfigParser.ConfigParser()
        metadata.read('metadata.txt')
        cfg_name = metadata.get('general', 'name')
    except ConfigParser.NoOptionError as oops:
        print oops.message
    except ConfigParser.NoSectionError as secoops:
        print secoops.message
        #print "Missing section '{}' when looking for option '{}'".format(
        print "Unable to get the name of your plugin from metadata.txt"
        cfg_name = click.prompt("Name of the plugin:")

    # get the list of python files
    py_files = glob.glob('*.py')
    print py_files
    # guess the main dialog ui file
    main_dlg = glob.glob('*_dialog_base.ui')

    # get the other ui files
    other_ui = glob.glob('*.ui')
    # remove the main dialog file
    try:
        other_ui.remove(main_dlg)
    except:
        # don't care if we didn't find it
        pass

    # get the resource files (.qrc)
    resources = glob.glob("*.qrc")

    extras = glob.glob('*.png') + glob.glob('metadata.txt')

    cfg = template.substitute(Name=cfg_name,
                              PythonFiles=' '.join(py_files),
                              MainDialog=' '.join(main_dlg),
                              CompiledUiFiles=' '.join(other_ui),
                              Resources=' '.join(resources),
                              Extras=' '.join(extras))

    fname = name
    if os.path.exists(fname):
        confirm = click.confirm('{} exists. Overwrite?'.format(name))
        if not confirm:
            fname = click.prompt('Enter a name for the config file:')

    with open(fname, 'w') as f:
        f.write(cfg)

    print "Created new config file in {}".format(fname)


def check_cfg(cfg, section, name):
    try:
        cfg.get(section, name)
        return True
    except ConfigParser.NoOptionError as oops:
        print oops.message
    except ConfigParser.NoSectionError:
        print "Missing section '{}' when looking for option '{}'".format(
              section, name)
    return False


def get_config(config='pb_tool.cfg'):
    """
    Read the config file pb_tools.cfg and return it
    """
    if os.path.exists(config):
        cfg = ConfigParser.ConfigParser()
        cfg.read(config)
        #click.echo(cfg.sections())
        return cfg
    else:
        print "There is no {} file in the current directory".format(config)
        print "We can't do anything without it"
        sys.exit(1)


def compiled_ui(cfg):
    #cfg = get_config(config)
    try:
        uis = cfg.get('files', 'compiled_ui_files').split()
        compiled = []
        for ui in uis:
            (base, ext) = os.path.splitext(ui)
            compiled.append('{}.py'.format(base))
        #print "Compiled UI files: {}".format(compiled)
        return compiled
    except ConfigParser.NoSectionError as oops:
        print oops.message
        sys.exit(1)


def compiled_resource(cfg):
    #cfg = get_config(config)
    try:
        res_files = cfg.get('files', 'resource_files').split()
        compiled = []
        for res in res_files:
            (base, ext) = os.path.splitext(res)
            compiled.append('{}_rc.py'.format(base))
        #print "Compiled resource files: {}".format(compiled)
        return compiled
    except ConfigParser.NoSectionError as oops:
        print oops.message
        sys.exit(1)


def compile_files(cfg):
    # Compile all ui and resource files
    # TODO add changed detection
    #cfg = get_config(config)

    ui_files = cfg.get('files', 'compiled_ui_files').split()
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

    res_files = cfg.get('files', 'resource_files').split()
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


def copy(source, destination):
    """Copy files recursively.

    Taken from: http://www.pythoncentral.io/
                how-to-recursively-copy-a-directory-folder-in-python/

    :param source: Source directory.
    :type source: str

    :param destination: Destination directory.
    :type destination: str

    """
    try:
        shutil.copytree(source, destination)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(source, destination)
        else:
            print('Directory not copied. Error: %s' % e)


def get_plugin_directory():
    if sys.platform == 'win32':
        home = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
    else:
        home = os.environ['HOME']
    qgis2 = os.path.join('.qgis2', 'python', 'plugins')

    return os.path.join(home, qgis2)


def config_template():
    """
    :return: the template for a pb_tool.cfg file
    """
    template = """# Configuration file for plugin builder tool
# Sane defaults for your plugin generated by the Plugin Builder are
# already set below.
#
# As you add Python source files and UI files to your plugin, add
# them to the appropriate [files] section below.

[plugin]
# Name of the plugin. This is the name of the directory that will
# be created in .qgis2/python/plugins
name: $Name

[files]
# Python  files that should be deployed with the plugin
python_files: $PythonFiles

# The main dialog file that is loaded (not compiled)
main_dialog: $MainDialog

# Other ui files for your dialogs (these will be compiled)
compiled_ui_files: $CompiledUiFiles

# Resource file(s) that will be compiled
resource_files: $Resources

# Other files required for the plugin
extras: $Extras

# Other directories to be deployed with the plugin.
# These must be subdirectories under the plugin directory
extra_dirs:


[help]
# the built help directory that should be deployed with the plugin
dir: help/build/html
# the name of the directory to target in the deployed plugin
target: help
"""
    return template

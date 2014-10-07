Plugin Build Tool - pb_tool
============================
http://g-sherman.github.io/plugin_build_tool

Python command line tool for compiling and deploying QGIS plugins on all OS platforms.


## Features

*pb_tool* provides commands to aid in developing, testing, and deploying
a QGIS Python Plugin:

* Compile resource and UI files
* Deploy to your plugins directory for testing in QGIS
* Create a zip file for upload to a repository
* Clean both compiled and deployed files
* Build and clean documentation
* Build translation files
* Works on Windows, OS X, and Linux

##Installation
You can install the tool using pip:

    pip install pb_tool

To upgrade to the latest version, use:

    pip install --upgrade pb_tool

You can also install using easy_install:

    easy_install pb_tool

For information on getting setup to develop on Windows, see:
[The Almost Complete Guide to Getting Started with PyQGIS on Windows](http://spatialgalaxy.net/the-almost-complete-guide-to-getting-started-with-pyqgis-on-windows)

##Usage

*pb_tool* requires a configuration file in order to do anything. By default,
*pb_tool* assumes a file name of pb_tool.cfg, although you can specify a
different one using the ``--config`` options in most commands.

To display the available commands, just enter `pb_tool` on the command line:


    $ pb_tool
    Usage: pb_tool [OPTIONS] COMMAND [ARGS]...

      Simple Python tool to compile and deploy a QGIS plugin. For help on a
      command use --help after the command: pb_tool deploy --help.

      pb_tool requires a configuration file (default: pb_tool.cfg) that declares
      the files and resources used in your plugin. Plugin Builder 2.6.0 creates
      a config file when you generate a new plugin template.

      See http://g-sherman.github.io/plugin_build_tool for for an example config
      file. You can also use the create command to generate a best-guess config
      file for an existing project, then tweak as needed.

    Options:
      --help  Show this message and exit.

    Commands:
      clean       Remove compiled resource and ui files
      clean_docs  Remove the built HTML help files from the...
      compile     Compile the resource and ui files
      create      Create a config file based on source files in...
      dclean      Remove the deployed plugin from the...
      deploy      Deploy the plugin to QGIS plugin directory...
      doc         Build HTML version of the help files using...
      list        List the contents of the configuration file
      translate   Build translations using lrelease.
      validate    Check the pb_tool.cfg file for mandatory...
      version     Return the version of pb_tool and exit
      zip         Package the plugin into a zip file suitable...


##Command Help

Here is the help for a few of the commands, as reported using the --help option:

###Compile

    $ pb_tool compile --help
    Usage: pb_tool compile [OPTIONS]

      Compile the resource and ui files

    Options:
      --config TEXT  Name of the config file to use if other than pb_tool.cfg
      --help         Show this message and exit.


###Clean Deployment
    $ pb_tool dclean --help
    Usage: pb_tool dclean [OPTIONS]

      Remove the deployed plugin from the .qgis2/python/plugins directory

    Options:
      --config TEXT  Name of the config file to use if other than pb_tool.cfg
      --help         Show this message and exit.
**Note**: Confirmation is required to remove the plugin

###Clean Compiled Files
    $ pb_tool clean --help
    Usage: pb_tool clean [OPTIONS]

      Remove compiled resource and ui files

    Options:
      --config TEXT  Name of the config file to use if other than pb_tool.cfg
      --help         Show this message and exit.

###Deploy
    $ pb_tool deploy --help
    Usage: pb_tool deploy [OPTIONS]

      Deploy the plugin using parameters in pb_tool.cfg

    Options:
      --config TEXT  Name of the config file to use if other than pb_tool.cfg
      --help         Show this message and exit.
**Note**: Confirmation is required before deploying as it removes the current version.

###Zip
    $ pb_tool zip --help
    Usage: pb_tool zip [OPTIONS]

      Package the plugin into a zip file suitable for uploading to the QGIS
      plugin repository

    Options:
      --config TEXT  Name of the config file to use if other than pb_tool.cfg
      --help         Show this message and exit.

**Note**: To get a clean package for upload to a repository, the zip command
suggests doing a `dclean` and `deploy` first.

###Creating a Config File for an Existing Project
You can create a config file for an existing plugin project by changing to the
directory containing the plugin source and using `pb_tool create`:

    $ pb_tool create --help
    Usage: pb_tool create [OPTIONS]

      Create a config file based on source files in the current directory

    Options:
      --name TEXT  Name of the config file to create if other than pb_tool.cfg
      --help       Show this message and exit.

Once the config file is created you can try `deploy` to see if it
picked up everything needed for your plugin---or open it in your
favorite text editor to tweak it as needed. The config file is annotated
and should be self-explanatory.

####Sample Config

    # Sane defaults for your plugin generated by the Plugin Builder are
    # already set below.
    # 
    # As you add Python source files and UI files to your plugin, add
    # them to the appropriate [files] section below.

    [plugin]
    # Name of the plugin. This is the name of the directory that will
    # be created in .qgis2/python/plugins
    name: TestPlugin

    [files]
    # Python  files that should be deployed with the plugin
    python_files: __init__.py test_plugin.py test_plugin_dialog.py 

    # The main dialog file that is loaded (not compiled)
    main_dialog: test_plugin_dialog_base.ui

    # Other ui files for dialogs you create (these will be compiled)
    compiled_ui_files: foo.ui

    # Resource file(s) that will be compiled
    resource_files: resources.qrc

    # Other files required for the plugin
    extras: icon.png metadata.txt

    # Other directories to be deployed with the plugin.
    # These must be subdirectories under the plugin directory
    extra_dirs: i18n

    # ISO code(s) for any locales (translations), separated by spaces.
    # Corresponding .ts files must exist in the i18n directory
    locales: af

    [help]
    # the built help directory that should be deployed with the plugin
    dir: help/build/html
    # the name of the directory to target in the deployed plugin 
    target: help



##Deploying

    Use ``pb_tool deploy`` to build your plugin and copy it
    to qgis2/python/plugins`` in your HOME directory:


    pb_tool deploy
    Deploying will:
                * Remove your currently deployed version
                * Compile the ui and resource files
                * Build the help docs
                * Copy everything to your .qgis2/python/plugins directory

    Proceed? [y/N]: y
    Removing plugin from /Users/gsherman/.qgis2/python/plugins/TestPlugin
    Deploying to /Users/gsherman/.qgis2/python/plugins/TestPlugin
    Compiling to make sure install is clean
    Skipping foo.ui (unchanged)
    Compiled 0 UI files
    Skipping resources.qrc (unchanged)
    Compiled 0 resource files
    Building the help documentation
    sphinx-build -b html -d build/doctrees   source build/html
    Running Sphinx v1.2b1
    loading pickled environment... done
    building [html]: targets for 0 source files that are out of date
    updating environment: 0 added, 0 changed, 0 removed
    looking for now-outdated files... none found
    no targets are out of date.

    Build finished. The HTML pages are in build/html.
    Copying __init__.py
    Copying test_plugin.py
    Copying test_plugin_dialog.py
    Copying test_plugin_dialog_base.ui
    Copying foo.py
    Copying resources_rc.py
    Copying icon.png
    Copying metadata.txt
    Copying help/build/html to /Users/gsherman/.qgis2/python/plugins/TestPlugin/help



##What's Missing

* `pb_tool` currently doesn't support running tests for your plugin.
* Probably other things we haven't thought of...

##Why?
Why create a build tool when `make` using the Makefile generated by the
Plugin Builder plugin generally works? Here are some reasons:

* `pb_tool` lets you create configs for plugins that were not created using the
  Plugin Builder plugin
* The Makefile doesn't work completely on Windows in all cases
* Writing a command line tool is fun..

##Contributing
Issues and pull requests can be submitted here:
* https://github.com/g-sherman/plugin_build_tool

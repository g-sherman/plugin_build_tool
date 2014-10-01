Plugin Build Tool
=================

Pure Python command line tool for compiling and deploying QGIS plugins on all OS platforms.

## Features

*pb_tool* provides commands to aid in developing, testing, and deploying
a QGIS Python Plugin:

* Compile resource and UI files
* Deploy to your plugins directory for testing in QGIS
* Create a zip file for upload to a repository
* Clean both compiled and deployed files
* Build and clean documentation
* Works on Windows, OS X, and Linux

##Installation
You can install the tool using pip:

    pip install pb_tool

To upgrade to the latest version, use:

    pip install --upgrade pb_tool

You can also install using easy_install:

    easy_install pb_tool

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

      See https://github.com/g-sherman/plugin_build_tool/blob/master/test_plugin
      /pb_tool.cfg for an example config file. You can also use the create
      command to generate a best-guess config file for an existing project, then
      tweak as needed.

    Options:
      --help  Show this message and exit.

    Commands:
      clean       Remove compiled resource and ui files
      clean_docs  Remove the built HTML help files from the...
      compile     Compile the resource and ui files
      create      Create a config file based on source files in...
      dclean      Remove the deployed plugin from the...
      deploy      Deploy the plugin using parameters in...
      doc         Build HTML version of the help files using...
      list        List the contents of the configuration file
      validate    Check the pb_tool.cfg file for mandatory...
      version     Return the version of pb_tool and exit
      zip         Package the plugin into a zip file suitable...

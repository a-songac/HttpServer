'''
Generate Argument Parsers for the server

@author: arno
'''

import argparse

def generateArgParsers():
    parser = argparse.ArgumentParser(
            description="httpfs is a simple file server.")
    
    parser.add_argument('-v',
                              dest="isVerbose",
                              action="store_const", const=True, default=False,
                              help="Prints debugging messages.")

    parser.add_argument('-p',
                              dest="port",
                              action="store",
                              metavar="PORT",
                              type=int,
                              default=8080,
                              help="Specifies the port number that the server will listen and serve at.")

    parser.add_argument('-d',
                              dest="homeDir",
                              action="store",
                              metavar="PATH-TO-DIR",
                              default=".",
                              help="Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.")

    return parser
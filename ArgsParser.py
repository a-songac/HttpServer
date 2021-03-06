'''
Generate Argument Parsers for the server

@author: arno
'''
import os
import argparse
HOME_DIR = os.getcwd()

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
                              default=HOME_DIR,
                              help="Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.")
    parser.add_argument('--delay-writing',
                              dest="debugMode",
                              action="store_const", const=True, default=False,
                              help="Debug mode where writing operation has a delay. Used to test concurrency")

    return parser
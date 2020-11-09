from common import *
import argparse

parser = argparse.ArgumentParser(description='Counts the number of joints used in a mot XML file')
parser.add_argument('filename', type=str, help='The path of the mot XML file')
args = parser.parse_args()
mot = loadMotXML(args.filename)
print('Joint count (%s): %d' % (args.filename, len(mot.Joints)))
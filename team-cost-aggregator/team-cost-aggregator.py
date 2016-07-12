import imp,argparse
import os,sys
import json,yaml
import pprint

# project modules
import output

def readConfigFile(path):
    configMap = []

    try:
        config_file_handle = open(path)
        configMap = yaml.load(config_file_handle)
        config_file_handle.close()
    except:
        print "Error: Unable to open config file %s or invalid yaml" % path

    return configMap

## mainFile
def main(argv):

    # Add our folder to the system path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    parser = argparse.ArgumentParser(description='Report on AWS costs by team')
    parser.add_argument('-d','--debug', help='Enable debug output',action='store_true')
    parser.add_argument('-c','--config', help='Full path to a config file',required=True)
    parser.add_argument('-f','--folder', help='Folder containing the team cost summaries',required=True)
    args = parser.parse_args()

    configMap = readConfigFile(args.config)

    if configMap:
        print "Outputing results using data in folder %s" % args.folder

        # Output the results for the run of each plugin
        output.outputResults(args.folder,configMap,args.debug)

if __name__ == "__main__":
   main(sys.argv[1:])

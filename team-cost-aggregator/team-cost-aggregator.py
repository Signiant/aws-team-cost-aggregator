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
        print "Generating report using data in folder " + args.folder

        # Output the results
        output.outputResults(args.folder,configMap,args.debug)

        # Move the current output files to previous so we can report percent change
        print "Moving current output files to previous" + args.folder
        all_team_results_files = os.listdir(args.folder)
        for team_result_file in all_team_results_files:
            team_result_fullpath = os.path.join(args.folder,team_result_file)

            # Skip if we have a sub-dir
            if os.path.isdir(team_result_fullpath):
                continue
            elif str(team_result_fullpath).endswith(".prev"):
                print "Skipping processing of " + team_result_fullpath
                continue
            else:
                team_result_fullpath_prev = team_result_fullpath + ".prev"
                print "Moving " + team_result_fullpath + " to " + team_result_fullpath_prev
                os.rename(team_result_fullpath,team_result_fullpath_prev)

if __name__ == "__main__":
   main(sys.argv[1:])

import yaml
import argparse

def getArgs():
    parser=argparse.ArgumentParser(description="versions file parser")
    parser.add_argument("file_name")
    args=parser.parse_args()

    return args.file_name

def readFile(file_name):
    with open(file_name, 'r') as file:
        data = yaml.safe_load(file)
    return data

def getCmds(parsed_file):
    for svc in parsed_file['services']:
        envVarName = 'IMAGE_' + svc.upper()
        print("{}={}".format(envVarName, parsed_file['services'][svc]['version']))

if __name__ == "__main__":
   file_name = getArgs()
   parsed_file = readFile(file_name)
   getCmds(parsed_file)
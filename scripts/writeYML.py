import yaml
import argparse
import os

def getArgs():
    parser=argparse.ArgumentParser(description="versions file parser")
    parser.add_argument("file_name")
    args=parser.parse_args()

    return args.file_name

def readFile(file_name):
    with open(file_name, 'r') as file:
        data = yaml.safe_load(file)
    return data

def setVersions(parsed_file):
    for svc in parsed_file['services']:
        envVarName = svc.upper() + '_IMAGE'
        parsed_file['services'][svc]['version'] = os.environ[envVarName]

    return parsed_file

def writeFile(file_name, data):
    # print("Data:  {}".format(data))
    with open(file_name, 'w') as file:
        yaml.dump(data, file, sort_keys=False)

if __name__ == "__main__":
   file_name = getArgs()
   parsed_file = readFile(file_name)
   data = setVersions(parsed_file)
   writeFile(file_name, data)
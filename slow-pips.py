import subprocess, os, sys, argparse, time
from prettytable import PrettyTable
from tqdm import tqdm

# The script reads a requirments.txt file, records install time of each module 
# from it & displays a sorted table based on timings. By default, it will look 
# for requirements.txt file in current working directory, 
# -r flag can be used to override this behavior by providing a file path. 
# -f flag can be used to force reinstall of the module.

# commandline args
argParser = argparse.ArgumentParser(description='Script to get install timings of pip packages.')
argParser.add_argument('-r', '--requirments', help='requirments.txt file path', default='requirements.txt',type=str)
argParser.add_argument('-f', '--force', action='store_true', help='force reinstall of the modules')

args = argParser.parse_args()

#print(args)

pip3_cmd = ["pip3", "install"]
if args.force:
   pip3_cmd.append("--no-cache-dir")
   pip3_cmd.append("--force-reinstall")
   pip3_cmd.append("--ignore-installed")

if not os.path.isfile(args.requirments):
   print('requirements.txt does not exist. Use -h for help.')
   sys.exit(1)

# exit if pip3 doesn't exist
pip3 = subprocess.run(["command", "-v", "pip3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
if pip3.returncode != 0:
    print("pip3 not found.")
    sys.exit(1)

pip3_version = subprocess.run(["pip3", "--version"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
print("Using", str(pip3_version.stdout, 'utf-8'))

# create table to store install data
result_table = PrettyTable(["Module", "Time", "time_sec"])
total_time = 0

# load modules from requirments.txt into a list
modules = []
with open(args.requirments) as f:
    modules = f.read().replace(" ","").splitlines()

print("Analyzing {} dependencies...".format(len(modules)))

# iterate through each module and measure install time
for module in tqdm(modules):
    start = time.time()
    result = subprocess.run( pip3_cmd + [module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time()
    elapsed_time = end - start
    install_time = time.strftime("%Mm %Ss", time.gmtime(elapsed_time))
    total_time = total_time + elapsed_time
    if result.returncode == 0:
        result_table.add_row([module, install_time, elapsed_time])
    else:
        result_table.add_row([module, install_time + "(F)", elapsed_time])


# print results
print("Results")
print(result_table.get_string(sortby="time_sec", reversesort=True, fields=["Module", "Time"]))
print("Total Time Taken: {}".format(time.strftime("%Mm %Ss", time.gmtime(total_time))))
print("(F) in table represents failed installation.")
print("test connection")

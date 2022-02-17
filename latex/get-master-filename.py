import sys


if len(sys.argv) < 2:
    print("Requires 1 argument: current tex file")
    exit(1)

current_filename = sys.argv[1]
master_filename = current_filename.split('/')[-1]

f = open(current_filename)
for line in f:
    if '%%% TeX-master:' in line:
        elements = line.split('\"')
        if len(elements) == 3 and elements[1] != "":
            master_filename = elements[1] + ".tex"

sys.stdout.write(master_filename)
sys.stdout.flush()
sys.exit(0)
        



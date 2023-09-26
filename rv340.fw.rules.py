## this script will parse thru the exported config file from a Cisco RV340 Firewall and export the firewall rules into a CSV file
## usage: python3 fw.rules.py -F /path/to/ConfigFile.xml

## update output file location here
outputFile = "/tmp/out.csv"
#
import os,sys,requests,urllib3,csv,re,time,pdb,argparse
from xml.etree.ElementTree import fromstring, ElementTree
parser = argparse.ArgumentParser()
############################################
parser.add_argument("-v", "--verbose", help = "verbose")
parser.add_argument("-F", "--inputFile", help = "inputFile to parse")
args = parser.parse_args()
if args.verbose:
    verbose=int(args.verbose)
    if verbose >= 1:
        print("Diplaying verbose as: % s" % args.verbose)
else:
    verbose=0
if args.inputFile:
    inputFile=str(args.inputFile)
    if verbose >= 1:
        print("Diplaying inputFile as: % s" % args.inputFile)
else:
    sys.exit("no inputFile specified.  Use -F /path/to/file")
#
with open(inputFile, 'r') as f:
    dd = f.read()
dd = re.sub('xmlns.*"', '' ,dd)
tree = ElementTree(fromstring(dd))
root = tree.getroot()

x=0
for child in root:
    if "firewall-acl-rules" in str(child):
        tgt = x
    x=x+1

csv="rule-id;priority;enabled;action;service;log;source-interface;source-ip;dest-interface;dest-ip\n";x=0
for child in root[tgt][0].findall('firewall-acl-rule'):
    if verbose == 1: 
        print("root[11][0]["+str(x)+"]")
    if verbose == 1: print("rule-id: "+str(child[0].text))
    csv=csv+str(child[0].text)+";"
    if verbose == 1: print("priority: "+str(child[1].text))
    csv=csv+str(child[1].text)+";"
    if verbose == 1: print("enabled: "+str(child[2].text))
    csv=csv+str(child[2].text)+";"
    if verbose == 1: print("action: "+str(child[3][0].tag))
    csv=csv+str(child[3][0].tag)+";"
    if verbose == 1: print("service: "+str(child[4].text))
    csv=csv+str(child[4].text)+";"
    if verbose == 1: print("log: "+str(child[5].text))
    csv=csv+str(child[5].text)+";"
    if verbose == 1: print("source interface: "+str(child[6][0].text))
    csv=csv+str(child[6][0].text)+";"
    if "any" in str(child[7][0].tag):       # source-ip
        if verbose == 1: print("source IP: ANY")
        csv=csv+"ANY;"
    if "ipv4" in str(child[7][0].tag):
        if "range" in str(child[7][0][0].tag):
            start =   str(child[7][0][0][0].text)
            end = str(child[7][0][0][1].text)
            if verbose == 1: print("source-ip: "+start+" - "+end)
            csv=csv+start+" - "+end+";"
        if "subnet" in str(child[7][0][0].tag):
            subnet = str(child[7][0][0][0].text)+"/"+str(child[7][0][0][1].text)
            if verbose == 1: print("source IP: "+subnet)
            csv=csv+subnet+";"
        if "single" in str(child[7][0][0].tag):
            subnet = str(child[7][0][0].text)
            if verbose == 1: print("source IP: "+str(child[7][0][0].text))
            csv=csv+str(child[7][0][0].text)+";"
    if verbose == 1: print("dest interface: "+str(child[6][1].text))
    csv=csv+str(child[6][1].text)+";"
    if "any" in str(child[8][0].tag):       # dest-ip
        if verbose == 1: print("dest IP: ANY")
        csv=csv+"ANY\n"
    if "ipv4" in str(child[8][0].tag):
        if "range" in str(child[8][0][0].tag):
            start =   str(child[8][0][0][0].text)
            end = str(child[8][0][0][1].text)
            if verbose == 1: print("dest-ip: "+start+" - "+end)
            csv=csv+start+" - "+end+"\n"
        if "subnet" in str(child[8][0][0].tag):
            subnet = str(child[8][0][0][0].text)+"/"+str(child[8][0][0][1].text)
            if verbose == 1: print("source IP: "+subnet)
            csv=csv+subnet+";\n"
        if "single" in str(child[8][0][0].tag):
            subnet = str(child[8][0][0].text)
            if verbose == 1: print("source IP: "+str(subnet))
            csv=csv+str(child[8][0][0].text)+";\n"
    if verbose == 1: 
        print("\n")
        time.sleep(0)
    x=x+1

if os.path.exists(outputFile):
    os.remove(outputFile)
with open(outputFile, 'w') as f:
    f.write(csv)

aa = csv.split("\n")
for x in aa:
    if verbose == 1:
        print(x)
print("Done.  Data written to file "+str(outputFile)+"\n\nTo load the file in excel, open excel, go to DATA tab and click GET DATA > FROM FILE, then sort by Priority\n")

sys.exit()

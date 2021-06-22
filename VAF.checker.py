#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 19:57:59 2021

@author: lukszafron@gmail.com
"""

appname = "Variant Allele Freq. checker"
appversion = "1.0"

import re, getopt, sys, os

def usage():
    print(
        "\nWelcome to the", appname, "app.\n\n"
        "The following options are available:\n\n"
        "\t-h, --help:\tprints this help message.\n"
        "\t-f, --freq:\tthe desired Variant Allele Frequency (VAF, in percentages)\n"
        "\t-p, --path:\tthe path to a VCF file containing the FORMAT/AD taq\n"
        "\t-v, --version:\tprints the version of this program.\n"
  )

try:
        opts, args = getopt.getopt(sys.argv[1:], "h,f:,p:,v", ["help","freq=","path=","version"])
        if len(opts) == 0:
                usage()
                sys.exit()
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            elif o in ("-f", "--freq"):
                freq = a
            elif o in ("-p", "--path"):
                path = a
            elif o in ("-v", "--version"):
                print(" version: ".join((appname, appversion)))
                sys.exit()
            else:
                assert False, "Unhandled option: "+o

except getopt.GetoptError as err:
    # print help information and exit:
    print("\n",err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    
assert os.path.isfile(path), "The "+ path + " file does not exist."

try:
    freq = float(freq)/100
except:
    raise IOError("The desired allele frequency was not provided.")
        
with open(path, 'rt') as f:
    vcf = f.readlines()
    
header = [v for v in vcf if re.search(string=v, pattern="^#.*")]
values = [v for v in vcf if not re.search(string=v, pattern="^#.*")]
if len(re.findall(pattern="AD",string=values[0].split(sep = "\t")[8])) != 1:
    raise Exception("The allele depth tag (AD) was not calculated.")

adpos = [i1 for i1,val1 in enumerate(values[0].split(sep = "\t")[8].split(sep = ":")) if val1 == "AD"]
assert len(adpos) == 1, "There are multiple AD tags in this VCF file."
adpos = adpos[0]

ADs = [line.split(sep = "\t")[9].split(sep = ":")[adpos] for line in values]

refvals = list(map(int,[val.split(sep = ",")[0] for val in ADs]))
altvals = list(map(int,[val.split(sep = ",")[1] for val in ADs]))

VAFs = []
for i,refval in enumerate(refvals):
    sumval = refvals[i] + altvals[i]
    VAF = altvals[i]/sumval
    VAFs.append(VAF)

passed_values = [line for index,line in enumerate(values) if VAFs[index] >= freq]

passed_vcf = header + passed_values

print(''.join(passed_vcf).strip())
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Calculate similarity score for two json files."""

__license__ = "GPL"
__version__ = "2.0"


import sys, getopt
import json
import os

# Measure the difference based on the intersection of both sets
def XgetMatchesLen(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    #print(set1 ^ set2) # print intersection
    return (len(set1 & set2), len(set1 | set2))

# Measure the length of the set with a maximum of the smaller set
def getMatchesLen(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    if len(set1) < len(set2):
        x = set2
        set2 = set1
        set1 = x
    #print(set2 - set1) # print what is in the smaller but missing from the larger set
    return (len(set1 & set2), len(set2))

def computeSimilarity(dict1, dict2):
    totalMatches = 0.0
    totalLen = 0.0
    for comparable in ('globalvars', 'exportedfunctions', 'importedfunctions', 'importedglobals', 'dependencies'):
        (matches, length) =XgetMatchesLen(dict1[comparable], dict2[comparable])
        totalMatches = totalMatches + matches
        totalLen = totalLen + length
        print('Matches: {} length: {}'.format(matches, length))
    return totalMatches / totalLen        

if __name__ == "__main__":
    lib1 = ''
    lib2 = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:', ['file='])
    except getopt.GetOptError:
        print('Usage: ', sys.argv[0], ' -f <file1.json> -f <file2.json>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: ', sys.argv[0], ' -f <file1.json> -f <file2.json>')
            sys.exit()
        elif opt in ('-f', '--file'):
            if lib1 == '':
                lib1 = arg
            else:
                if lib2 == '':
                    lib2 = arg
                else:
                    print('Please only compare two files!')
    if lib1 == '' or lib2 == '':
        print('Usage: ', sys.argv[0], ' -f <file1.json> -f <file2.json>')
        sys.exit()
    
    # Do the magic
    dict1 = json.load(open(lib1, 'r'))
    dict2 = json.load(open(lib2, 'r'))
    score = computeSimilarity(dict1, dict2)
    print('{:25s} | {:25s} | Score:{:.2%}'.format(lib1[:-5],lib2[:-5],score))

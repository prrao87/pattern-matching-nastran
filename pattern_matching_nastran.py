"""
Script to extract relevant numerical data blocks from a large text file.
Uses pattern matching with regular expressions.

The example input data comes from a structural analysis solver "NASTRAN"
Our aim is to extract relevant force data from all "QUAD4" elements in the data set

Since NASTRAN only outputs force data in discrete blocks (of 32 lines each), we need to
store the data in memory and write it all to disk so that we can perform numerical 
calculations on the forces.

# Updated to Python version: 3.6

Created by: Prashanth Rao
Date: 03/12/2017
"""
import sys, os
import re
from math import sqrt           

def extract_data(filename, setname, lineskip):
    # Define search pattern to isolate relevant data from output
    setname = ' '.join(setname.upper())     # Convert to uppercase as per NASTRAN output
    
    # Define patterns using regex
    elt_pattern = re.compile(r'(' + setname + ')')  # Pattern: ( Q U A D 4 ) or ( T R I A 3 )
    sub_pattern = re.compile(r'SUBCASE'+'\s*=?\s*([0-9]+)') # Pattern: SUBCASE 10 or any other number
    stop_pattern = re.compile(r'[A-Z]+\s+[Nn][Aa][Ss][Tt][Rr][Aa][Nn]') # Pattern: MD/MSC/NX NASTRAN (big or small letters)
    alt_stop_pattern = re.compile(r'\*+')
    
    flag = False
    n_match = 0           # Loadcase page start number 
    subcase_repeat = [-1, -1]   # Dummy list used purely to track changes in subcase number
    
    with open(filename, "r") as file:
            it = iter(file)
            for line in it:
                if flag:                            # if flag == True
                    if stop_pattern.search(line) or alt_stop_pattern.search(line):   # if we hit a stopping pattern, stop search
                        flag = False                # Reset flag 
                    else: 
                        out.write(line)
                        # print(line)
                find = sub_pattern.search(line)
                if find:
                    f = int(find.group(1))
                if elt_pattern.search(line):
                    n_match += 1
                    subcase_repeat.append(f)    # Subcase number to track when loadcase changes
                    
                    # Store each subcase in a NEW text file, by comparing case numbers
                    if subcase_repeat[-1] != subcase_repeat[-2]:
                        out = open("output_subcase_"+str(subcase_repeat[-1])+".txt", "a")
                        # print(f"Found numerical force data for loadcase {f}")
                    
                    for _ in range(lineskip):   # Ignore the next 'lineskip' number of lines
                        next(it)
                    flag = True
            out.close()
            repeat = subcase_repeat.count(subcase_repeat[0])
    return n_match   
    
if __name__ == "__main__":
    
    filename = "test_input.f06"
    setname = "quad4"   # Say we want to pull all force data related to "quad4" elements
    lineskip = 2  # We need to skip the next 2 lines after the pattern is matched
    
    n_match = extract_data(filename, setname, lineskip)
    
    print(f"Found {n_match} data blocks of the element {setname}")
    
    

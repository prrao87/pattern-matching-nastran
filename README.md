# pattern-matching-nastran
Extract numerical force data from a text file that stores the data in discrete blocks - using regex

This is an example highlighting my use case of Python regular expressions to extract and store structured data.

The use case involves data from a specific structural solver "NASTRAN" - this solver outputs force data on finite element models. The useful data is embedded in millions of lines of extraneous information, so it is necessary to extract the data and then arrange it so that numerical computations can easily be performed on it. The problem is that the data is output in discrete blocks of 32 lines, with section breaks in between. So a slightly more complex function is required to extract, combine and arrange the force data in a machine-readable format. Hence, a combination of regex, string ops and file handling functions are used. 

The algorithm works as follows:
- Read in the data line by line, and match the pattern ```( Q U A D 4 )```, which is the type of finite element on which we want the force values. This allows us to identify the start of the relevant data block.
- Once the correct data block is identified, we need to identify the subcase number (loadcase) which this data is for. This is done by matchine the pattern ```SUBCASE #``` where "#" represents a 2 or 3 digit number.
- Then we skip 2 lines (column headers), following which the 32 lines of relevant numerical force information is read in and stored.
- Finally, we hit the end of the data block after 32 lines, which is identified by the stop pattern: ```MD/MSC/NX NASTRAN```. The exact text here depends on the type of analysis that output the data, and the exact flavor of NASTRAN used. The regex aims to generalize this information as best possible. 
- The data block that is stored in memory is then written to a file (output_subcase_#.txt).
- The next data block is identified the same way, and appended to the already open write file.
- The subcase number is tracked along with the data blocks.

The above approach makes it possible to parse through a very large text file, and store thousands of elements' worth of force data and perform custom calculations on them.

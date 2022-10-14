# assume that test file is in the same file as csv_combiner and fixtures folder
import unittest
import pandas as pd
import random
from csv_combiner import combine

# files for testing
driver = 'csv_combiner.py'
csv1 = './fixtures/accessories.csv'
csv2 = './fixtures/clothing.csv'
csv3 = './fixtures/household_cleaners.csv'

# inputs stored in each file
accessories = pd.read_csv(csv1)
clothing = pd.read_csv(csv2)
household = pd.read_csv(csv3)

# get the total rows of random combined file and the command to combine method
def randomFiles():
    rand = random.randint(4, 1000)
    print("Combine {0} files".format(rand))
    
    command = [driver]
    actual_rows = 0

    for i in range(rand):
        file = random.randint(1,3)
        if file == 1:
            command.append(csv1)
            actual_rows += len(accessories.index)-1
        elif file == 2:
            command.append(csv2)
            actual_rows += len(clothing.index)-1
        else:
            command.append(csv3)
            actual_rows += len(household.index)-1
        
    # add the header row
    actual_rows += 1
    
    return actual_rows, command

class TestCombiner(unittest.TestCase):
    # test if function throw an expected exception when no input is given
    def testValidCommandLine(self):
        print("Test command line")
        with self.assertRaises(Exception) as error:
            combine([driver])
        self.assertTrue("No input provided" in str(error.exception))
        
    # test if function throw an expected exception when given files are invalid or not found
    def testValidFiles(self):
        print("Test input files")
        # invalid file accessories.pdf
        with self.assertRaises(Exception) as error:
            combine([driver, './fixtures/accessories.pdf', csv1])
        self.assertTrue("Invalid file(s)" in str(error.exception))

        # furniture.csv not found in the folder
        with self.assertRaises(Exception) as error:
            combine([driver, './fixtures/furniture.csv', csv1, csv2])
        self.assertTrue("Invalid file(s)" in str(error.exception))

    # test if all rows are added and column = 3
    def testAddAllRows(self):
        print("Test add all rows/cols")
        print("Combine one file")
        # Case 1: one file
        actual_rows = len(accessories.index)
        df = combine([driver, csv1])
        self.assertTrue(len(df.index), actual_rows)
        self.assertTrue(len(df.columns), 3)

        print("Combine two files")
        # Case 2: combine two files
        actual_rows = len(accessories.index) + len(clothing.index) - 1
        df = combine([driver, csv1, csv2])
        self.assertTrue(len(df.index), actual_rows)
        self.assertTrue(len(df.columns), 3)

        print("Combine three files")
        # Case 3: combine three files
        actual_rows = len(accessories.index) + len(clothing.index) + len(household.index) - 2
        df = combine([driver, csv1, csv2, csv3])
        self.assertTrue(len(df.index), actual_rows)
        self.assertTrue(len(df.columns), 3)

        # Case 4: combine random number of files (up to 1000)
        actual_rows, command = randomFiles()
        df = combine(command)
        
        self.assertTrue(len(df.index), actual_rows)
        self.assertTrue(len(df.columns), 3)
        

    # check if the correct file names are added
    def testFileName(self):
        print("Test file name")
        _, command = randomFiles()
        df = combine(command)
        filenames = ['accessories.csv', 'clothing.csv', 'household_cleaners.csv']

        self.assertTrue(set(df.filename.unique()).issubset(set(filenames)))

if __name__ == '__main__':
    unittest.main()

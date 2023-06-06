import csv
import sys

def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)
    # open the txt file
    dna = open(sys.argv[2], 'r').read()
    # open the csv file
    with open(sys.argv[1], 'r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        print(hesders)
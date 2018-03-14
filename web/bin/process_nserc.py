import csv
import sys

in_csv = sys.argv[1]
out_csv = sys.argv[2]
UNIVERSITY_COLUMN = 4
UOFA = "University of Alberta"
with open(in_csv, 'r', encoding="iso-8859-1") as csv_file, open(out_csv, 'w') as csv_out:
    in_reader = csv.reader(csv_file)
    out_writer = csv.writer(csv_out)

    for row in in_reader:
        if row[UNIVERSITY_COLUMN] == UOFA:
            out_writer.writerow(row)
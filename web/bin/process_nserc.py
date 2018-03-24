import csv
import sys

in_csv = sys.argv[1]
out_csv = sys.argv[2]
NAME_COLUMN = 1
UNIVERSITY_COLUMN = 4
TITLE_COLUMN = 34
BODY_COLUMN = 36
OUT_FORMAT = [NAME_COLUMN, UNIVERSITY_COLUMN, TITLE_COLUMN, BODY_COLUMN]
UOFA = "University of Alberta"
with open(in_csv, 'r', encoding="utf-8") as csv_file, open(out_csv, 'w', encoding="utf-8") as csv_out:
    in_reader = csv.reader(csv_file)
    out_writer = csv.writer(csv_out)

    for row in in_reader:
        if row[UNIVERSITY_COLUMN] == UOFA:
            new_row = [row[i] for i in OUT_FORMAT]
            out_writer.writerow(new_row)
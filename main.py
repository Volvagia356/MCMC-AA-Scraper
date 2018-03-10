import os.path
import sys
import csv
import json

import scraper

def get_csv_writer(aa_type, columns):
    out_filename = aa_type + ".csv"
    out_path = os.path.join("out", out_filename)
    out_file = open(out_path, "w")
    out_csv = csv.DictWriter(out_file, columns)
    out_csv.writeheader()
    return out_csv

def write_csv_entries(csv_writer, entries):
    for entry in entries:
        csv_writer.writerow(entry)

def get_aa_to_csv(aa_type):
    columns = aa_types[aa_type]['columns']
    page_count = aa_types[aa_type]['page_count']

    csv_writer = get_csv_writer(aa_type, columns)
    entries = scraper.get_all_entries(aa_type, columns, page_count)
    write_csv_entries(csv_writer, entries)

with open("aa_types.json") as f:
    aa_types = json.load(f)

if __name__ == "__main__":
    aa_type = sys.argv[1]
    get_aa_to_csv(aa_type)

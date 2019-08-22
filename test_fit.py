#!/usr/bin/env python2
from fitparse import FitFile
import glob

def checkAllPossibleRecords(fitfile):
    record_ints = []
    for i in range(0, 268):
        record = fitfile.get_messages(i)
        try:
            print("{}: {}".format(i, next(record).get_values()))
            record_ints.append(i)
        except StopIteration:
            pass
    print(record_ints)
    print("\n\n")

def checkCurrentRecords(fitfile):
    for record in fitfile.get_messages():
        if record.name not in records:
            records.add(record.name)
        if record.name not in record_names:
            record_names[record.name] = set()
        records.add(record.name)
        for record_data in record:
            record_names[record.name].add(record_data.name)
            if "local_timestamp" in record_data.name or "system_timestamp" in record_data.name:
                print(record.name)
            if record_data.units:
                print(" * %s: %s %s" % (record_data.name, record_data.value, record_data.units))
            else:
                print(" * %s: %s" % (record_data.name, record_data.value))

def checkSpecificField(fitfile, field):
    print("{}: {}".format(fitfile, field))
    record = fitfile.get_messages(field)
    print(dir(record))
    for record_data in record:
        print(record_data)

def main():
    print_record_data = True
    files = sorted(glob.glob('fit_files/*.fit'))
    records = set()
    record_names = {}
    for f in files:
        print(f)
        fitfile = FitFile(f)
        checkAllPossibleRecords(fitfile)
        #checkCurrentRecords(fitfile)
        checkSpecificField(fitfile, 'event')

if __name__ == "__main__":
    main()

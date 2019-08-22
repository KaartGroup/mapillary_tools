#!/usr/bin/env python2
from fitparse import FitFile
import glob
print_record_data = True
files = sorted(glob.glob('fit_files/*.fit'))
records = set()
record_names = {}
for f in files:
    print(f)
    fitfile = FitFile(f)
    for record in fitfile.get_messages():
        if record.name not in records:
            pass
        if record.name not in record_names:
            record_names[record.name] = set()
        records.add(record.name)
        for record_data in record:
            record_names[record.name].add(record_data.name)
            if "local_timestamp" in record_data.name or "system_timestamp" in record_data.name:
                print(record.name)
            if print_record_data:
                if record_data.units:
                    print(" * %s: %s %s" % (record_data.name, record_data.value, record_data.units))
                else:
                    print(" * %s: %s" % (record_data.name, record_data.value))
    for record in fitfile.get_messages(162):
        print(record.name)
    for record in fitfile.get_messages(160):
        print(record.name)
    for event in fitfile.get_messages('event'):
        event_fields = set()
        for field in event.fields:
            event_fields.add(field.name)

#        print(event)
#        print(dir(event))
#        print(event.header)
#        print(event.name)
#        print(event_fields)
#        print(event.fields)
#        print("\n")
#print(records)
for record in record_names:
    print(record)
    print(record_names[record])
    pass


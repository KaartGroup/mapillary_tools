#!/usr/bin/env python

from fitparse import FitFile
import datetime
from tqdm import tqdm
import sortedcontainers

'''
Methods for parsing gps data from Garmin FIT files
'''

class RecordObject(object):
    def __init__(self, fitfileDictionary):
        self._dictionary = fitfileDictionary

    def __lt__(self, other):
        return self._getSortKey() < other._getSortKey()

    def _getSortKey(self):
        if "timestamp" in self._dictionary:
            rValue = self._dictionary["timestamp"]
            if "timestamp_ms" in self._dictionary:
                rValue += self._dictionary["timestamp_ms"]
            return rValue
        else:
            raise ValueError("There is no timestamp")

    def __str__(self):
        return self._dictionary["timestamp"]
        #return("{}.{}: {}, {}".format(self._dictionary["timestamp"], self._dictionary["timestamp_ms"] if "timestamp_ms" in self._dictionary else 0, self._dictionary["position_lat"], self._dictionary["position_long"]))

    def getDictionary(self):
        return self._dictionary

    def getLatitude(self):
        return self._dictionary["position_lat"] if "position_lat" in self._dictionary else None

    def getLongitude(self):
        return self._dictionary["position_long"] if "position_long" in self._dictionary else None

    def getAltitude(self):
        return self._dictionary["altitude"] if "altitude" in self._dictionary else None

    def getSpeed(self):
        return self._dictionary["speed"] if "speed" in self._dictionary else None

    def createTuple(self):
        rTuple = (
                self._dictionary["timestamp"],
                float(self._dictionary["position_lat"]) * 180 / 2**31,
                float(self._dictionary["position_long"]) * 180 / 2**31,
                self._dictionary["altitude"] if "altitude" in self._dictionary else None
            )
        return rTuple


def parse_uuid_string(uuid_string):
    '''
    Parses a video uuid string from fit similar to:  VIRBactioncameraULTRA30_Timelapse_3840_2160_1.0000_3936073999_36a2eff0_1_111_2019-01-17-09-01-03.fit
    Returns a tuple (camera_type, video_type, width, height, frame_rate, serial, unknown_1, unkown_2, video_id, fit_filename)
    '''
    return tuple(uuid_string.split("_"))


def get_lat_lon_time_from_fit(geotag_file_list, local_time=True, verbose=False):
    '''
    Read location and time stamps from a track in a FIT file.

    Returns a tuple (video_start_time, points) where points is a list of tuples (time, lat, lon, altitude)
    '''
    vids = {}
    sortedList = sortedcontainers.SortedSet()
    for geotag_file in geotag_file_list:

        alt = None
        lat = None
        lon = None
        time_delta = None
        fit = FitFile(geotag_file)

        vid_times = {}
        try:
            for record in fit.get_messages('record'):
                recordDict = {}
                for record_data in record:
                    recordDict[record_data.name] = record_data.value
                sortedList.add(RecordObject(recordDict))
        except ValueError:
            # Occurs when record not in fit file
            pass
    returnList = [record.createTuple() for record in sortedList if record.getLatitude() is not None]
    return returnList

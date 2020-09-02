import re
import pandas as pd

class MapData:

    def __init__(self, data):
        self.data = data
        self.home_col = sorted([x for x in list(data.columns) if re.search("l[na][gt]_h", x)], reverse = True)
        self.dest_col = sorted([x for x in list(data.columns) if re.search("l[na][gt]_d$", x)], reverse = True)
        self.territories = tuple(data.TA2018_name.unique())

    def getregiondata(self, region):
        return self.data[ (self.data.SA2_name_h == region) | (self.data.SA2_name_d == region) ]
    
    def getwidthfeature(self, commute_means):
        '''Can be modified further to look for max and min'''
        return "{0} * 0.2".format(commute_means)

    def getmeans(self):
        #get column names
        cols = list(self.data.columns)
        #returns tuple of columns that doesnt have SA2, lat or lng
        means_list = [x for x in cols if not (re.search("^SA2", x) or re.search("^lng", x) or re.search("^lat", x) or re.search("^TA2018", x))]

        return means_list

    def getHomeLoc(self, region):
        df = self.data[self.data.SA2_name_h == region]
        lng = list(df.lng_h.unique())
        lat = list(df.lat_h.unique())

        return (lng[0], lat[0])

    def getarea(self, territory):
        df = self.data[self.data.TA2018_name == territory]
        return tuple(df.SA2_name_h.unique())

    







    


    
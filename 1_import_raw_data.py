import os
import glob
from lib.utils import convert_xml_to_csv

from config import *

if __name__ == "__main__":       
    for xmlfile in glob.glob("data/xml/training/*.xml"):
        print "Converting", xmlfile
        filename = os.path.split(xmlfile)[-1][:-4]
        itemid = os.path.splitext(filename)[0]
        print filename
        outputfile = "data/csv/" + itemid + ".csv"
        convert_xml_to_csv(xmlfile, outputfile,COL_NAMES,READINGS_LIST,data_point=None,filezipped=False)

    for xmlfile in glob.glob("data/xml/validation/*.xml"):
        print "Converting", xmlfile
        filename = os.path.split(xmlfile)[-1][:-4]
        itemid = os.path.splitext(filename)[0]
        print filename
        outputfile = "data/csv/" + itemid + ".csv"
        convert_xml_to_csv(xmlfile, outputfile,COL_NAMES,READINGS_LIST,data_point=None,filezipped=False,append=True)

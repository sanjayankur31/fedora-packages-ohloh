#!/usr/bin/python

# Copyright 2013 Ankur Sinha 
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com> 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# File : getSourceList.py
#

import sys, urllib
import time
import xml.etree.ElementTree as ET

def run ():
    """
    Usage: ./getSourceList.py <API KEY>

    Gets the list of enlistments for fedora-packages on ohloh

    Refer:
        https://github.com/blackducksw/ohloh_api/blob/master/reference/enlistment.md

    """

# Get API key from command line
    api_key = sys.argv[1]

# Uh huh!
    total_pages = 1190

# API key only permits 1000 requests over a day. Run two requests in two days
# for complete list
    get_pages = 500;
    for page in range (1, get_pages, 1):
        params = urllib.urlencode({'api_key': api_key , 'page': page})
        url = "http://www.ohloh.net/projects/fedora-packages/enlistments.xml?%s" % params
        print "URL: %s" % url
        f = urllib.urlopen(url)

# Parse the response into a structured XML object
        tree = ET.parse(f)

# Did Ohloh return an error?
        elem = tree.getroot()
        error = elem.find("error")
        if error != None:
            print 'Ohloh returned:', ET.tostring(error),
            sys.exit()

        for node in elem.iter ():
            if node.tag == "url":
                print "\t%s:\t%s" % (node.tag, node.text)

# Give a gap between each call to ensure we don't stress ohloh too much
        time.sleep(0.1)

if __name__ == "__main__":
    run ()

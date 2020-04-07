#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 2019

@author: Kannan
"""
from configparser import ConfigParser

# Parser for property file
parser = ConfigParser()
parser.read('..//config//jd.config')

# Get String with repeated characters
def getStringWithThis(thischar):
    return thischar * 143

# Format ' String
def format_single_quote(field):
    if "'" in field:
        field = field.replace("'", "''")
    return field

#Format newLine , carriage return
def format_newLineCarriageReturn(field):
    return field.replace('\n', ' ').replace('\r', '')

# Get City List
def getCityList():
    return parser.get('search', 'cities').split(':')

#Get keyWord List
def getKeyWordList():
    return parser.get('search', 'keywords').split(':')

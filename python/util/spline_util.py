#!/usr/bin/env python3
#encoding=utf-8

# distance between two points
from math import hypot

def get_distance(x1,y1,x2,y2):
    dist = int(hypot(x2 - x1, y2 - y1))
    return dist

def average(lst): 
    return sum(lst) / len(lst) 

def is_same_direction_list(args,deviation=0):
    ret = True
    args_average=average(args)
    #print("args_average:", args_average)

    direction = -1
    if args[0] <= args_average:
        direction = 1
    
    idx=0
    args_count = len(args)
    for item in args:
        idx+=1
        if idx == args_count:
            break

        if direction==1:
            if (args[idx]+deviation)<item and (args[idx]-deviation)<item:
                ret = False
                break
        else:
            if (args[idx]+deviation)>item and (args[idx]-deviation)>item:
                ret = False
                break
    return ret

def is_same_direction(*args,deviation=0):
    return self.is_same_direction_list(args,deviation=deviation)

# common functions.
def find_between(s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def field_right(s, first, is_include_symbol=False):
    try:
        start = s.index(first )
        if not is_include_symbol:
            start += len(first )
        return s[start:]
    except ValueError:
        return ""

def field_left(s, first, is_include_symbol=False):
    try:
        start = s.index(first )
        if is_include_symbol:
            start += len(first )
        return s[:start]
    except ValueError:
        return ""

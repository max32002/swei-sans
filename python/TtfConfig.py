#!/usr/bin/env python3
#encoding=utf-8

class TtfConfig():
    VERSION = "1.042"
    PROCESS_MODE = "SANS"

    STYLE_INDEX = 4
    STYLE_ARRAY = ["Black","Bold","Medium","Regular","DemiLight","Light","Thin"]
    STYLE=STYLE_ARRAY[STYLE_INDEX]

    DEFAULT_COORDINATE_VALUE = -9999

    # for Regular
    #STROKE_MAX = 84
    #STROKE_MIN = 54

    STROKE_MAX = 90
    STROKE_MIN = 40
    
    STROKE_ACCURACY_PERCENT = 5
    STROKE_WIDTH_MAX = int((STROKE_MAX * (100+STROKE_ACCURACY_PERCENT))/100)
    STROKE_WIDTH_MIN = int((STROKE_MIN * (100-STROKE_ACCURACY_PERCENT))/100)
    #print("STROKE_WIDTH_MAX:", STROKE_WIDTH_MAX)
    #print("STROKE_MIN:", STROKE_MIN)

    # for X,Y axis equal compare.
    # each 100 px, +- 8 px.
    EQUAL_ACCURACY_MIN = 3
    EQUAL_ACCURACY_PERCENT = 0.08

    # unicode in field
    # 1 to 3
    UNICODE_FIELD = 2

    def hello(self):
        print("world!")

    def __init__(self, weight_code):
        import datetime

        self.STYLE_INDEX = int(weight_code)
        self.apply_weight_setting()
        print("Transform Mode:", self.PROCESS_MODE)
        print("Transform Style:", self.STYLE)
        print("Transform Version:", self.VERSION)
        print("Transform Time:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def apply_weight_setting(self):
        self.STYLE=self.STYLE_ARRAY[self.STYLE_INDEX]

        if self.STYLE in ["Black"]:
            self.STROKE_MAX = 154
            self.STROKE_MIN = 54

        if self.STYLE in ["Bold"]:
            self.STROKE_MAX = 134
            self.STROKE_MIN = 54

        if self.STYLE in ["SemiBold","Medium"]:
            self.STROKE_MAX = 114
            self.STROKE_MIN = 44

        if self.STYLE in ["Light","DemiLight"]:
            self.STROKE_MAX = 84
            self.STROKE_MIN = 34

        if self.STYLE in ["Thin"]:
            self.STROKE_MAX = 74
            self.STROKE_MIN = 26

        self.STROKE_WIDTH_MAX = int((self.STROKE_MAX * (100+self.STROKE_ACCURACY_PERCENT))/100)
        self.STROKE_WIDTH_MIN = int((self.STROKE_MIN * (100-self.STROKE_ACCURACY_PERCENT))/100)

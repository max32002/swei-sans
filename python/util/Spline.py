#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util

class Spline():
    config = None

    def __init__(self):
        pass

    def check_clockwise(self, spline_dict):
        clockwise = True
        area_total=0
        poly_lengh = len(spline_dict['dots'])
        #print('check poly: (%d,%d)' % (poly[0][0],poly[0][1]))
        for idx in range(poly_lengh):
            #item_sum = ((poly[(idx+1)%poly_lengh][0]-poly[(idx+0)%poly_lengh][0]) * (poly[(idx+1)%poly_lengh][1]-poly[(idx+0)%poly_lengh][1]))
            item_sum = ((spline_dict['dots'][(idx+0)%poly_lengh]['x']*spline_dict['dots'][(idx+1)%poly_lengh]['y']) - (spline_dict['dots'][(idx+1)%poly_lengh]['x']*spline_dict['dots'][(idx+0)%poly_lengh]['y']))
            #print(idx, poly[idx][0], poly[idx][1], item_sum)
            area_total += item_sum
        #print("area_total:",area_total)
        if area_total >= 0:
            clockwise = not clockwise
        return clockwise

    def assign_config(self, config):
        self.config = config

    def hello(self):
        print("world")

    def trace(self, stroke_dict):
        #print("trace")
        #print(stroke_dict)
        is_modified = False

        bmp_image = None
        y_offset = 880

        self.preprocess(stroke_dict)

        for key in stroke_dict.keys():
            spline_dict = stroke_dict[key]
            #print("key:", key, 'code:', spline_dict['dots'][0])
            # for debug
            #if key==2:
            if True:
                clockwise = self.check_clockwise(spline_dict)
                #print("clockwise:", clockwise)
                self.normalize(stroke_dict, key, bmp_image, y_offset)
                if clockwise:
                    trace_result, spline_dict = self.trace_nodes_in_strok(spline_dict)
                    if trace_result:
                        is_modified = True

            stroke_dict[key] = spline_dict

        return is_modified, stroke_dict

    def detect_margin(self, spline_dict):
        default_int = -9999

        margin_top=default_int
        margin_bottom=default_int
        margin_left=default_int
        margin_right=default_int
        for dot_dict in spline_dict['dots']:
            x=dot_dict['x']

            if x != default_int:
                if margin_right==default_int:
                    # initail assign
                    margin_right=x
                else:
                    # compare top
                    if x > margin_right:
                        margin_right = x

                if margin_left==default_int:
                    # initail assign
                    margin_left=x
                else:
                    # compare bottom
                    if x < margin_left:
                        margin_left = x

            y=dot_dict['y']
            if y !=default_int:
                if margin_top==default_int:
                    # initail assign
                    margin_top=y
                else:
                    # compare top
                    if y > margin_top:
                        margin_top = y

                if margin_bottom==default_int:
                    # initail assign
                    margin_bottom=y
                else:
                    # compare bottom
                    if y < margin_bottom:
                        margin_bottom = y

        spline_dict["top"]  = margin_top
        spline_dict["bottom"] = margin_bottom
        spline_dict["left"] = margin_left
        spline_dict["right"] = margin_right

    def split_spline(self, stroke_dict):
        redo_split = False
        from . import Rule101_Split_Spline

        #print("before split count:", len(stroke_dict))
        for key in stroke_dict.keys():
            spline_dict = stroke_dict[key]
            #print("key:", key, 'code:', spline_dict['dots'][0])
            # for debug
            #if key==5:
            if True:
                clockwise = self.check_clockwise(spline_dict)
                #print("clockwise:", clockwise)
                if clockwise:
                    # format code.
                    # start to travel nodes for [RULE #9]
                    # format curve coner as l conver

                    ru101=Rule101_Split_Spline.Rule()
                    ru101.assign_config(self.config)

                    idx=-1
                    redo_travel,idx,new_format_dict_array=ru101.apply(spline_dict, idx)
                    ru101 = None

                    if redo_travel:
                        if new_format_dict_array != None:
                            if len(new_format_dict_array) > 0:
                                new_key_index = len(stroke_dict)+1
                                stroke_dict[new_key_index]={}
                                stroke_dict[new_key_index]['dots']=new_format_dict_array
                        redo_split = True
                        break

            stroke_dict[key] = spline_dict

        #print("after split count:", len(stroke_dict))

        return redo_split

    def preprocess(self, stroke_dict):
        MAX_SPLIT_CONNT = 100

        idx=-1
        redo_split=False   # Disable
        redo_split=True    # Enable
        while redo_split:
            idx+=1
            redo_split=self.split_spline(stroke_dict)
            if idx >= MAX_SPLIT_CONNT:
                redo_split = False

    def normalize(self, stroke_dict, key, bmp_image, y_offset):
        from . import Rule102_Clean_Noise
        ru102=Rule102_Clean_Noise.Rule()
        ru102.assign_config(self.config)
        
        from . import Rule103_Merge_Line
        ru103=Rule103_Merge_Line.Rule()
        ru103.assign_config(self.config)

        from . import Rule104_Almost_Line_Curve
        ru104=Rule104_Almost_Line_Curve.Rule()
        ru104.assign_config(self.config)

        spline_dict = stroke_dict[key]

        # ==================================================
        # format code block
        # ==================================================

        # format code.
        # start to travel nodes for [RULE #104]
        # format curve coner as l conver
        #print("start Rule # 104...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        while redo_travel:
            redo_travel,idx=ru104.apply(spline_dict, idx)
        ru104 = None


        # start to travel nodes for [RULE #102]
        # format curve coner as l conver
        #print("start Rule # 102...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        while redo_travel:
            redo_travel,idx=ru102.apply(spline_dict, idx)
        ru102 = None

        # start to travel nodes for [RULE #103]
        # 有 first point 的關係，有時會有一小段的直線。
        #print("start Rule # 103...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        while redo_travel:
            redo_travel,idx=ru103.apply(spline_dict, idx)
        ru103 = None

        return spline_dict

    def trace_nodes_in_strok(self, spline_dict):
        is_modified = False

        from . import Rule1
        ru1=Rule1.Rule()
        ru1.assign_config(self.config)

        from . import Rule2
        ru2=Rule2.Rule()
        ru2.assign_config(self.config)

        self.detect_margin(spline_dict)

        # start to travel nodes for [RULE #1]
        # 
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        while redo_travel:
            redo_travel,idx=ru1.apply(spline_dict, idx)
            if redo_travel:
                is_modified = True
        ru1 = None

        # start to travel nodes for [RULE #2]
        # 
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        while redo_travel:
            redo_travel,idx=ru2.apply(spline_dict, idx)
            if redo_travel:
                is_modified = True
        ru2 = None

        return is_modified, spline_dict

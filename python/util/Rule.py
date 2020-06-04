#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util

class Rule():
    config = None
    unicode_int = -1

    def __init__(self):
        pass

    def assign_config(self, config):
        self.config = config

    def assign_unicode(self, val):
        self.unicode_int = val

    # 0-24F
    def is_Latin(self):
        ret = False
        if self.unicode_int > 0:
            if self.unicode_int <= 591:
                ret = True
        return ret

    # Hangul Syllables, U+AC00 - U+D7AF[3]
    def is_Hangul(self):
        ret = False
        if self.unicode_int > 0:
            if self.unicode_int >= 44032 and self.unicode_int <= 55215:
                ret = True
        return ret

    def reset_first_point(self, format_dict_array, spline_dict):
        spline_x = spline_dict['dots'][0]['x']
        spline_y = spline_dict['dots'][0]['y']
        spline_t = 'm'
        spline_code = spline_dict['dots'][0]['code']

        nodes_length = len(format_dict_array)
        # [IMPORTANT] data in "format_dict_array" are not CLEAN! 
        # please compute data from code.
        old_code = format_dict_array[nodes_length-1]['code']
        old_code_array = old_code.split(' ')
        if ' c ' in old_code:
            last_x = int(float(old_code_array[5]))
            last_y = int(float(old_code_array[6]))
        else:
            last_x = int(float(old_code_array[1]))
            last_y = int(float(old_code_array[2]))

        #print("original x,y:", spline_x,"-",spline_y,", transformed last x,y=",last_x,"-",last_y)
        if not(spline_x==last_x and spline_y==last_y):
            #print("not match!")
            #print("m old_code_string:", spline_code)
            
            old_code_array = spline_code.split(' ')
            old_code_array[0] = str(last_x)
            old_code_array[1] = str(last_y)
            
            # keep extra infomation cause more error.
            #new_code = ' '.join(old_code_array)
            new_code = "%d %d m 1\n" % (last_x, last_y)

            spline_x = last_x
            spline_y = last_y
            spline_code = new_code
            #print("new code:", spline_code)

        #print("\n\nbefore:", format_dict_array)
        dot_dict={}
        dot_dict['x']=spline_x
        dot_dict['y']=spline_y
        dot_dict['t']=spline_t
        dot_dict['code']=spline_code
        format_dict_array.insert(0,dot_dict)
        #print("\n\nafter:", format_dict_array)
        spline_dict['dots'] = format_dict_array

    def caculate_distance(self, format_dict_array):
        nodes_length = len(format_dict_array)
        for idx in range(nodes_length):
            next_index = (idx+1)%nodes_length

            # It's easy to forget to fill attrib!
            # restore value from code.
            old_code_string = format_dict_array[idx]['code']
            old_code_array = old_code_string.split(' ')
            if format_dict_array[idx]['t']=='c':
                format_dict_array[idx]['x1']=int(float(old_code_array[1]))
                format_dict_array[idx]['y1']=int(float(old_code_array[2]))
                format_dict_array[idx]['x2']=int(float(old_code_array[3]))
                format_dict_array[idx]['y2']=int(float(old_code_array[4]))
                format_dict_array[idx]['x']=int(float(old_code_array[5]))
                format_dict_array[idx]['y']=int(float(old_code_array[6]))
            else:
                format_dict_array[idx]['x']=int(float(old_code_array[1]))
                format_dict_array[idx]['y']=int(float(old_code_array[2]))

            current_x = format_dict_array[idx]['x']
            current_y = format_dict_array[idx]['y']

            next_x = format_dict_array[next_index]['x']
            next_y = format_dict_array[next_index]['y']
            distance = spline_util.get_distance(current_x,current_y,next_x,next_y)
            format_dict_array[idx]['distance']=distance

            format_dict_array[idx]['match_stroke_width'] = False
            if distance >= self.config.STROKE_WIDTH_MIN and distance <= self.config.STROKE_WIDTH_MAX:
                format_dict_array[idx]['match_stroke_width'] = True

            format_dict_array[idx]['x_direction']=0
            if next_x > current_x:
                format_dict_array[idx]['x_direction']=1
            if next_x < current_x:
                format_dict_array[idx]['x_direction']=-1

            format_dict_array[idx]['y_direction']=0
            if next_y > current_y:
                format_dict_array[idx]['y_direction']=1
            if next_y < current_y:
                format_dict_array[idx]['y_direction']=-1

            # 有誤差地判斷，與下一個點是否為平行線。
            EQUAL_ACCURACY = self.config.EQUAL_ACCURACY_PERCENT * distance
            if EQUAL_ACCURACY <= self.config.EQUAL_ACCURACY_MIN:
                EQUAL_ACCURACY = self.config.EQUAL_ACCURACY_MIN
            format_dict_array[idx]['x_equal_fuzzy']=False
            if abs(next_x - current_x) <= EQUAL_ACCURACY:
                format_dict_array[idx]['x_equal_fuzzy']=True

            format_dict_array[idx]['y_equal_fuzzy']=False
            if abs(next_y - current_y) <= EQUAL_ACCURACY:
                format_dict_array[idx]['y_equal_fuzzy']=True

        return format_dict_array

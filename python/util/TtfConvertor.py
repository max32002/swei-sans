#!/usr/bin/env python3
#encoding=utf-8

import os
import glob

from . import Spline

class Convertor():
    sp = Spline.Spline()
    config = None

    def __init__(self):
        pass

    def load_to_memory(self, filename_input):
        stroke_dict = {}
        dot_dict = {}
        dots_array = []
        points_array = []
        default_int = -9999

        #print("load to memory, filename_input:", filename_input)
        myfile = open(filename_input, 'r')

        code_begin_string = 'SplineSet'
        code_begin_string_length = len(code_begin_string)
        code_end_string = 'EndSplineSet'
        code_end_string_length = len(code_end_string)

        is_code_flag=False

        stroke_index = 0
        
        for x_line in myfile:
            if not is_code_flag:
                # check begin.

                if code_begin_string == x_line[:code_begin_string_length]:
                    is_code_flag = True
            else:
                # is code start.
                #print("x_line:", x_line)

                if x_line[:1] != ' ':
                    if stroke_index >= 1:
                        stroke_dict[stroke_index]={}
                        stroke_dict[stroke_index]['dots'] = dots_array
                        stroke_dict[stroke_index]['points'] = points_array
                        #if stroke_index == 1:
                            #print("key:", stroke_index, "data:", stroke_dict)
                        
                        # reset new
                        dots_array = []
                        points_array = []

                    stroke_index += 1

                # check end
                if code_end_string == x_line[:code_end_string_length]:
                    #is_code_flag = False
                    break

                dot_dict = {}
                #print("add to code:", x_line)
                dot_dict['code'] = x_line

                # type
                t=''
                if ' m ' in x_line:
                    t='m'
                if ' l ' in x_line:
                    t='l'
                if ' c ' in x_line:
                    t='c'
                dot_dict['t']=t

                x=default_int
                y=default_int
                x1=default_int
                y1=default_int
                x2=default_int
                y2=default_int
                if ' ' in x_line:
                    x_line_array = x_line.split(' ')
                    if t=='m':
                        x=int(float(x_line_array[0]))
                        y=int(float(x_line_array[1]))

                    if t=='l':
                        x=int(float(x_line_array[1]))
                        y=int(float(x_line_array[2]))

                    if t=='c':
                        if len(x_line_array) >=7:
                            x=int(float(x_line_array[5]))
                            y=int(float(x_line_array[6]))
                            x1=int(float(x_line_array[1]))
                            y1=int(float(x_line_array[2]))
                            x2=int(float(x_line_array[3]))
                            y2=int(float(x_line_array[4]))
                points_array.append([x,y])

                dot_dict['x']=x
                dot_dict['y']=y

                dot_dict['x1']=x1
                dot_dict['y1']=y1
                dot_dict['x2']=x2
                dot_dict['y2']=y2

                dots_array.append(dot_dict)

        myfile.close()
        return stroke_dict

    def write_to_file(self, filename_input, stroke_dict, readonly):
        filename_input_new = filename_input + ".tmp"

        myfile = open(filename_input, 'r')
        myfile_new = open(filename_input_new, 'w')
        code_begin_string = 'SplineSet'
        code_begin_string_length = len(code_begin_string)
        code_end_string = 'EndSplineSet'
        code_end_string_length = len(code_end_string)

        is_code_flag=False

        stroke_index = 0
        #print("write_to_file:", filename_input)
        for x_line in myfile:
            #print("x_line:", x_line)
            if not is_code_flag:
                # check begin.

                if code_begin_string == x_line[:code_begin_string_length]:
                    is_code_flag = True
                myfile_new.write(x_line)

            else:
                # check end
                if code_end_string == x_line[:code_end_string_length]:
                    #print("code_end_string:", x_line)

                    is_code_flag = False

                    #flush memory to disk
                    for key in stroke_dict.keys():
                        #print("key:", key)
                        spline_dict = stroke_dict[key]
                        #print("spline_dict:", spline_dict)
                        for dot_dict in spline_dict['dots']:
                            new_line = dot_dict['code']
                            myfile_new.write(new_line)

                    myfile_new.write(x_line)
                    #break

        myfile.close()
        myfile_new.close()

        if not readonly:
            os.remove(filename_input)
            os.rename(filename_input_new, filename_input)

        return stroke_dict

    def convet_font(self, filename_input, readonly=False):
        ret = False

        stroke_dict = self.load_to_memory(filename_input)
        self.sp.assign_config(self.config)

        ret, stroke_dict = self.sp.trace(stroke_dict)

        if ret:
            if not stroke_dict is None:
                #print("write to file:", filename_input)
                self.write_to_file(filename_input,stroke_dict,readonly)
                stroke_dict = None

        return ret

    def convert(self, path, config):
        self.config = config
        readonly = True     #debug
        readonly = False    #online

        idx=0
        convert_count=0

        filename_pattern = path + "/*.glyph"
        for name in glob.glob(filename_pattern):
            idx+=1
            #print("convert filename:", name)
            is_convert = False
            is_convert = self.convet_font(name,readonly)
            if is_convert:
                convert_count+=1
                #print("convert list:", name)
            #break

            if idx % 1000 == 0:
                print("Processing:", idx)

        return idx

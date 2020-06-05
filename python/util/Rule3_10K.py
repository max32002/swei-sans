#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

class Rule(Rule.Rule):

# RULE # 3
# 「萬」的冂符號
# PS: 因為 array size change, so need redo.

    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx):
        redo_travel=False

        # clone
        format_dict_array=[]
        format_dict_array = spline_dict['dots'][1:]
        format_dict_array = self.caculate_distance(format_dict_array)

        nodes_length = len(format_dict_array)
        #print("orig nodes_length:", len(spline_dict['x']))
        #print("format nodes_length:", nodes_length)

        travel_enable = True
        if self.is_Latin() or self.is_Hangul():
            travel_enable = False

        rule_need_lines = 12
        fail_code = -1
        if nodes_length >= rule_need_lines and travel_enable:
            for idx in range(nodes_length):
                if idx <= resume_idx:
                    # skip traveled nodes.
                    continue

                is_debug_mode = False
                #is_debug_mode = True

                if is_debug_mode:
                    debug_coordinate_list = [[399,355]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(12):
                        print(debug_idx-2,": values#3:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # begin travel.
                is_match_pattern = True

                if is_match_pattern:
                    fail_code = 100
                    if format_dict_array[(idx+1)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                            if format_dict_array[(idx+3)%nodes_length]['t'] == 'l':
                                if format_dict_array[(idx+4)%nodes_length]['t'] == 'l':
                                    if format_dict_array[(idx+5)%nodes_length]['t'] == 'l':
                                        if format_dict_array[(idx+6)%nodes_length]['t'] == 'l':
                                            if format_dict_array[(idx+7)%nodes_length]['t'] == 'l':
                                                if format_dict_array[(idx+8)%nodes_length]['t'] == 'l':
                                                    is_match_pattern = True

                # compare dot+0
                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False
                    # only go buttom
                    if format_dict_array[(idx+0)%nodes_length]['y_direction'] < 0:
                        if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                            if format_dict_array[(idx+0)%nodes_length]['distance'] > 120:
                                is_match_pattern = True

                # compare dot+1
                if is_match_pattern:
                    fail_code = 210
                    is_match_pattern = False
                    # only go left
                    if format_dict_array[(idx+1)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+1)%nodes_length]['x_direction'] < 0:
                            if format_dict_array[(idx+1)%nodes_length]['match_stroke_width']:
                                is_match_pattern = True

                # compare dot+2
                if is_match_pattern:
                    fail_code = 220
                    is_match_pattern = False
                    # only go up.
                    if format_dict_array[(idx+2)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+2)%nodes_length]['y_direction'] > 0:
                            if format_dict_array[(idx+2)%nodes_length]['distance'] > 120:
                                is_match_pattern = True

                # compare dot+3
                if is_match_pattern:
                    fail_code = 230
                    is_match_pattern = False
                    # only go left
                    if format_dict_array[(idx+3)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+3)%nodes_length]['x_direction'] < 0:
                            if format_dict_array[(idx+3)%nodes_length]['distance'] < 100:
                                is_match_pattern = True

                # compare dot+4
                if is_match_pattern:
                    fail_code = 240
                    is_match_pattern = False
                    # only go up.
                    if format_dict_array[(idx+4)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+4)%nodes_length]['y_direction'] > 0:
                            if format_dict_array[(idx+4)%nodes_length]['match_stroke_width']:
                                is_match_pattern = True

                # compare dot+5
                if is_match_pattern:
                    fail_code = 250
                    is_match_pattern = False
                    # only go left
                    if format_dict_array[(idx+5)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+5)%nodes_length]['x_direction'] > 0:
                            if format_dict_array[(idx+5)%nodes_length]['distance'] < 100:
                                is_match_pattern = True

                # compare dot+6
                if is_match_pattern:
                    fail_code = 260
                    is_match_pattern = False
                    # only go up.
                    if format_dict_array[(idx+6)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+6)%nodes_length]['y_direction'] > 0:
                            if format_dict_array[(idx+6)%nodes_length]['distance'] < 100:
                                is_match_pattern = True

                # compare dot+7
                if is_match_pattern:
                    fail_code = 270
                    is_match_pattern = False
                    # only go right
                    if format_dict_array[(idx+7)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+7)%nodes_length]['x_direction'] > 0:
                            if format_dict_array[(idx+7)%nodes_length]['match_stroke_width']:
                                is_match_pattern = True

                # compare dot+8
                if is_match_pattern:
                    fail_code = 280
                    is_match_pattern = False
                    # only go bottom.
                    if format_dict_array[(idx+8)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+8)%nodes_length]['y_direction'] < 0:
                            if format_dict_array[(idx+8)%nodes_length]['distance'] < 100:
                                is_match_pattern = True

                # compare dot+9
                if is_match_pattern:
                    fail_code = 290
                    is_match_pattern = False
                    # only go right.
                    if format_dict_array[(idx+9)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+9)%nodes_length]['x_direction'] > 0:
                            if format_dict_array[(idx+9)%nodes_length]['distance'] > 150:
                                is_match_pattern = True

                # compare dot-1
                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False
                    # only go right.
                    if format_dict_array[(idx+nodes_length-1)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+nodes_length-1)%nodes_length]['x_direction'] < 0:
                            if format_dict_array[(idx+nodes_length-1)%nodes_length]['distance'] > 150:
                                is_match_pattern = True

                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#3:", fail_code)
                        pass
                    else:
                        print("match rule #3")
                        print(idx,"debug rule#3:",format_dict_array[idx]['code'])
                        pass

                #print(idx,"fail code:", fail_code)
                if is_match_pattern:

                    target_index = (idx+3)%nodes_length
                    del format_dict_array[target_index]

                    # side effect after remove item.
                    if idx > target_index:
                        idx -= 1

                    nodes_length = len(format_dict_array)
                    target_index = (idx+3)%nodes_length
                    del format_dict_array[target_index]

                    # side effect after remove item.
                    if idx > target_index:
                        idx -= 1

                    nodes_length = len(format_dict_array)
                    target_index = (idx+3)%nodes_length
                    del format_dict_array[target_index]

                    # side effect after remove item.
                    if idx > target_index:
                        idx -= 1

                    nodes_length = len(format_dict_array)
                    target_index = (idx+4)%nodes_length
                    del format_dict_array[target_index]

                    # side effect after remove item.
                    if idx > target_index:
                        idx -= 1

                    nodes_length = len(format_dict_array)
                    nodes_length = len(format_dict_array)
                    target_index = (idx+4)%nodes_length
                    del format_dict_array[target_index]

                    # side effect after remove item.
                    if idx > target_index:
                        idx -= 1

                    nodes_length = len(format_dict_array)
                    nodes_length = len(format_dict_array)
                    target_index = (idx+4)%nodes_length
                    del format_dict_array[target_index]

                    # side effect after remove item.
                    if idx > target_index:
                        idx -= 1

                    nodes_length = len(format_dict_array)

                    redo_travel=True
                    resume_idx = idx
                    break
                    #pass

        if redo_travel:
            # check close path.
            self.reset_first_point(format_dict_array, spline_dict)

        return redo_travel, resume_idx

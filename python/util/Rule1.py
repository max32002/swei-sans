#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

class Rule(Rule.Rule):

# RULE # 1
# 拔角(右下) 9號洞
# PS: 因為 array size change, so need redo.

    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx):
        redo_travel=False

        MAX_LEG_LENGTH_PERCENT=21
        MAX_LEFT_MOUNTAIN_HEIGHT = 30   # for 山 & 出 的橫線。獅尾黑體
        LINE_ACCURACY=3

        MORE_LEG_LENGTH_UNDERGROUND_LENGTH = 600   # for 㠀的山要拔腳。底夠長，可以多拔一點。
        MORE_MAX_LEG_LENGTH_PERCENT=24

        # fix 搏/博/㙛/捕 誤拔問題。
        NEXT_HORIZONTAL_LINE_Y_ACCURACY=6

        # clone
        format_dict_array=[]
        format_dict_array = spline_dict['dots'][1:]
        format_dict_array = self.caculate_distance(format_dict_array)

        nodes_length = len(format_dict_array)
        #print("orig nodes_length:", len(spline_dict['x']))
        #print("format nodes_length:", nodes_length)

        rule_need_lines = 5
        fail_code = -1
        if nodes_length >= rule_need_lines:
            for idx in range(nodes_length):
                if idx <= resume_idx:
                    # skip traveled nodes.
                    continue

                is_debug_mode = False
                #is_debug_mode = True

                if is_debug_mode:
                    debug_coordinate_list = [[899,659]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(8):
                        print(debug_idx-2,": values for rule#2:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # begin travel.
                is_match_pattern = True

                if is_match_pattern:
                    fail_code = 100
                    if format_dict_array[(idx+1)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                            if format_dict_array[(idx+3)%nodes_length]['t'] == 'l':
                                is_match_pattern = True

                # compare dot+0
                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False
                    # only go buttom
                    if format_dict_array[(idx+0)%nodes_length]['y_direction'] < 0:
                        if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                            is_match_pattern = True

                # compare dot+1
                if is_match_pattern:
                    fail_code = 210
                    is_match_pattern = False
                    # only go left
                    if format_dict_array[(idx+1)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+1)%nodes_length]['x_direction'] < 0:
                           is_match_pattern = True

                # dot# 1 match stroke width
                if is_match_pattern:
                    fail_code = 210
                    is_match_pattern = False
                    if format_dict_array[(idx+1)%nodes_length]['match_stroke_width']:
                        is_match_pattern = True

                # compare dot+2
                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False
                    # only go up.
                    if format_dict_array[(idx+2)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+2)%nodes_length]['y_direction'] > 0:
                           is_match_pattern = True

                # compare dot+3
                if is_match_pattern:
                    fail_code = 400
                    is_match_pattern = False
                    # only go left.
                    if format_dict_array[(idx+3)%nodes_length]['x_direction'] < 0:
                        fail_code = 410
                        if format_dict_array[(idx+3)%nodes_length]['y_equal_fuzzy']:
                           is_match_pattern = True
                        else:
                            # 替「㟝」增加例外。
                            fail_code = 420
                            distance = format_dict_array[(idx+3)%nodes_length]['distance']
                            EQUAL_ACCURACY = self.config.EQUAL_ACCURACY_PERCENT * distance
                            if format_dict_array[(idx-1+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                fail_code = 430
                                if format_dict_array[(idx-1+nodes_length)%nodes_length]['x_direction'] > 0:
                                    fail_code = 431
                                    if format_dict_array[(idx+5+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                        fail_code = 432
                                        if format_dict_array[(idx+5+nodes_length)%nodes_length]['x_direction'] > 0:
                                            fail_code = 433
                                            if format_dict_array[(idx+4+nodes_length)%nodes_length]['x_equal_fuzzy']:
                                                fail_code = 434
                                                if format_dict_array[(idx+4+nodes_length)%nodes_length]['y_direction'] > 0:
                                                    fail_code = 435
                                                    if format_dict_array[(idx+0+nodes_length)%nodes_length]['distance'] > self.config.STROKE_MAX:
                                                        fail_code = 436
                                                        if format_dict_array[(idx+3+nodes_length)%nodes_length]['distance'] > self.config.STROKE_MAX:
                                                            fail_code = 437
                                                            if format_dict_array[(idx+4+nodes_length)%nodes_length]['distance'] > self.config.STROKE_MAX:
                                                                fail_code = 438
                                                                # dot4, must large then dot3
                                                                if format_dict_array[(idx+4+nodes_length)%nodes_length]['distance'] > format_dict_array[(idx+3+nodes_length)%nodes_length]['distance']:
                                                                    fail_code = 439
                                                                    # dot0 is the largest.
                                                                    if format_dict_array[(idx+0+nodes_length)%nodes_length]['distance'] > format_dict_array[(idx+4+nodes_length)%nodes_length]['distance']:
                                                                        fail_code = 440
                                                                        # 放寬誤差, 使用 (318-74) * 0.08 = 19, 目標是要到 22
                                                                        EQUAL_ACCURACY = 0.105 * distance


                            if EQUAL_ACCURACY <= self.config.EQUAL_ACCURACY_MIN:
                                EQUAL_ACCURACY = self.config.EQUAL_ACCURACY_MIN
                            format_dict_array[idx]['y_equal_fuzzy']=False
                            if abs(format_dict_array[(idx+3+nodes_length)%nodes_length]['y'] - format_dict_array[(idx+4+nodes_length)%nodes_length]['y']) <= EQUAL_ACCURACY:
                                is_match_pattern=True

                # compare 4,3
                if is_match_pattern:
                    fail_code = 500
                    is_match_pattern = False
                    # only go left.
                    if abs(format_dict_array[(idx+4)%nodes_length]['y'] - format_dict_array[(idx+3)%nodes_length]['y']) < LINE_ACCURACY:
                        is_match_pattern = True
                    else:
                        slash_height = format_dict_array[(idx+3)%nodes_length]['y'] - format_dict_array[(idx+4)%nodes_length]['y']
                        #print("slash_height:", slash_height)
                        if slash_height < MAX_LEFT_MOUNTAIN_HEIGHT:
                            is_match_pattern = True

                if is_match_pattern:
                    fail_code = 600
                    is_match_pattern = False
                    # only go left.
                    if format_dict_array[(idx+4)%nodes_length]['x'] < format_dict_array[(idx+3)%nodes_length]['x']:
                        is_match_pattern = True

                # must match x axis same direction.
                if is_match_pattern:
                    fail_code = 700
                    x_array = []
                    y_array = []
                    for t_idx in range(rule_need_lines):
                        y_array.append(format_dict_array[(idx+t_idx) % nodes_length]['y'])
                        x_array.append(format_dict_array[(idx+t_idx) % nodes_length]['x'])
                    direction_flag = spline_util.is_same_direction_list(x_array,deviation=10)
                    if not direction_flag:
                        is_match_pattern=False


                if is_match_pattern:
                    if False:
                        for t_idx in range(5):
                            print(t_idx, "t_idx:",format_dict_array[(idx+t_idx)%nodes_length]['t'])
                            print(t_idx, "code:",format_dict_array[(idx+t_idx)%nodes_length]['code'])

                # check length
                if is_match_pattern:
                    fail_code = 800
                    body_length = abs(format_dict_array[(idx+1) % nodes_length]['y']-format_dict_array[(idx+0) % nodes_length]['y'])
                    leg_length = abs(format_dict_array[(idx+2) % nodes_length]['y']-format_dict_array[(idx+3) % nodes_length]['y'])
                    if body_length > 0:
                        leg_percent = int((leg_length/body_length)*100)
                        if leg_percent > MAX_LEG_LENGTH_PERCENT:
                            #print("leg_percent:",leg_percent)
                            is_match_pattern = False

                            # but.
                            underground_distance = format_dict_array[(idx+3) % nodes_length]['x']-format_dict_array[(idx+4) % nodes_length]['x']
                            if underground_distance >= MORE_LEG_LENGTH_UNDERGROUND_LENGTH:
                                if leg_percent < MORE_MAX_LEG_LENGTH_PERCENT:
                                    is_match_pattern = True

                # fix 搏/博/㙛/捕 誤拔問題。
                if is_match_pattern:
                    fail_code = 900
                    if format_dict_array[(idx+3)%nodes_length]['y_equal_fuzzy'] and format_dict_array[(idx+5)%nodes_length]['y_equal_fuzzy'] and format_dict_array[(idx+7)%nodes_length]['y_equal_fuzzy']:
                        fail_code = 910
                        if format_dict_array[(idx+2)%nodes_length]['x_equal_fuzzy'] and format_dict_array[(idx+4)%nodes_length]['x_equal_fuzzy'] and format_dict_array[(idx+6)%nodes_length]['x_equal_fuzzy']:
                            fail_code = 920
                            if abs(format_dict_array[(idx+8)%nodes_length]['y'] - format_dict_array[(idx+3)%nodes_length]['y']) < NEXT_HORIZONTAL_LINE_Y_ACCURACY:
                                fail_code = 930
                                is_match_pattern = False

                                # 在這情況下，希望可以拔掉「中甲」系列的小腳。
                                if format_dict_array[(idx+2+nodes_length)%nodes_length]['distance'] <= 130:
                                    fail_code = 940
                                    if format_dict_array[(idx+4+nodes_length)%nodes_length]['distance'] >= 200:
                                        fail_code = 950
                                        if format_dict_array[(idx+4+nodes_length)%nodes_length]['y_direction'] < 0 and format_dict_array[(idx+6+nodes_length)%nodes_length]['y_direction'] > 0:
                                            fail_code = 960
                                            # almost the same length.
                                            if abs(format_dict_array[(idx+4+nodes_length)%nodes_length]['distance'] - format_dict_array[(idx+6+nodes_length)%nodes_length]['distance']) < 10:
                                                fail_code = 970
                                                if format_dict_array[(idx-1+nodes_length)%nodes_length]['x_direction'] > 0:
                                                    fail_code = 980
                                                    if format_dict_array[(idx-1+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                                        if abs(format_dict_array[(idx+1)%nodes_length]['y'] - format_dict_array[(idx+5+nodes_length)%nodes_length]['y']) > 130:
                                                            is_match_pattern = True

                # fix 霵的「耳」 誤拔問題。
                if is_match_pattern:
                    fail_code = 1000
                    right_height = format_dict_array[(idx+0+nodes_length)%nodes_length]['distance']
                    # left 只放二個短邊。
                    left_height = format_dict_array[(idx+2+nodes_length)%nodes_length]['distance'] + format_dict_array[(idx+4+nodes_length)%nodes_length]['distance']
                    bottom_length = format_dict_array[(idx+3+nodes_length)%nodes_length]['distance']
                    # 第一段腿長，太長不拔。
                    if format_dict_array[(idx+2+nodes_length)%nodes_length]['distance'] >= 150:
                        fail_code = 1010
                        is_match_pattern = False
                    else:
                        # 第2段腿長，太短&向上時不拔。
                        if format_dict_array[(idx+4+nodes_length)%nodes_length]['distance'] <= 150:
                            fail_code = 1020
                            # 但向下時要拔
                            if format_dict_array[(idx+4+nodes_length)%nodes_length]['y_direction'] > 0:
                                is_match_pattern = False
                        else:
                            fail_code = 1030
                            if right_height > left_height and bottom_length > left_height:
                                fail_code = 1040
                                #print("1")
                                if format_dict_array[(idx-1+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                    fail_code = 1050
                                    #print("2")
                                    # 排除底為斜邊的「山」，
                                    if format_dict_array[(idx-1+nodes_length)%nodes_length]['x_direction'] < 0:
                                        is_match_pattern = False


                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#1:", fail_code)
                        pass
                    else:
                        print("match rule #1")
                        print(idx,"debug rule#1:",format_dict_array[idx]['code'])
                        pass

                #print(idx,"fail code:", fail_code)
                if is_match_pattern:
                    #print("match rule #1")
                    #print(idx,"code:",format_dict_array['code'][idx])
                    #print(idx,"code:",format_dict_array['code'])

                    new_x = format_dict_array[(idx+0)%nodes_length]['x']
                    new_y = format_dict_array[(idx+3)%nodes_length]['y']
                    new_x = format_dict_array[(idx+0)%nodes_length]['x']
                    new_y = format_dict_array[(idx+3)%nodes_length]['y']

                    old_code_string = format_dict_array[(idx+1)%nodes_length]['code']
                    #print("old_code_string:", old_code_string)
                    old_code_array = old_code_string.split(' ')
                    old_code_array[1] = str(new_x)
                    old_code_array[2] = str(new_y)
                    new_code = ' '.join(old_code_array)
                    format_dict_array[(idx+1)%nodes_length]['code'] = new_code
                    #format_dict_array['x'][(idx+1)%nodes_length] = new_x
                    format_dict_array[(idx+1)%nodes_length]['y'] = new_y
                    #print('update new code:',new_code)

                    target_index = (idx+3)%nodes_length
                    del format_dict_array[target_index]

                    # side effect after remove item.
                    if idx > target_index:
                        idx -= 1

                    nodes_length = len(format_dict_array)
                    target_index = (idx+2)%nodes_length
                    #print("nodes_length:", nodes_length)
                    #print("remove at index:", target_index)
                    del format_dict_array[target_index]

                    redo_travel=True
                    resume_idx = idx
                    break

        if redo_travel:
            # check close path.
            self.reset_first_point(format_dict_array, spline_dict)

        return redo_travel, resume_idx

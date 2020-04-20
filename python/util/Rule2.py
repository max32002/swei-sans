#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

class Rule(Rule.Rule):

# RULE # 2
# 拔角(左下) 6號洞
# PS: 因為 array size change, so need redo.

    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx):
        redo_travel=False

        MAX_LEG_LENGTH_PERCENT=19
        
        # 如果對面高於 300，則支援長尾巴。 for「﨑」裡的口.
        # BUT: 這個在 Thin weight 裡是 361-125=236 超短！
        MORE_LEG_LENGTH_NEIGHBOR_HEIGHT = 220

        MORE_LEG_LENGTH_PERCENT=26
        
        # for 佳 (regular), 會套到。右下要>70
        # 「集」的 Bold style, Y axis, 379-289=90
        MIN_NEIGHBOR_HEIGHT=90      
        
        UNDERGROUND_LENGTH=750      
        # for 匯，因為"佳"，沒套到.，for 謳，有點短 (X=957-465=492)
        # 改成 480, 會造成 集，沒有尾巴！
        LINE_ACCURACY=3

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

                is_match_pattern = False

                #print(idx,"debug rule2:",format_dict_array['code'][idx])
                # 拔腳

                #if format_dict_array['t'][(idx+0)%nodes_length] != 'c':
                if format_dict_array[(idx+1)%nodes_length]['t'] == 'l':
                    if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+3)%nodes_length]['t'] == 'l':
                            #if format_dict_array['t'][(idx+4)%nodes_length] != 'c':
                            is_match_pattern = True

                # compare 1,0
                if is_match_pattern:
                    fail_code = 10
                    is_match_pattern = False
                    # only go buttom
                    if abs(format_dict_array[(idx+1)%nodes_length]['y'] - format_dict_array[(idx+0)%nodes_length]['y']) < LINE_ACCURACY:
                        is_match_pattern = True

                if is_match_pattern:
                    is_match_pattern = False
                    # only go buttom
                    if format_dict_array[(idx+1)%nodes_length]['x'] < format_dict_array[(idx+0)%nodes_length]['x']:
                        is_match_pattern = True

                # compare 2,1
                if is_match_pattern:
                    fail_code = 100
                    is_match_pattern = False
                    # only go left.
                    if format_dict_array[(idx+2)%nodes_length]['y'] < format_dict_array[(idx+1)%nodes_length]['y']:
                        is_match_pattern = True

                if is_match_pattern:
                    is_match_pattern = False
                    # only go left.
                    if abs(format_dict_array[(idx+2)%nodes_length]['x'] - format_dict_array[(idx+1)%nodes_length]['x']) < LINE_ACCURACY:
                        is_match_pattern = True

                # compare 3,2
                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False
                    # only go buttom
                    if abs(format_dict_array[(idx+3)%nodes_length]['y'] - format_dict_array[(idx+2)%nodes_length]['y']) < LINE_ACCURACY:
                        is_match_pattern = True

                if is_match_pattern:
                    is_match_pattern = False
                    # only go buttom
                    if format_dict_array[(idx+3)%nodes_length]['x'] < format_dict_array[(idx+2)%nodes_length]['x']:
                        is_match_pattern = True

                # compare 4,3
                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False
                    # only go left.
                    if format_dict_array[(idx+4)%nodes_length]['y'] > format_dict_array[(idx+3)%nodes_length]['y']:
                        is_match_pattern = True

                if is_match_pattern:
                    is_match_pattern = False
                    # only go left.
                    if abs(format_dict_array[(idx+4)%nodes_length]['x'] - format_dict_array[(idx+3)%nodes_length]['x']) < LINE_ACCURACY:
                        is_match_pattern = True

                # must match x axis same direction.
                if is_match_pattern:
                    fail_code = 400
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

                previous_index = (idx+nodes_length-1) % nodes_length
                previous_x = format_dict_array[previous_index]['x']
                previous_y = format_dict_array[previous_index]['y']

                previous_2index = (idx+nodes_length-2) % nodes_length
                previous_2x = format_dict_array[previous_2index]['x']
                previous_2y = format_dict_array[previous_2index]['y']
                previos_ground_length = previous_x - previous_2x

                neighbor_height = previous_y - format_dict_array[idx]['y']

                # check leg length percent
                if is_match_pattern:
                    fail_code = 500
                    body_length = abs(format_dict_array[(idx+4) % nodes_length]['y']-format_dict_array[(idx+3) % nodes_length]['y'])
                    leg_length = abs(format_dict_array[(idx+2) % nodes_length]['y']-format_dict_array[(idx+1) % nodes_length]['y'])
                    if body_length > 0:
                        leg_percent = int((leg_length/body_length)*100)
                        if leg_percent > MAX_LEG_LENGTH_PERCENT:
                            #print("Fail leg_percent:", leg_percent)
                            #print("neighbor_height:", neighbor_height)
                            is_match_pattern = False

                            # from top go buttom.
                            if neighbor_height > 0:
                                if neighbor_height > MORE_LEG_LENGTH_NEIGHBOR_HEIGHT:
                                    # 右側高度夠長，允論較長的百分比。
                                    if leg_percent <= MORE_LEG_LENGTH_PERCENT:
                                        is_match_pattern = True
                                    

                                    if is_match_pattern == False:
                                        # for 磞 的粗體「石」左下角。
                                        # 因斜線讓左邊高度變短，尾巴占的百分比太大。
                                        leg_percent = int((leg_length/neighbor_height)*100)
                                        #print("Fail new leg_percent:", leg_percent)
                                        # 使用一般的百分比即可。
                                        if leg_percent <= MAX_LEG_LENGTH_PERCENT:
                                            is_match_pattern = True

                # 增加例外的case, ex: 佳 和 集
                if is_match_pattern:
                    fail_code = 600
                    # neighbor height 太短，就不拔腳。
                    #print("neighbor_height:", neighbor_height)

                    # from top go buttom.
                    if neighbor_height > 0:
                        if neighbor_height <= MIN_NEIGHBOR_HEIGHT:
                            is_match_pattern = False
                            
                            # but 地板夠長，還是要拔。for:匯
                            # 但「集」的粗體超長！
                            underground_distance = format_dict_array[(idx+0) % nodes_length]['x']-format_dict_array[(idx+1) % nodes_length]['x']
                            #print("underground_distance:", underground_distance)                            
                            if underground_distance > UNDERGROUND_LENGTH:
                                is_match_pattern = True

                                # match 超長地板，用這個判斷來區分 集和匯
                                if previos_ground_length > 0:
                                    if previos_ground_length < int(underground_distance/2):
                                        # 遇到 "集" 不拔
                                        is_match_pattern = False

                # fix 搏/博/㙛/捕 誤拔問題。
                if is_match_pattern:
                    fail_code = 700
                    y_equal_check = False
                    if format_dict_array[(idx+0)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+2)%nodes_length]['y_equal_fuzzy']:
                            if format_dict_array[(idx-2+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                if format_dict_array[(idx-4+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                    y_equal_check = True
                    if y_equal_check:
                        if abs(format_dict_array[(idx+0)%nodes_length]['y'] - format_dict_array[(idx-3+nodes_length)%nodes_length]['y']) < NEXT_HORIZONTAL_LINE_Y_ACCURACY:
                            is_match_pattern = False

                #print("fail code:", fail_code)
                if is_match_pattern:
                    #print("match rule #2")
                    #print(idx,"code:",format_dict_array['code'][idx])
                    #print(idx,"code:",format_dict_array['code'])

                    new_x = format_dict_array[(idx+4)%nodes_length]['x']
                    new_y = format_dict_array[(idx+1)%nodes_length]['y']

                    old_code_string = format_dict_array[(idx+1)%nodes_length]['code']
                    #print("old_code_string:", old_code_string)
                    old_code_array = old_code_string.split(' ')
                    old_code_array[1] = str(new_x)
                    old_code_array[2] = str(new_y)
                    new_code = ' '.join(old_code_array)
                    format_dict_array[(idx+1)%nodes_length]['code'] = new_code
                    format_dict_array[(idx+1)%nodes_length]['x'] = new_x
                    #format_dict_array['y'][(idx+1)%nodes_length] = new_y
                    #print('update new code:',new_code)

                    #print("nodes_length:", nodes_length)
                    target_index = (idx+3)%nodes_length
                    del format_dict_array[target_index]

                    # side effect after remove item.
                    if idx > target_index:
                        idx -= 1

                    nodes_length = len(format_dict_array)
                    target_index = (idx+2)%nodes_length
                    del format_dict_array[target_index]

                    redo_travel=True
                    resume_idx = idx
                    break

        if redo_travel:
            # check close path.
            self.reset_first_point(format_dict_array, spline_dict)

        return redo_travel, resume_idx

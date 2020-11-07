#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

class Rule(Rule.Rule):

# RULE # 2
# 拔角(左下) LEFT+BOTTOM
# PS: 因為 array size change, so need redo.

    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx):
        redo_travel=False

        MAX_LEG_LENGTH_PERCENT=22

        # 非中文的字，不需要去處理。
        if self.is_Latin():
            #print("latin unicode_int:", self.unicode_int)
            MAX_LEG_LENGTH_PERCENT=13
        if self.is_Hangul():
            #print("kr unicode_int:", self.unicode_int)
            MAX_LEG_LENGTH_PERCENT=13


        # 如果對面高於 300，則支援長尾巴。 for「﨑」裡的口.
        # BUT: 這個在 Thin weight 裡是 361-125=236 超短！
        #    : 在「闢」的口，右側是 212
        MORE_LEG_LENGTH_NEIGHBOR_HEIGHT = 205

        MORE_MAX_LEG_LENGTH_PERCENT=26
        
        # for 佳 (regular), 會套到。右下要>70
        # 「集」的 Bold style, Y axis, 379-289=90
        # PS: ver 1.030 版後，決定拔掉佳的左下角。
        #   : 所以這一個變數暫時沒在使用。
        MIN_NEIGHBOR_HEIGHT=90      

        # PS: ver 1.030 版後，決定拔掉佳的左下角。
        #   : 所以這一個變數暫時沒在使用。
        # for 匯，裡的"佳"，沒套到.，for 謳，有點短 (X=957-465=492)
        # 改成 480, 會造成 集，沒有尾巴！
        UNDERGROUND_LENGTH=750      

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

        DISABLE_LIST = "𩝐霞"
        travel_enable = True
        if self.unicode_int > 0:
            if chr(self.unicode_int) in DISABLE_LIST:
                travel_enable = False

        rule_need_lines = 5
        fail_code = -1
        if nodes_length >= rule_need_lines and travel_enable:
            for idx in range(nodes_length):
                if idx <= resume_idx:
                    # skip traveled nodes.
                    continue

                is_debug_mode = False
                #is_debug_mode = True

                if is_debug_mode:
                    debug_coordinate_list = [[184,295]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(8):
                        print(debug_idx-2,": values#2:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

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
                    # only go left
                    if format_dict_array[(idx+0)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+0)%nodes_length]['x_direction'] < 0:
                            is_match_pattern = True

                # compare dot+1
                if is_match_pattern:
                    fail_code = 210
                    is_match_pattern = False
                    # only go bottom
                    if format_dict_array[(idx+1)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+1)%nodes_length]['y_direction'] < 0:
                           is_match_pattern = True

                # compare dot+2
                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False
                    # only go left.
                    if format_dict_array[(idx+2)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                           is_match_pattern = True

                # dot# 2 match stroke width
                if is_match_pattern:
                    fail_code = 310
                    is_match_pattern = False
                    if format_dict_array[(idx+2)%nodes_length]['match_stroke_width']:
                        is_match_pattern = True

                # compare dot+3
                if is_match_pattern:
                    fail_code = 400
                    is_match_pattern = False
                    # only go up.
                    if format_dict_array[(idx+3)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+3)%nodes_length]['y_direction'] > 0:
                           is_match_pattern = True


                # compare dot-1
                if is_match_pattern:
                    fail_code = 410
                    is_match_pattern = False
                    # only go bottom.
                    if format_dict_array[(idx-1+nodes_length)%nodes_length]['x_equal_fuzzy']:
                        fail_code = 420
                        # PS: remarked, because of 「口」是對的，but for「中」或「虫」是錯的。
                        #if format_dict_array[(idx-1+nodes_length)%nodes_length]['y_direction'] < 0:
                        is_match_pattern = True

                # must match x axis same direction.
                if is_match_pattern:
                    fail_code = 500
                    x_array = []
                    y_array = []
                    for t_idx in range(4):
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

                # check leg length percent
                previos_ground_length = format_dict_array[(idx-2+nodes_length)%nodes_length]['distance']
                neighbor_height = format_dict_array[(idx-1+nodes_length)%nodes_length]['distance']
                body_length = format_dict_array[(idx+3+nodes_length)%nodes_length]['distance']
                leg_length = format_dict_array[(idx+1+nodes_length)%nodes_length]['distance']
                if is_match_pattern:
                    fail_code = 600
                    # 身體太短，排除。
                    if body_length < 30:
                        is_match_pattern = False

                if is_match_pattern:
                    fail_code = 601
                    # 腿太長，排除。
                    if leg_length >= 120:
                        is_match_pattern = False
                
                if is_match_pattern:
                    fail_code = 610
                    # 腿比身還長，排除。
                    if body_length < leg_length:
                        is_match_pattern = False

                if is_match_pattern:
                    fail_code = 620
                    # 身的高，必需比起始點高，不然「十」和「草」部會消失。
                    if format_dict_array[(idx+4) % nodes_length]['y'] <= (format_dict_array[(idx+1) % nodes_length]['y']+30):
                        is_match_pattern = False

                if is_match_pattern:
                    fail_code = 630

                    # 腿的比例太長，進行「排除」。
                    leg_percent = int((leg_length/body_length)*100)

                    if is_debug_mode:
                        print("Fail leg_percent:", leg_percent)
                        print("neighbor_height:", neighbor_height)
                        print("previos_ground_length:", previos_ground_length)
                        print("leg_height:", leg_length)
                        print("body_height:", body_length)

                        print("MORE_MAX_LEG_LENGTH_PERCENT:", MORE_MAX_LEG_LENGTH_PERCENT)
                        print("MORE_LEG_LENGTH_NEIGHBOR_HEIGHT:", MORE_LEG_LENGTH_NEIGHBOR_HEIGHT)
                        print("MAX_LEG_LENGTH_PERCENT:", MAX_LEG_LENGTH_PERCENT)

                    if leg_percent > MAX_LEG_LENGTH_PERCENT:
                        is_match_pattern = False

                        # 在被排除的情況下。
                        if is_match_pattern == False:
                            # 當遇到口造形時，應該可以進行拔腳。
                            # PS: 一定要加這一個前提，不然 門左邊會消失. 
                            if leg_percent <= MORE_MAX_LEG_LENGTH_PERCENT:
                                fail_code = 630
                                # 左右幾乎相等。
                                if abs(body_length - (neighbor_height+leg_length)) <= 10:
                                    is_match_pattern = True

                        # 在被排除的情況下。
                        if is_match_pattern == False:
                            # 使用 neighbor height 做比對.
                            if neighbor_height > 0:
                                fail_code = 640
                                if neighbor_height > MORE_LEG_LENGTH_NEIGHBOR_HEIGHT:
                                    fail_code = 650
                                    # 右側高度夠長，允許較長的百分比。
                                    if leg_percent <= MORE_MAX_LEG_LENGTH_PERCENT:
                                        is_match_pattern = True
                                    
                                    if is_match_pattern == False:
                                        fail_code = 660
                                        # for 「磞」、「薜」 的粗體「石」左下角。
                                        # 因斜線讓左邊高度變短，尾巴占的百分比太大。
                                        right_leg_percent = int((leg_length/neighbor_height)*100)
                                        #print("Fail new leg_percent:", right_leg_percent)
                                        # 使用一般的百分比檢查即可。
                                        if right_leg_percent <= MAX_LEG_LENGTH_PERCENT:
                                            is_match_pattern = True

                # 增加例外的case, ex: 佳 和 集
                # PS: ver 1.030 版後，決定拔掉佳的左下角。
                #   : 所以這一個變數暫時沒在使用。
                #if is_match_pattern:
                if False:
                    fail_code = 700
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
                    fail_code = 800
                    y_equal_check = False
                    if format_dict_array[(idx+0)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+2)%nodes_length]['y_equal_fuzzy']:
                            if format_dict_array[(idx-2+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                if format_dict_array[(idx-4+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                    y_equal_check = True
                    
                    if y_equal_check:
                        fail_code = 810
                        if abs(format_dict_array[(idx+0)%nodes_length]['y'] - format_dict_array[(idx-3+nodes_length)%nodes_length]['y']) < NEXT_HORIZONTAL_LINE_Y_ACCURACY:
                            is_match_pattern = False


                    if is_match_pattern == False:
                        # 在這情況下，希望可以拔掉「中甲」系列的小腳。
                        fail_code = 820
                        if format_dict_array[(idx+1+nodes_length)%nodes_length]['distance'] <= 120:
                            fail_code = 830
                            # 中/甲，是長的，但蹿的「串」是短的。
                            if format_dict_array[(idx-1+nodes_length)%nodes_length]['distance'] >= 120:
                                fail_code = 840
                                if format_dict_array[(idx-1+nodes_length)%nodes_length]['distance'] >= (2 * format_dict_array[(idx+1+nodes_length)%nodes_length]['distance']):
                                    if format_dict_array[(idx+4)%nodes_length]['y_equal_fuzzy']:
                                        fail_code = 850
                                        if format_dict_array[(idx+4)%nodes_length]['x_direction'] > 0:
                                            fail_code = 860
                                            if abs(format_dict_array[(idx+2)%nodes_length]['y'] - format_dict_array[(idx-1+nodes_length)%nodes_length]['y']) > 70:
                                                is_match_pattern = True
                # fix 「霞」誤拔問題。
                if is_match_pattern:
                    fail_code = 900
                    is_match_sunset_pattern = False
                    right_height = format_dict_array[(idx+1+nodes_length)%nodes_length]['distance'] + format_dict_array[(idx-1+nodes_length)%nodes_length]['distance'] + format_dict_array[(idx-3+nodes_length)%nodes_length]['distance']
                    # check #1: 右邊長。
                    if body_length > right_height:
                        fail_code = 910
                        is_match_sunset_pattern = True

                    # check #2: 外形. direction.
                    if is_match_sunset_pattern:
                        fail_code = 920
                        is_match_sunset_pattern = False
                        if format_dict_array[(idx-1+nodes_length)%nodes_length]['x_equal_fuzzy']:
                            if format_dict_array[(idx-2+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                if format_dict_array[(idx-3+nodes_length)%nodes_length]['x_equal_fuzzy']:
                                    if format_dict_array[(idx-4+nodes_length)%nodes_length]['y_equal_fuzzy']:
                                        is_match_sunset_pattern = True

                    # check #3: 外形. length.
                    if is_match_sunset_pattern:
                        fail_code = 930
                        is_match_sunset_pattern = False
                        if format_dict_array[(idx-1+nodes_length)%nodes_length]['match_stroke_width']:
                            if format_dict_array[(idx-2+nodes_length)%nodes_length]['distance'] > format_dict_array[(idx-1+nodes_length)%nodes_length]['distance']:
                                if format_dict_array[(idx-2+nodes_length)%nodes_length]['distance'] > format_dict_array[(idx-3+nodes_length)%nodes_length]['distance']:
                                    is_match_sunset_pattern = True

                    # check #4: 外形. position.
                    if is_match_sunset_pattern:
                        fail_code = 940
                        if abs(format_dict_array[(idx+1)%nodes_length]['x'] - format_dict_array[(idx-2+nodes_length)%nodes_length]['x']) <= 3:
                            if abs(format_dict_array[(idx+1)%nodes_length]['x'] - format_dict_array[(idx-3+nodes_length)%nodes_length]['x']) <= 3:
                                is_match_pattern = False

                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#2:", fail_code)
                        pass
                    else:
                        print("match rule #2")
                        print(idx,"debug rule#2:",format_dict_array[idx]['code'])
                        pass

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

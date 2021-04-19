filter_list = {}
def fileter_indicator(indicator_list, user_tag):
    tmp_list = []    
    for key in indicator_list:
        user_tag = key+"@"+user_tag
        if user_tag in filter_list:
            continue
        else:
            filter_list[user_tag] = 1
            tmp_list.append(key)
    return tmp_list
from cycle_time_custom import get_cycle_time
import pandas


input_df = pandas.read_csv('get_run.p.csv')
status_tag = ['f1p1_online_status', 'f1p2_online_status']

condition_dict = {'f1p1_online_status': '{f1p1_online_status} == 1', 'f1p2_online_status': '{f1p2_online_status} == 1'}
cycle_tag_dict = {'f1p1_online_status': 'f1p1_dol', 'f1p2_online_status': 'f1p2_dol'} 
time_unit_dict = {'f1p1_online_status': 'days', 'f1p2_online_status': 'days'} 
pattern_dict = {'f1p1_online_status': 'reset', 'f1p2_online_status': 'noreset'} 
round_dict = {'f1p1_online_status': 'no', 'f1p2_online_status': 'no'}
freq_dict = {'f1p1_online_status': 5, 'f1p2_online_status': 5}

response = get_cycle_time(input_df, status_tag, condition_dict, cycle_tag_dict, time_unit_dict, pattern_dict, round_dict,
                   freq_dict)





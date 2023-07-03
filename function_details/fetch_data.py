import requests
# import json

# url = 'http://10.26.50.124:31186/pi/fetch_summary'
# start_time = '2022-01-01 00:00:00'
# end_time = '2022-04-01 00:00:00'
# freq_mins = 5
# pi_tags = ["39XA151",  "39XA152",  "39HC131.S",  "39FI347",  "39DI348",  "39FI123",  "39TI203",  "39TI201",  "39TI199",  "39TI198",  "39PI101",  "39TI103",  "39FC145",  
#            "39FI125",  "39PI123",  "39PI118",  "39FC126",  "39FC127",  "39FC128",  "39FC129",  "39FI187",  "39FC158",  "39FI159",  "13FI197",  "84FI208",  "39FI186",  
#            "39FI162",  "39PI181",  "39PI180",  "39DI108",  "39DI111",  "39PI142",  "39PI143",  "39FC225",  "39FC226",  "39TC198"]

# headers= {"pi-server": "AZRAPT5164.phillips66.net", "username": "gharas", "password": "Ingenero2022"}



# params = {"start_time": start_time, "end_time": end_time, "freq_mins": freq_mins, "pi_tags": pi_tags}
def fetch_data(url, start_time,  end_time, freq_mins, pi_tags, pi_server, username,  password):
        params = {"start_time": start_time, "end_time": end_time, "freq_mins": freq_mins, "pi_tags": pi_tags}
        headers= {"pi-server": pi_server, "username": username, "password": password}
        response = requests.get(url=url, params=params, headers=headers)
        return response
    

# result = fetch_data(url, params, headers)
# result.json()

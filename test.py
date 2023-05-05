import requests
import json
import datetime

if __name__ == "__main__":

    '''test enter main window'''
    # data = {'username':'测试03'}
    # with requests.post(
    #     url="http://127.0.0.1:8082/v1/enter_main_window", 
    #     data=json.dumps(data), 
    # ) as r:
    #     print(r.text)
    #     print(r.status_code)

    '''test start game'''
    # data = {'song_id':1}
    # with requests.post(
    #     url="http://127.0.0.1:8082/v1/start_game", 
    #     data=json.dumps(data), 
    # ) as r:
    #     print(r.text)
    #     print(r.status_code)

    '''test end game'''
    data = {
        'user_id':'2',
        'user_name':'zc',
        'start_time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'end_time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'song_id':1,
        'score':9874,
        'combo':80,
    }
    with requests.post(
        url="http://127.0.0.1:8082/v1/end_game", 
        data=json.dumps(data), 
    ) as r:
        print(r.text)
        print(r.status_code)


    '''test sign up'''
    # data = {'username':'测试01'}
    # with requests.post(
    #     url="http://127.0.0.1:8082/v1/user/signup", 
    #     data=json.dumps(data), 
    # ) as r:
    #     print(r.text)
    #     print(r.status_code)

    '''test user update'''
    # data = {
    #     'username':'zc',
    #     'end_time_last_play':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'song_id':1
    # }
    # with requests.post(
    #     url="http://127.0.0.1:8082/v1/user/update", 
    #     data=json.dumps(data), 
    # ) as r:
    #     print(r.text)
    #     print(r.status_code)

    '''test play_record update'''
    # data = {
    #     'play_start_time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'play_end_time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'song_id':1,
    #     'user_id':1,
    #     'score':10000,
    #     'combo':99
    # }
    # with requests.post(
    #     url="http://127.0.0.1:8082/v1/play_record/update", 
    #     data=json.dumps(data), 
    # ) as r:
    #     print(r.text)
    #     print(r.status_code)

    '''test song update'''
    # data = {
    #     'song_id':1,
    #     'user_id_last_play':2,
    #     'end_time_last_play':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'score':7000,
    #     'combo':124
    # }
    # with requests.post(
    #     url="http://127.0.0.1:8082/v1/song/update", 
    #     data=json.dumps(data), 
    # ) as r:
    #     print(r.text)
    #     print(r.status_code)

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import re
from colorama import Fore
import random

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)

credentials = flow.run_console()
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

request = youtube.channels().list(
    part = "statistics",
    id = "UCO8TxmbM-0wAxXms2mONrYg"
)
response = request.execute()

print()

#播放清單內容處理
def youtube_playlistItems(playlistID):
    request = youtube.playlistItems().list(
        part= "snippet", 
        playlistId= playlistID ,
        maxResults = 50
    )
    response = request.execute()
    
    for i in range(len(response['items'])):
        print(response['items'][i]['snippet']['title'])

def youtube_playlistItemsInsert(playlistID,videoID,position):
    request = youtube.playlistItems().insert(
        part = "snippet",
        body = {
            "snippet":{
                "playlistId": playlistID,
                "position": position,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId":videoID
                }
            }
        }
    )
    response = request.execute()

def youtube_playlistItemsDelete(searched_id):
    request = youtube.playlistItems().delete(
        id = searched_id
    )
    response = request.execute()

def youtube_playlistItemsSearch(playlistID):
    request = youtube.playlistItems().list(
        part= "snippet", 
        playlistId= playlistID ,
        maxResults = 50
    )
    response = request.execute()
    
    key_word = input("輸入搜尋內容\n")
    
    print("以下為搜尋結果")
    for i in range(len(response['items'])):
        if (key_word in response['items'][i]['snippet']['description']
        or key_word in response['items'][i]['snippet']['title']):
            print(response['items'][i]['snippet']['title'])

def youtube_playlistItemsUpdate(playlistID,new_videoID,position):
    youtube_playlistItemsDelete(search_id(position))
    youtube_playlistItemsInsert(playlistID,new_videoID,position)

#id 搜尋
def search_id(playlistID,position: int):
    request = youtube.playlistItems().list(
        part= "snippet", 
        playlistId= playlistID ,
        maxResults = 50
    )
    response = request.execute()

    result = response['items'][position]['id']
    return result

def search_videoID(address):
    r1 = re.search(r'v=',address)
    r2 = re.search(r'&',address)
    start = r1.end()
    end = r2.start()
    id = address[start:end]
    return id

def search_playlistID(address):
    r1 = re.search(r'list=',address)
    r2 = re.search(r'&index',address)
    start = r1.end()
    if r2 == None:
        id = address[start:]
    else:
        end = r2.start()
        id = address[start:end]
    return id

def position_to_videoID(playlistID,position):
    request = youtube.playlistItems().list(
        part= "snippet", 
        playlistId= playlistID ,
        maxResults = 50
    )
    response = request.execute()
    
    return response['items'][position]['snippet']['resourceId']['videoId']

def id_to_videoID(playlistID,id):
    request = youtube.playlistItems().list(
        part= "snippet", 
        playlistId= playlistID ,
        maxResults = 50
    )
    response = request.execute()

    for i in range(len(response['items'])):
        if id == response['items'][i]['id']:
            return response['items'][i]['snippet']['resourceId']['videoId']

#playlist長度搜尋
def search_playlist_len(playlistID):
    request = youtube.playlistItems().list(
        part= "snippet", 
        playlistId= playlistID ,
        maxResults = 50
    )
    response = request.execute()
    
    return len(response['items'])

#使用者2
def print_youtube_playlistItems():
    try:
        print("查詢播放清單內容")
        playlist_address = input("輸入播放清單網址\n")
        playlistID = search_playlistID(playlist_address)
        youtube_playlistItems(playlistID)
        return True
    except:
        return False

def insert_youtube_playlistItems():
    try:
        print("新增播放清單影片")
        playlist_address = input("輸入播放清單網址\n")
        video_address = input("輸入影片網址\n")
        position = int(input("輸入位置\n"))
        position -= 1
        playlistID = search_playlistID(playlist_address)
        videoID = search_videoID(video_address)
        youtube_playlistItemsInsert(playlistID,videoID,position)
        return True
    except:
        return False

def delete_youtube_playlistItems():
    try:
        print("刪除播放清單影片")
        playlist_address = input("輸入播放清單網址\n")
        position = int(input("輸入影片位置\n"))
        position -= 1
        playlistID = search_playlistID(playlist_address)
        searched_id = search_id(playlistID,position)
        youtube_playlistItemsDelete(searched_id)
        return True
    except:
        return False

def search_youtube_playlistItems():
    print("搜尋播放清單內容")
    playlist_address = input("輸入播放清單網址\n")
    playlistID = search_playlistID(playlist_address)
    youtube_playlistItemsSearch(playlistID)

def modify_youtube_playlistItems():
    try:
        print("修改播放清單順序")
        playlist_address = input("輸入播放清單網址\n")
        origin_position = int(input("輸入原影片位置\n"))
        new_position = int(input("輸入欲放置位置\n"))
        origin_position -= 1
        new_position -= 1
        playlistID = search_playlistID(playlist_address)
        searched_id = search_id(playlistID,origin_position)
        videoID = position_to_videoID(playlistID,origin_position)
        youtube_playlistItemsDelete(searched_id)
        youtube_playlistItemsInsert(playlistID,videoID,new_position)
        return True
    except:
        return False

def random_youtube_playlistItems():
    try:
        print("打亂播放清單順序")
        playlist_address = input("輸入播放清單網址\n")
        playlistID = search_playlistID(playlist_address)
        playlist_len = search_playlist_len(playlistID)
        new_order = list(range(playlist_len))
        random.shuffle(new_order)
        id_list = []
        videoID_list = [] 
        for i in range(playlist_len):
            id_list.append(search_id(playlistID,new_order[i]))
            videoID_list.append(id_to_videoID(playlistID,id_list[i]))
        for i in range(playlist_len):
            youtube_playlistItemsDelete(id_list[i])
        for i in range(playlist_len):
            youtube_playlistItemsInsert(playlistID,videoID_list[i],i)
        return True
    except:
        return False

def playlistItems_function_table():
    func1 = Fore.YELLOW + "查詢播放清單內容  請按1"
    func2 = "新增播放清單影片  請按2"
    func3 = "刪除播放清單影片  請按3"
    func4 = "修改播放清單順序  請按4"
    func5 = "打亂播放清單順序  請按5"
    func6 = "搜尋關鍵字        請按6"
    func_end = "取消              請按0" + Fore.RESET
    print(func1,func2,func3,func4,func5,func6,func_end,sep = '\n')
    func = int(input())
    if func == 1:
        if print_youtube_playlistItems():
            pass
        else:
            print(Fore.RED + "輸入網址有誤" + Fore.RESET)
    elif func == 2:
        if insert_youtube_playlistItems():
            print(Fore.GREEN + "新增成功" + Fore.RESET)
        else:
            print(Fore.RED + "新增失敗" + Fore.RESET)
    elif func == 3:
        if delete_youtube_playlistItems():
            print(Fore.GREEN + "刪除成功" + Fore.RESET)
        else:
            print(Fore.RED + "刪除失敗" + Fore.RESET)
    elif func == 4:
        if modify_youtube_playlistItems():
            print(Fore.GREEN + "修改成功" + Fore.RESET)
        else:
            print(Fore.RED + "修改失敗" + Fore.RESET)
    elif func == 5:
        if random_youtube_playlistItems():
            print(Fore.GREEN + "修改成功" + Fore.RESET)
        else:
            print(Fore.RED + "修改失敗" + Fore.RESET)
    elif func == 6:
        search_youtube_playlistItems()
    else:
        pass
    print()

#播放清單處理
def youtube_playlistInsert(new_playlist_name,new_playlist_description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": new_playlist_name,
            "description": new_playlist_description,
            "tags": [
              "sample playlist",
              "API call"
            ],
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()

    return response['id']

def youtube_playlistUpdate(playlistID,title,description):
    request = youtube.playlists().update(
        part="snippet,status",
        body={
          "id": playlistID,
          "snippet": {
            "title": title,
            "description": description,
            "tags": [
              "updated playlist",
              "API FTW"
            ]
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()
    
def youtube_playlistDelete(playlistID):
    request = youtube.playlists().delete(
        id= playlistID
    )
    request.execute()

def youtube_playlistCopy(origin_playlistID,playlistID):
    request = youtube.playlistItems().list(
        part= "snippet", 
        playlistId= origin_playlistID ,
        maxResults = 50
    )
    response = request.execute()
    
    for i in range(len(response['items'])):
        videoID = response['items'][i]['snippet']['resourceId']['videoId']
        youtube_playlistItemsInsert(playlistID,videoID,i)

#使用者1
def create_youtube_playlist():
    print("新增播放清單")
    playlist_name = input("輸入播放清單名稱\n")
    description = input("輸入播放清單說明\n")
    youtube_playlistInsert(playlist_name,description)

def update_youtube_playlist():
    try:
        print("修改播放清單名稱")
        playlist_address = input("輸入播放清單網址\n")
        title = input("輸入新的播放清單標題\n")
        description = input("輸入新的播放清單說明\n")
        playlistID = search_playlistID(playlist_address)
        youtube_playlistUpdate(playlistID,title,description)
        return True
    except:
        return False

def delete_youtube_playlist():
    try:
        print("刪除播放清單")
        playlist_address = input("輸入播放清單網址\n")
        playlistID = search_playlistID(playlist_address)
        youtube_playlistDelete(playlistID)
        return True
    except:
        return False

def copy_youtube_playlist():
    try:
        print("複製播放清單")
        playlist_name = input("輸入新的播放清單名稱\n")
        description = input("輸入新的播放清單說明\n")
        playlistID = youtube_playlistInsert(playlist_name,description)
        origin_playlist_address = input("輸入被複製播放清單網址\n")
        origin_playlistID = search_playlistID(origin_playlist_address)
        youtube_playlistCopy(origin_playlistID,playlistID)
        return True
    except:
        return False

def playlist_function_table():
    func1 = Fore.YELLOW + "新增播放清單      請按1"
    func2 = "修改播放清單名稱  請按2"
    func3 = "刪除播放清單      請按3"
    func4 = "複製播放清單      請按4"
    end_func = "取消              請按0" + Fore.RESET
    print(func1,func2,func3,func4,end_func,sep = "\n")
    func = int(input())
    if func == 1:
        create_youtube_playlist()
    elif func == 2:
        if update_youtube_playlist():
            print(Fore.GREEN + "更新成功" + Fore.RESET)
        else:
            print(Fore.RED + "更新失敗" + Fore.RESET)
    elif func == 3:
        if delete_youtube_playlist():
            print(Fore.GREEN + "刪除成功" + Fore.RESET)
        else:
            print(Fore.RED + "刪除失敗" + Fore.RESET)
    elif func == 4:
        if copy_youtube_playlist():
            print(Fore.GREEN + "複製成功" + Fore.RESET)
        else:
            print(Fore.RED + "複製失敗" + Fore.RESET)
    else:
        pass
    print()

#使用者3 #跨清單處理
def playlist_to_playlist_item_movement():
    try:
        print("跨播放清單影片搬移")
        origin_playlist_address = input("輸入原影片所屬播放清單\n")
        origin_position = int(input("輸入原影片在播放清單位置\n"))
        new_playlist_address = input("輸入新播放清單網址\n")
        new_position = int(input("輸入預放置播放清單位置\n"))
        origin_position -= 1
        new_position -= 1
        origin_playlistID = search_playlistID(origin_playlist_address)
        videoID = position_to_videoID(origin_playlistID,origin_position)
        new_playlistID = search_playlistID(new_playlist_address)
        youtube_playlistItemsInsert(new_playlistID,videoID,new_position)
        id = search_id(origin_playlistID,origin_position)
        youtube_playlistItemsDelete(id)
        return True
    except:
        return False

def playlist_to_playlist_item_search():
    try:
        playlist_numbers = int(input("輸入欲查詢播放清單數量\n"))
        playlist_address_list = []
        playlistID_list = []
        for i in range(playlist_numbers):
            playlist_address_list.append(input("輸入播放清單網址\n"))
            playlistID_list.append(search_playlistID(playlist_address_list[i]))
            
        key_word_list = []
        key_word_list.extend(input("輸入搜尋內容\n").split())

        result = []
        for k in range(len(key_word_list)):
            result.append([])
            for j in range(len(playlistID_list)):
                request = youtube.playlistItems().list(
                part= "snippet", 
                playlistId= playlistID_list[j] ,
                maxResults = 50
                )
                response = request.execute()
            
                key_word = key_word_list[k].lower()    
                for i in range(len(response['items'])):
                    title = response['items'][i]['snippet']['title'].lower()
                    description = response['items'][i]['snippet']['description'].lower()
                    if (key_word in title or key_word in description):
                        result[k].append(response['items'][i]['snippet']['title'])

        final = []
        for i in range(len(result)):
            for j in range(len(result[i])):
                if not result[i][j] in final:
                    final.append(result[i][j])

        if len(final) == 0:
            print("查無結果")
        else:
            print("以下為搜尋結果")
            for i in range(len(final)):
                print(final[i])
        return True
    except:
        return False

def playlist_to_playlist_function_table():
    func1 = Fore.YELLOW + "搬移  請按1"
    func2 = "搜尋  請按2"
    end_func = "取消  請按0" + Fore.RESET
    print(func1,func2,end_func,sep = "\n")
    func = int(input())
    if func == 1:
        if playlist_to_playlist_item_movement():
            print(Fore.GREEN + "搬移成功" + Fore.RESET)
        else:
            print(Fore.RED + "搬移失敗" + Fore.RESET)
    elif func == 2:
        if playlist_to_playlist_item_search():
            pass
        else:
            print(Fore.RED + "搜尋失敗" + Fore.RESET)
    else:
        pass
    print()

#函式選擇
def function_choice():
    func1 = Fore.BLUE + "播放清單處理      請按1"
    func2 = "播放清單內容處理  請按2"
    func3 = "跨播放清單處理    請按3"
    end_func = "結束              請按0" + Fore.RESET
    print(func1,func2,func3,end_func,sep = "\n")
    func = int(input())
    if func == 1:
        playlist_function_table()
    elif func == 2:
        playlistItems_function_table()
    elif func == 3:
        playlist_to_playlist_function_table()
    else:
        print(Fore.GREEN + "結束" + Fore.RESET)
        return 0
    return function_choice()

def main():
    function_choice()
    #功能1  隨機順序(打亂順序)
    #功能2 複製播放清單
    #功能3 支援多關鍵字查詢

if __name__ == '__main__':
    main()


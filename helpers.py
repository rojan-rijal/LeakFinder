import requests, json, sys
from bs4 import BeautifulSoup

"""
credit: https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
"""
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""


def sendRequest(searchString, startNum):
    cse_result = []
    search_url = 'https://www.googleapis.com/customsearch/v1?key=GOOGLE_API_KEY&cx=GOOGLE_CSE_LINK&q=intext:"{0}"&start={1}'.format(searchString, startNum)
#    print search_url
    search_cse = requests.get(search_url)
    cse_result = json.loads(search_cse.text) # response here can have prezi, trello, and others.
    if 'items' not in cse_result:
        print("Nothing found. Please refine your search")
        sys.exit()
    else:
        return cse_result


"""
getWebsiteTitle(link) is used to grab
prezi/codepen and other links title. Along
with this, it will also include screenshot.
"""
def getWebsiteTitle(link):
    website_request = requests.get(link)
    website_response_parsed = BeautifulSoup(website_request.text, "lxml")
    try:
    	website_title = website_response_parsed.title.text
    except:
        website_title = 'No Title'
    return website_title

"""
getBoardName(id) is used to get Board Name for
a Trello card/board. It will return Access
Denied when the API returns 403. This is linked
with Trello API request (runTrelloApi)
"""
def getBoardName(id, cardOrNot):
    if cardOrNot:
        url = 'https://api.trello.com/1/cards/{0}/board'.format(id)
    else:
        url = 'https://api.trello.com/1/boards/{0}'.format(id)
    querystring = {"key":"TRELLO_API_KEY","token":"TRELLO_AUTH_KEY"}
    trello_api_request = requests.request("GET", url, params=querystring)
    try:
        trello_api_response = json.loads(trello_api_request.text)
        return trello_api_response['name']
    except:
        return "Access Denied"


"""
Used to find name of board titles. This is used to identify boards.
"""
def runTrelloApi(trelloArray):
    boards = []
    combined_response = []
    for link in trelloArray:
        combined_response.clear()
        if "/b/" in link:
            board_id = find_between(link, '/b/', '/')
            board_name = getBoardName(board_id, False)
            if board_name not in boards:
                if "Access Denied" not in board_name:
                    combined_response.append(board_name)
                    combined_response.append(link)
                else:
                    combined_response.append("Access Denied")
                    combined_response.append(link)
        elif "/c/" in link:
            card_id =  find_between(link, '/c/', '/')
            board_name = getBoardName(card_id, True)
            if board_name not in boards:
                if "Access Denied" not in board_name:
                    combined_response.append(board_name)
                    combined_response.append(link)
                else:
                    combined_response.append("Access Denied")
                    combined_response.append(link)
        boards.append(combined_response)
    return boards

def isFileEligible(fileLoc):
    file_lines = 0
    with open(fileLoc, 'r') as file:
       for line in file:
           file_lines += 1
    if file_lines <= 7:
       return False
    else:
       return True

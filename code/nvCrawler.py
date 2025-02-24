import os
import sys
import urllib.request
import datetime
import time
import json

client_id = 'i3xVuiED1QNsvhNKmvWd'
client_secret = 'AtE6FKk1C9'

#[CODE 1]

def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s]Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e :
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 2]
def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)     #[CODE 1]

    if(responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

#[CODE 3]
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt':cnt, 'title':title, 'description':description,
                       'org_link':org_link, 'link':org_link, 'pDate':pDate})
    return

#[CODE 0]
def main():
    node = 'news'  # 크롤링한 대상
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult = []
    
    jsonResponse = getNaverSearch(node, srcText, 1, 100)  #[CODE 2]
    if jsonResponse is None:
        print("API 요청에 문제가 있습니다. 프로그램을 종료합니다.")
        return
    
    total = jsonResponse.get('total', 0)  # 'total' 키가 없으면 기본값으로 0을 반환합니다.
    
    while jsonResponse and jsonResponse.get('display', 0) != 0:
        for post in jsonResponse.get('items', []):
            cnt += 1
            getPostData(post, jsonResult, cnt)   #[CODE 3]
            
        start = jsonResponse['start'] + jsonResponse.get('display', 0)
        jsonResponse = getNaverSearch(node, srcText, start, 100)   #[CODE 2]
        
    print('전체 검색 : %d 건' % total)
        
    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf-8') as outfile:  # 파일을 UTF-8로 인코딩합니다.
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
            
        outfile.write(jsonFile)
            
    print("가져온 데이터 : %d 건" % (cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))

if __name__ == '__main__':
    main()
import urllib.request
import datetime
import json
import pandas as pd

ServiceKey = "77694a57686b756d33366c69434b76"  # 서울 열린 데이터 광장 API 인증키

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def getFreeFormSuggestions():
    # 서울 열린 데이터 광장에서 자유형 제안 데이터를 가져오는 함수
    service_url = "http://openAPI.seoul.go.kr:8088/" + ServiceKey + "/json/OA-2563/1/5/"
    responseDecode = getRequestUrl(service_url)
    
    if responseDecode is None:
        return None
    else:
        try:
            jsonData = json.loads(responseDecode)
            return jsonData['OA-2563']['row']
        except Exception as e:
            print(e)
            return None

def saveToCSV(data, filename):
    # 데이터를 CSV 파일로 저장하는 함수
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print("데이터를 CSV 파일로 저장했습니다:", filename)

def main():
    # 메인 함수
    print("<< 서울시 자유형 제안 데이터를 수집합니다. >>")
    suggestions_data = getFreeFormSuggestions()
    if suggestions_data:
        saveToCSV(suggestions_data, 'seoul_freeform_suggestions.csv')

if __name__ == '__main__':
    main()

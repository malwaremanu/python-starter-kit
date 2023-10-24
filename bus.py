import requests

url = "https://prdenv.nuego.in/graphql"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

data = {
    "id": "GetSeatArrangmentQuery",
    "query": "query GetSeatArrangmentQuery($referenceNo: String!) { seatArrangementDetails(referenceNo: $referenceNo) { SeatNo Row Column IsLadiesSeat Available SeatType UpLowBerth BlockType RowSpan ColumnSpan SeatCategory SeatRate IsLowPrice OriginalSeatRate } }",
    "variables": {
        "referenceNo": "1010#983#2242#509#509#12765#25102023#11:55 PM#11:55 PM#2"
    }
}

response = requests.post(url, headers=headers, json=data, cookies={"CookieName": "CookieValue"})

# Check the response status and content
if response.status_code == 200:    
    bdata = response.json()    
    ndata = []
    for a in bdata['data']['seatArrangementDetails']:
        if a['Row'] in [2, 3, 4, 5] and a['IsLadiesSeat'] == False and a['Available'] == True:
            ndata.append([a['SeatNo'], a['OriginalSeatRate']])
    
    print(f"{len(ndata)} seats available with details as follows")
    for x in ndata:
        print(x)
else:
    print("Request failed with status code:", response.status_code)
    print(response.text)


import requests
from datetime import datetime
#cowin api--calendarByDistrict
base_cowin_url ="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")


def fetch_data_from_cowin(district_id):
    query_parameters = "?district_id={}&date={}".format(district_id,today_date)
    header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    final_url = base_cowin_url + query_parameters
    response = requests.get(final_url,headers=header)
    extract_availability_data(response)
    #print(response.text)

def extract_availability_data(response):
    response_json = response.json()
    for center in response_json["centers"]:
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["min_age_limit"] == 45 :
                message = "Pincode: {}, Name: {}, Slots: {}, Minimum Age: {}". format(
                    center["center_id"],center["name"], 
                    session["available_capacity_dose1"],
                    session["min_age_limit"]
            )
                send_message_telegram(message)                 


def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__groupid__",group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response)

if __name__ == "__main__":
    fetch_data_from_cowin(142)

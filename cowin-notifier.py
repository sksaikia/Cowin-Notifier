import requests
import time
from datetime import datetime,timedelta
from plyer import notification

user_age = 55
pincodes=["782411","782410"]
num_days = 6

print("Starting Search for vaccine slots")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while(True) :
    availbleCenters = 0

    #We have to search for all pincodes for all the given dates
    for pincode in pincodes:
        for date in actual_dates:
            #The API to hit for our operation
            URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            result = requests.get(URL, headers=header)
            #If the response is 200 then proceed
            if result.ok:
                response_json = result.json()
                #We have to search for available capacity in each session for each center
                for center in response_json['centers']:
                    for session in center['sessions']:
                        #If the condition is satisfied like the available capacity is not zero and age limit is also satisfied then print them
                        if (session['available_capacity']>0 and session['min_age_limit']<=user_age and session["date"] == date ):
                            availbleCenters = availbleCenters+1
                            print('Center Name : ' , center['name'])
                            print('Available slots : ' , session['available_capacity'])
                            print('Pincode : ' , pincode)
                            print('Vaccine Name : ' , session['vaccine'])
                            print('Date : ', session['date'])
                            print('----------------------------------')

                            centerName = center['name']
                            availbleSlots = session['available_capacity']
                            dateOfSlot = session['date']
                            vaccineName = session['vaccine']
                            #plyer is used here to notify people in desktop.
                            notification.notify(
                                title="Vaccine Slots Availble",
                                # the body of the notification
                                message=f"Center Name : {centerName} \n Availble slots : {availbleSlots} \n Vaccine Name : {vaccineName} \n Date : {dateOfSlot}",
                                #You can add a icon here also in the .ico format
                                # the notification stays for 5sec
                                timeout=5
                            )


            else:
                print("No Response")

    if availbleCenters==0:
        print("No availble slots in these areas...")
        notification.notify(
            title="No Vaccine Slots are available",
            # the body of the notification
            message="Sorry, there is no available slot in your area",
            # You can add a icon here also in the .ico format
            # the notification stays for 5sec
            timeout=5
        )
    else:
        print(f"Hurray. Found {availbleCenters} results...")
    #The process will resume after 300 seconds. That means we will make the APi call again after 5 minutes.
    time.sleep(300)
    print("Waited for 5 minutes. Start searching again")
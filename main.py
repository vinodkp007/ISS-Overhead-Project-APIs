import time
import requests
from datetime import datetime
import smtplib

MY_EMAIL = "YOUR MAIL"
PASS =     "YOUR MAIL PASSWORD"
MY_LAT = 12.288479
MY_LONG = 77.780533



#Your position is within +5 or -5 degrees of the ISS position.
def is_overHead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        return True

def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunset, sunrise)
    time_now = datetime.now()
    if time_now in range(sunrise, sunset):
        return True

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
while True:
    print("Running")
    if is_overHead() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASS)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="TO MAIL GOES HERE",
                                msg="Subject:ISS Over Your Head\n\nLOOK UP!!!!")

    time.sleep(60)







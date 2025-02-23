import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

# Constants
OPENWEATHER_API_KEY = "62df3f23cf6e7c0bb8f84b101683938a"       #Enter openweather api key   
TWILIO_ACCOUNT_SID = "ACacb8361b4b7f6255970f6d9c9ea4517c"      #Enter twilio account sid       
TWILIO_AUTH_TOKEN = "674f4e8d11d0adc4bae7292a12f62f2f"         #Enter twilio authentication token      
FROM_PHONE = "+1 681 419 6067"                                 #Enter the developer's temp number                                
TO_PHONE = "+91 8974657320"                                    #Enter twilio registered phone number to receive alert


# Fetch weather data
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

# Analyze flood risk
def analyze_flood_risk(data):
    weather = data['weather'][0]['description'].lower()
    rain = data.get('rain', {}).get('1h', 0)  # Rainfall in last 1 hour (mm)
    wind_speed = data['wind']['speed']  # Wind speed in m/s
    flood_risk = "Low"
    
    if "rain" in weather or "storm" in weather:
        if rain > 12 or wind_speed > 25:
            flood_risk = "Critical"
        elif rain > 5 or wind_speed > 20:
            flood_risk = "High"
        elif rain > 1 or wind_speed > 15:
            flood_risk = "Moderate"
        else:
            flood_risk = "Low"
        
        return f"Flood Risk Level: {flood_risk}"
    return None

# Send SMS alert 
def send_sms_alert(body):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=FROM_PHONE,
            to=TO_PHONE
        )
        print(f"SMS alert sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")


# Main function
def main():
    city = input("Enter your city: ")
    try:
        weather_data = fetch_weather_data(city)
        alert_message = analyze_flood_risk(weather_data)
        
        if alert_message:
            print("Flood Alert:")
            print(alert_message)
            send_sms_alert(alert_message)
        else:
            print("No flood risks detected.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

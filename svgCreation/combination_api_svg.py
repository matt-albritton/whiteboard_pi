from __future__ import print_function

from datetime import date, datetime, timedelta, timezone
from sportsreference.nba.schedule import Schedule as NBASchedule
from sportsreference.ncaab.schedule import Schedule as ncaabSchedule
import requests
import json
from contextlib import redirect_stdout
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

#Things to get
high = 0        #temps
low = 0
conditions = "scattered clouds"
cOpp = "GSW"    #celtics
cScore = 100
cOppScore = 95
yOpp = "Harv"   #yale bball
yScore = 50
yOppScore = 45
quoteLines = [] #quote
events = [['','']] *4 #calander

svgOut = ""


def getCeltics():
    global cOpp, cScore, cOppScore
    today = date.today()
    sch = NBASchedule('BOS', year = '2023')
    curGame = 0
    for i in range((len(sch.dataframe)-1), 0, -1):
        # print(i)
        # This is AWFULY SLOW to iterate through and compare. only max of 80ish rows, but still brutal.
        if sch.dataframe.iloc[i][2].date() < today- timedelta(days = 1):
            curGame=i
            break
    lastGame = sch.dataframe.iloc[curGame]
    # print(lastGame)
    cOppList = lastGame['opponent_name'].split()
    cOpp = cOppList[len(cOppList) - 1]
    print(f"cOp: {cOpp}")
    cScore = lastGame['points_scored']
    cOppScore = lastGame['points_allowed']

def getYale():
    global yOpp, yScore, yOppScore
    today = date.today()
    sch = ncaabSchedule('Yale', year = '2023')
    # print(sch.dataframe)
    curGame = 0
    # print(sch.dataframe.iloc[1]['datetime'])
    for i in range((len(sch.dataframe)-1), 0, -1):
        if sch.dataframe.iloc[i]['datetime'].date() < today- timedelta(days = 1):
            curGame=i
            break
    lastGame = sch.dataframe.iloc[curGame]
    # print(lastGame)
    yOpp = lastGame['opponent_name']
    yScore = lastGame['points_for']
    yOppScore = lastGame['points_against']

def getWeather():
    global high, low, conditions
    api_key = "c854070b0199d85ce752463f2956d40f"
    lat = "41.307826052089524"
    lon = "-72.92923991437938"
    url = "https://api.openweathermap.org/data/3.0/onecall?lat=%s&lon=%s&exclude=current,minutely,hourly,alerts&appid=%s&units=imperial" % (lat, lon, api_key)
    response = requests.get(url)
    data = json.loads(response.text)

    low = round(data['daily'][0]['temp']['min'])
    high = round(data['daily'][0]['temp']['max'])
    conditions = data['daily'][0]['weather'][0]['description'].capitalize()


def getQuote():
    global quoteLines
    url = "https://quotes.rest/qod?category=inspire&language=en"
    response = requests.get(url)
    data = json.loads(response.text)
   #  qLength = data["contents"]["quotes"][0]["length"]
   #  quoteList = data["contents"]["quotes"][0]["quote"].split()
   #  author = data["contents"]["quotes"][0]["author"]
    qLength = len("Your life does not get better by chance. It gets better by change.")
    quoteList = "Your life does not get better by chance. It gets better by change.".split()
    author = "Jim Rohn"
    quoteLines = []
    tempString = ""
    for i, word in enumerate(quoteList):
      tempString = tempString + word + " "
      if (i+1) % 5 == 0:
         quoteLines.append(tempString)
         # print(f"5 words gotten. Temp String = {tempString}")
         # print(quoteLines)
         tempString = ""
      if i == len(quoteList) - 1:
         quoteLines.append(tempString)
         quoteLines.append(f"-{author}")
         # print(f"last section gotten. Temp String = {tempString}")
         # print(quoteLines)



def getEvents():
    global events

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        maxTime = datetime.utcnow() + timedelta(days = 1)
        maxTime = maxTime.isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now, timeMax= maxTime,
                                              maxResults=4, singleEvents=True,
                                              orderBy='startTime').execute()
        gotEvents = events_result.get('items', [])
    
        if not gotEvents:
            print('No upcoming events found.')
            return
        i=0
        for event in gotEvents:
            startTime = event['start'].get('dateTime').split("T")[1].split("-")[0]
            start = datetime.strptime(startTime,"%H:%M:%S").strftime("%I:%M %p")
            # print(f"{start} {event['summary']}")
            events[i] = [start, event['summary']]
            i = i+1
    
    except HttpError as error:
        print('An error occurred: %s' % error)

def getAllAPIs():
   print("Getting today's data from APIs...")
   getCeltics()
   print(f'Celtics: {cScore} {cOpp}: {cOppScore}')
   getYale()
   print(f'Yale: {yScore} {yOpp}: {yOppScore}')
   getQuote()
   print (quoteLines)
   getWeather()
   print(f'{conditions} with a low of {low}°F and high of {high}°F')
   getEvents()
   for event in events:
       print(f"{event[1]} at {event[0]}")
   print("All data gathered.")


def doReplacments():
   global svgOut
   #open og file
   svgInFile = open("dash_og.svg", "r")
   svgIn = svgInFile.read()
   svgInFile.close()
   #replace with new data
   svgOut = svgIn.replace("Wednesday, Dec 14", date.today().strftime("%A, %b. %d"))
   svgOut = svgOut.replace("c1234", conditions)
   svgOut = svgOut.replace("HiT", str(high))
   svgOut = svgOut.replace("LoT", str(low))
   svgOut = svgOut.replace("Timberwolves", cOpp)
   svgOut = svgOut.replace("c11", str(cScore))
   svgOut = svgOut.replace("ac00", str(cOppScore))
   svgOut = svgOut.replace("y11", str(yScore))
   svgOut = svgOut.replace("Harvard", yOpp)
   svgOut = svgOut.replace("ay00", str(yOppScore))
   svgOut = svgOut.replace("T1", events[0][0])
   svgOut = svgOut.replace("E1", events[0][1])
   svgOut = svgOut.replace("T2", events[1][0])
   svgOut = svgOut.replace("E2", events[1][1])
   svgOut = svgOut.replace("T3", events[2][0])
   svgOut = svgOut.replace("E3", events[2][1])
   svgOut = svgOut.replace("T4", events[3][0])
   svgOut = svgOut.replace("E4", events[3][1])
   for i, line in enumerate(quoteLines):
      svgOut = svgOut.replace(f"L{str(i+1)}", line)
   for i in range(1,8):
      svgOut = svgOut.replace(f"L{str(i+1)}", "")



def main():
   print(date.today().strftime("%A, %b. %d"))
   getAllAPIs()
   doReplacments()
   with open('dashboard.svg', 'w') as f:
      with redirect_stdout(f):
         print(svgOut)



if __name__ == "__main__":
  main()
  

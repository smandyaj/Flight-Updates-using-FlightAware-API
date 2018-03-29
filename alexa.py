from __future__ import print_function
import base64
import urllib2
import json
import datetime

'''pullrequest demo'''
'''locked branch'''
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    event['session']['application']['applicationId'] = 'amzn1.ask.skill.7aab8c9b-10f8-4ec7-954b-4ce49b4a2ce8'
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
    if (event['session']['application']['applicationId'] !=
        '<APPLICATION ID>'):
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent_name)
    # Dispatch to your skill's intent handlers
    if intent_name == "FlightStatus":
        return flight_status(intent, session)
    elif intent_name == "FlightDetails":
        return flight_details(intent, session)
    elif intent_name == "InFlightInfo":
        return inflight_info(intent, session)
    elif intent_name == "AirportOperation":
        return airport_operation(intent, session)
    elif intent_name == "ZipcodeDetails":
        return zipcode_details(intent, session)
    elif intent_name == "AirlineInsight":
        return airline_insight(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Please say a flight number"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please say an airline (United, Delta, Jet Blue, Alaska, American, and Virgin) and flight number"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def flight_details(intent, session):
   
    speech_output = ""

   
    reprompt_text = ""
    should_end_session = False
    
    airline_name = intent['slots']['FlightNumber']['value']
    
    req = urllib2.Request("http://flightxml.flightaware.com/json/FlightXML2/AirlineInfo?airlineCode=%s" % airline_name)
    
    base64string = base64.encodestring('%s:%s' % ('<flighaware username>', '<Use your pwd>')).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string) 
    
    
    
    
    print(req)
    resp = urllib2.urlopen(req)

    data = json.loads(resp.read())
    
    name = data['AirlineInfoResult']['name']
    shortname = data['AirlineInfoResult']['shortname']
    callsign = data['AirlineInfoResult']['callsign']
    country = data['AirlineInfoResult']['country']
    
    speech_output = "Flight name is %s also known as %s or %s. It operates at %s" % (name,
                                                                                     shortname,
                                                                                     callsign,
                                                                                     country,
                                                                                     )
    
    return build_response({}, build_speechlet_response(
        "Flight Details", speech_output, "", True))

def airline_insight(intent, session):
   
    speech_output = ""

   
    reprompt_text = ""
    should_end_session = False
    
    from1 = intent['slots']['FlightNumberFrom']['value']
    to1 = intent['slots']['FlightNumberTo']['value']
    
    req = urllib2.Request("http://flightxml.flightaware.com/json/FlightXML2/AirlineInsight?origin=%s&destination=%s&reportType=1" %(from1,to1))
    
    base64string = base64.encodestring('%s:%s' % ('<flighaware username>', '<Use your pwd>')).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string) 
    
    
    
    
    print(req)
    resp = urllib2.urlopen(req)

    data = json.loads(resp.read())
    print(data)
    car = data['AirlineInsightResult']['data'][0]['carrier']
    percent = data['AirlineInsightResult']['data'][0]['percent']
    fare_min = data['AirlineInsightResult']['data'][0]['fare_min']
    fare_median = data['AirlineInsightResult']['data'][0]['fare_median']
    fare_max = data['AirlineInsightResult']['data'][0]['fare_max']
    
    speech_output = "The best carrier for the given source and destination is %s, with %s people opting for the airline it offers a minimum fare of %s dollars and median fare of %s dollars and maximum fare of %s dollars" % (car,
                                                                                     percent,
                                                                                     fare_min,
                                                                                     fare_median,
                                                                                     fare_max,
                                                                                     )
    
    return build_response({}, build_speechlet_response(
        "Flight Details", speech_output, "", True))


def zipcode_details(intent, session):
   
    speech_output = ""

   
    reprompt_text = ""
    should_end_session = False
    
    zipcode = intent['slots']['FlightNumber']['value']
    
    req = urllib2.Request("http://flightxml.flightaware.com/json/FlightXML2/ZipcodeInfo?zipcode=%s" % zipcode)
    
    base64string = base64.encodestring('%s:%s' % ('<flighaware username>', '<Use your pwd>')).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string) 
    
    
    
    
    print(req)
    resp = urllib2.urlopen(req)

    data = json.loads(resp.read())
    
    city = data['ZipcodeInfoResult']['city']
    state = data['ZipcodeInfoResult']['state']
    county = data['ZipcodeInfoResult']['county']

    
    speech_output = "The given zipcode belongs to %s city at %s State and %s County" % (city,
                                                                                     state,
                                                                                     county,
                                                                                     )
    
    return build_response({}, build_speechlet_response(
        "Flight Details", speech_output, "", True))

def inflight_info(intent, session):
   
    speech_output = ""
    reprompt_text = ""
    should_end_session = False
    
    airline_name = intent['slots']['FlightNumber']['value']
    
    req = urllib2.Request("http://flightxml.flightaware.com/json/FlightXML2/InFlightInfo?ident=%s" % airline_name)
    
    base64string = base64.encodestring('%s:%s' % ('<flighaware username>', '<Use your pwd>')).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string) 
    
    
    
    
    print(req)
    resp = urllib2.urlopen(req)

    data = json.loads(resp.read())
    
    flightid = data['InFlightInfoResult']['faFlightID']
    lat = data['InFlightInfoResult']['latitude']
    lon = data['InFlightInfoResult']['longitude']
    
    speech_output = "In Flight infomation, The flight id  %s Flying at %s Latitude and %s Longitude" % (flightid,
                                                                                     lat,
                                                                                     lon,
                                                                                     )
    
    return build_response({}, build_speechlet_response(
        "Flight Details", speech_output, "", True))

def airport_operation(intent, session):
   
    speech_output = ""
    reprompt_text = ""
    should_end_session = False
    
    airport_name = intent['slots']['FlightNumber']['value']
    print(airport_name)
    req = urllib2.Request("http://flightxml.flightaware.com/json/FlightXML2/CountAirportOperations?airport=%s" % airport_name)
    
    base64string = base64.encodestring('%s:%s' % ('<flighaware username>', '<Use your pwd>')).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string) 
    
    
    
    
    print(req)
    resp = urllib2.urlopen(req)

    data = json.loads(resp.read())
    enroute = data['CountAirportOperationsResult']['enroute']
    departed = data['CountAirportOperationsResult']['departed']
    scheduled_dep = data['CountAirportOperationsResult']['scheduled_departures']
    scheduled_arr = data['CountAirportOperationsResult']['scheduled_arrivals']
    
    speech_output = "%s flights are in transit right now, %s flights have departed. There are %s flights which are scheduled to takeoff and %s flights are scheduled to arrive for the Given Airport" % (enroute,
                                                                                     departed,
                                                                                     scheduled_dep,
                                                                                     scheduled_arr,
                                                                                     )
    
    return build_response({}, build_speechlet_response(
        "Flight Details", speech_output, "", True))

def flight_status(intent, session):

   # if 'Airline' not in intent['slots'] or 'FlightNumber' not in intent['slots']:
    #    return get_welcome_response()

    # hacking these classes in right now because AWS Lambda doesn't support an easy "import pytz" and I didn't upload it yet
    class TZ_UTC(datetime.tzinfo):

        def utcoffset(self, dt):
            return datetime.timedelta(0)

        def dst(self, dt):
            return datetime.timedelta(0)

        def tzname(self, dt):
            return "UTC"

    class TZ_PST(datetime.tzinfo):

        def utcoffset(self, dt):
            return datetime.timedelta(hours=-8) + self.dst(dt)

        def dst(self, dt):
            # DST starts last Sunday in March
            d = datetime.datetime(dt.year, 4, 1)   # ends last Sunday in October
            self.dston = d - datetime.timedelta(days=d.weekday() + 1)
            d = datetime.datetime(dt.year, 11, 1)
            self.dstoff = d - datetime.timedelta(days=d.weekday() + 1)
            if self.dston <=  dt.replace(tzinfo=None) < self.dstoff:
                return datetime.timedelta(hours=1)
            else:
              return datetime.timedelta(0)

        def tzname(self, dt):
            return "US/Pacific"

    #airline_name = intent['slots']['Airline']['value']
    #airline_code = ""

    # these happen to be airlines I care about right now, need to convert to a dict lookup or better
    #if airline_name == "united":
    #    airline_code = "UA"
    #elif airline_name == "delta":
    #    airline_code = "DL"
    #elif airline_name == "jet blue":
     #   airline_code = "JBU"
    #elif airline_name == "alaska" or airline_name == "alaska airlines":
        #airline_code = "ASA"
    #elif airline_name == "american" or airline_name == "american airlines":
     #   airline_code = "AAL"
    #elif airline_name == "virgin" or airline_name == "virgin america":
       # airline_code = "VRD"

   # ident = "%s%s" % (airline_code, intent['slots']['FlightNumber']['value'])
    ident = intent['slots']['FlightNumber']['value']
    print("HI:"+ident)
    req = urllib2.Request("http://flightxml.flightaware.com/json/FlightXML2/FlightInfo?ident=%s" % ident)
    
    base64string = base64.encodestring('%s:%s' % ('<flighaware username>', '<Use your pwd>')).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string) 
    
    
    
    print(req)
    resp = urllib2.urlopen(req)

    data = json.loads(resp.read())

    flights = data['FlightInfoResult']['flights']

    for flight in flights:
        estimated_arrival_time = datetime.datetime.fromtimestamp(int(flight['estimatedarrivaltime']))
        if estimated_arrival_time.date() == datetime.date.today():
            break

   # airline_name = intent['slots']['Airline']['value']
    flight_number = intent['slots']['FlightNumber']['value']

    speech_output = ""

    if flight['actualdeparturetime'] == 0:  # flight hasn't left yet
        filed_departure_time = datetime.datetime.fromtimestamp(int(flight['filed_departuretime']))
        delta = filed_departure_time - datetime.datetime.now()

        # FIXME this doesn't necessarily handle delays on departure? nor does it say on-time or late because FlightAware API sucks

        speech_output = "%s is departing %s for %s in %s hours and %s minutes" % (flight_number,
                                                                                     flight['originCity'],
                                                                                     flight['destinationCity'],
                                                                                     delta.seconds / (60*60),
                                                                                     (delta.seconds % (60*60)) / 60)

    elif flight['actualarrivaltime'] != 0:  # flight has already landed
        actual_arrival_time = datetime.datetime.fromtimestamp(int(flight['actualarrivaltime']))
        delta = datetime.datetime.now() - actual_arrival_time
        hours = delta.seconds / (60*60)

        speech_output = "%s arrived at %s %s%s%s minutes ago" % (flight_number,
                                                                            flight['destinationCity'],
                                                                            hours if hours > 0 else "",
                                                                            " hours and " if (hours > 1) else (" hour and " if (hours == 1) else ""),
                                                                            (delta.seconds % (60*60)) / 60)

    elif estimated_arrival_time > datetime.datetime.now():  # flight is in the air
        estimated_arrival_time = estimated_arrival_time.replace(tzinfo=TZ_UTC())
        estimated_arrival_time = estimated_arrival_time.astimezone(tz=TZ_PST())

        speech_output = "%s is arriving at %s on time at %s" % (flight_number,
                                                                   flight['destinationCity'],
                                                                   estimated_arrival_time.strftime("%H:%M")
                                                                   )
    else:
        speech_output = "Sorry, this flight doesn't match our parameters...check the logs"

    return build_response({}, build_speechlet_response(
        "Flight Status", speech_output, "", True))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

from twilio.rest import TwilioRestClient
def sms( words ):
  account = "ACbad6eee013f65641bcd8f784b916fc97"
  token = "6692f408dc3141156346acd35aa4e63e"
  client = TwilioRestClient( account, token )
  client.messages.create( body = words , to = "+18017917020", \
                                    from_ = "+13852442950" )

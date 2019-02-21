import decimal
import json
import africastalking
import requests

# Initialize SDK
username = "goldenmorn"    # use 'sandbox' for development in the test environment
api_key = "8d9fdea4fdfdab2be9019406007311ab9fdbd553194d89774dfad7628f385c24"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)

# This is a workaround for: http://bugs.python.org/issue16535
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

def checkTelco(number):
	prefix = number[0:6]
	telco_name = ''
	mtn_prefix = ['234703','234706','234803','234806','234813','234814','234816','234903','234906','234810']
	glo_prefix = ['234705','234805','234807','234811','234815','234905']
	etisalat_prefix = ['234809','234817','234818','234908','234909']
	airtel_prefix = ['234701','234708','234802','234808','234812','234902','234907']

	print("starting check")
	print(prefix)

	if (prefix in mtn_prefix):
		telco_name = 'mtn'
	elif (prefix in glo_prefix):
		telco_name = 'glo'
	elif (prefix in etisalat_prefix):
		telco_name = 'etisalat'
	elif (prefix in airtel_prefix):
		telco_name = 'airtel'
	else:
		telco_name = ''

	return telco_name
def send(number,message):
	phone_number = "234"+number[1:]
	telco_name = checkTelco(phone_number)
	if (telco_name == 'airtel'):
	    PARAMS = {
	        'username': "sponge",
	        'password': "sponge",
	        'smsc': 'Airtel_RECEIVE1',
	        'to': phone_number,
	        'from': '55332',
	        'text': message
	        }
	    req = requests.get("http://5.101.174.139:13035/cgi-bin/sendsms",params = PARAMS)
	    print(req)
	elif (telco_name == 'glo' or telco_name == 'mtn' or telco_name == "etisalat"):
	    # Initialize a service e.g. SMS
	    sms = africastalking.SMS

	    # Use the service synchronously
	    phone_number = "+"+phone_number
	    senderID = "cerealquizz"
	    try:
	        print("sending sms.....",sms,phone_number)
	        response = sms.send(message, [phone_number],senderID)
	        print(response)
	    except Exception as e:
	        print ('Encountered an error while sending: {0}'.format(str(e)))
	else:
	    pass

def sendSMS(number,name,f_phone,f_name):
	link = "http://jkgiftingseason.com/"
	# sending message to user
	print("Sending thank you sms to user")
	message = "Thanks {0}, Your donation will will go a long way in helping spread our message. Further donations can be made to Zenith Bank acct:1004807710. Reference: freelagos".format(name)
	send(number,message)

	# sending message to user
	if f_phone==None or f_name==None:
		pass
	else:
		print("Sending referal sms to friend")
		f_message = "Hello {0}, {1} believes you would like to support JK, click this link to make your donation. {2}".format(f_name,name,link)
		send(f_phone,f_message)

	print("done sending the two sms...")
	return True
	

	# sending message to friend

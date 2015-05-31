import json
import gspread
import facebook
from oauth2client.client import SignedJwtAssertionCredentials

# fetch from google doc
def fetch_from_GGdoc():
	json_key = json.load(open('Google_Auth.json'))
	scope = ["https://spreadsheets.google.com/feeds","https://docs.google.com/feeds/"]
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
	gc = gspread.authorize(credentials)

	ss = gc.open("LQD Confessions (Responses)")

	dict = ss.worksheet("Form Responses").get_all_values()

	reduced_list = [s[1] for s in dict if s[2] == 'roi']
	return reduced_list

def get_api(cfg):
	graph = facebook.GraphAPI(cfg['access_token'])
	return graph

def post_to_FB(msg):
	cfg = json.load(open('Facebook_Auth.json'))
	api = get_api(cfg)
	status = api.put_wall_post(msg.encode('utf-8'))


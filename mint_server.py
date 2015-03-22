from flask import Flask
from flask import request
import time
import datetime
import mintapi
import simplejson

app = Flask(__name__)

@app.route("/")
def home():
	return "Let's get minty, yeah!"

@app.route("/get_mint")
def get_mint_account():
	u = request.args.get('u')
	p = request.args.get('p')
	mint = mintapi.Mint(u, p)
	all_accounts = mint.get_accounts()

	# Need to sanitize python dates to be able to
	# convert to JSON
	
	for account in all_accounts:
		if 'closeDateInDate' in account:
			account['closeDateInDate'] = int(time.mktime(account['closeDateInDate'].timetuple()))
		if 'lastUpdatedInDate' in account:
			account['lastUpdatedInDate'] = int(time.mktime(account['lastUpdatedInDate'].timetuple()))
		if 'addAccountDateInDate' in account:
			account['addAccountDateInDate'] = int(time.mktime(account['addAccountDateInDate'].timetuple()))
		if 'fiLastUpdatedInDate' in account:
			account['fiLastUpdatedInDate'] = int(time.mktime(account['fiLastUpdatedInDate'].timetuple()))
	
	return simplejson.dumps(all_accounts)


if __name__ == "__main__":
    app.run()


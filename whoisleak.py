import whois
import argparse
import requests
import cfscrape
import json
import Image, ImageFont, ImageDraw
import time

def searching(url):

	search = whois.whois(url)
	return search.email

def consult(email):


	try:

		r = requests.get('https://hacked-emails.com/api?q='+email)

		if r.status_code is 200:

			result = json.loads(r.text)

			if result['status'] == 'found':

				print ("\033[1;31;40mYour email " + result['query'] + " has been leaked to the following repositories: \n")

				for leak in result['data']:

					print ("\033[0;37;40m[+] Database Leaked: " + leak['title'] + " | Date Leaked: " + leak['date_leaked'])

			elif result['status'] == "notfound":

				print ("\033[1;32;40mYour email" + result['query'] + " hasn't been leaked! \n")

		else:

			scraper = cfscrape.create_scraper()

			req = scraper.get("http://haveibeenpwned.com/api/v2/breachedaccount/"+email).content

			if req:

	                        result = json.loads(req)

				print "\033[1;31;40mYour email " + email + " has been leaked to the following repositories: \n"

				for leak in result:

					print "\033[0;37;40m[+] Database Leaked: " + leak['Title'] + " | Date Leaked: " + leak['BreachDate']

			else:

				print ("\033[1;32;40mYour email" + email + " hasn't been leaked! \n")
	except:

		print ("Some error occurred with queries leakeds.")

def checking():

	emails = searching(url)

	if emails is None:

		print ("\n")
		banner()

		print ("\033[1;32;40mYour domain email is hidden!")

	elif type(emails) is list:

		banner()

		for email in emails:

			consult(email)

	else:

		print ("\n")
		banner()
		consult(emails)

def banner():

	ShowText = 'For Educational Purpose Only'

	font = ImageFont.truetype('arialbd.ttf', 15) #load the font
	size = font.getsize(ShowText)  #calc the size of text in pixels
	image = Image.new('1', size, 1)  #create a b/w image
	draw = ImageDraw.Draw(image)
	draw.text((0, 0), ShowText, font=font) #render the text to the bitmap
	for rownum in range(size[1]):
		line = []
		for colnum in range(size[0]):
			if image.getpixel((colnum, rownum)): line.append(' '),
			else: line.append('#'),
		print (''.join(line))

	print ("Access the site https://databases.today to download the available leaks.\n")

if __name__ == '__main__':

	parsing = argparse.ArgumentParser(description="This tool queries the emails that registered the domain and verifies if they were leaked in some data leak.")
	required = parsing.add_argument_group('Required Argument')
	required.add_argument('-u','--url', help='Insert your domain url',required=True)
	args = parsing.parse_args()

	url = args.url

	checking()

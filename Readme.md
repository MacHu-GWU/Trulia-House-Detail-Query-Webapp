#Trulia House Detail Query Webapp

This is a simple web app to get house detail by address and zipcode from www.trulia.com. You just need to upload your address book in tab delimited format, and submit. Then you can get a json includes the house detail information you need.

###Web app url

http://10.255.145.57:8080/ (For weatherbughome internal use only. Cannot visit it from out side network)

###Address Format

If you want to add the apartment number, use #1023, don't use apt1023. It doesn't matter you have city or state name in the address. This is also a valid address:

	24007 Ridge Rd, Germantown, MD

###Zipcode Format

Only accept 5 digits zipcode

###Example input file (You can download one on the web app homepage)

	250 Deerwood Dr	76712
	12511 Royal Crown Dr	20876
	9203 Hunting Pines Pl	22032
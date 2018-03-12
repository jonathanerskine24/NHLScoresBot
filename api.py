import requests
import json
import datetime
# import test


def getDate():
	now = datetime.datetime.now()
	year = now.year
	month = now.month
	if month < 10:
		month = "0"+str(month)
	day = now.day
	if day < 10:
		day = "0"+str(day)
	date = "{}-{}-{}".format(year, month, day)
	return date

def returnData(page):
	response = requests.get(page)
	data = response.json()
	return data


# converts UST to ESD
def fixTime(time):
	hour = int(time[11:13])
	minute = time[14:16]
	# print "{}:{}".format(hour, minute)
	if (hour - 4) <= 0:
		hour = 12 + (hour - 4)
		return "{}:{} PM".format(hour, minute)
	else:
		if hour > 12:
			hour = (hour - 4) - 12
			if hour > 0:
				return "{}:{} PM".format(hour, minute)
			else:
				hour = 12 + hour
				return "{}:{} AM".format(hour, minute)


teamIDs = {
	"devils":"1","njd":"1",
	"islanders":"2", "nyi":"2",
	"rangers":"3", "nyr":"3",
	"flyers":"4", "phi":"4",
	"penguins":"5", "bitchpigeons":"5", "pens":"5", "pit":"5",
	"bruins":"6", "bos":"6",
	"sabres":"7", "buf":"7",
	"canadiens":"8", "habs":"8", "mtl":"8",
	"senators":"9", "ott":"9",
	"leafs":"10", "tor":"10",
	"hurricanes":"12", "car":"12",
	"panthers":"13", "pans":"13", "fla":"13",
	"lightning":"14", "tbl":"14",
	"capitals":"15", "caps":"15", "was":"15", "wsh":"15",
	"blackhawks":"16", "chi":"16",
	"redwings":"17", "det":"17",
	"predators":"18", "nsh":"18",
	"blues":"19", "stl":"19",
	"flames":"20", "cgy":"20",
	"avalanche":"21", "avs":"21", "col":"21",
	"oilers":"22", "edm":"22",
	"canucks":"23", "van":"23",
	"ducks":"24", "ana":"24",
	"stars":"25", "dal":"25",
	"kings":"26", "lak":'26',
	"sharks":"28", "sjs":"28",
	"cbj":"29", "bjs":"29", "blue jackets":"29",
	"wild":"30", "min":"30",
	"jets":"52", "wpg":"52",
	"coyotes":"53", "ari":"53",
	"vgk":"54", "knights":"54", "vegas":"54"
}

# /help
# returns a list of acceptable commands and their format 
# WORKS
def help(): 
	s = "/recap <yyyy-mm-dd>: recap of that days games\n/score <team> <yyyy-mm-dd>: get a teams score from a given day\n"
	s += "/test test\n"
	return s

def goalHelp():
	s = "/goal <team> <goalNumber> will return that goal from that teams last game\n\n/goal <team> <goalNumber> <date> will return that goal from that teams game on that day\n\nEnter 'last' in place of <goalNum> to see the last goal from that game"
	return s

def liveData(link):
	liveData = returnData(link)

	teams = liveData['liveData']['boxscore']['teams']
	linescore = liveData['liveData']['linescore']
	away = teams['away'];home = teams['home']
	currentPeriod = linescore['currentPeriod']

	if currentPeriod != 0:
		timeRemaining = linescore['currentPeriodTimeRemaining']
		finalPeriod = linescore['currentPeriodOrdinal']
	else:
		timeRemaining = "not started"
		finalPeriod = liveData["gameData"]['datetime']['dateTime']
		finalPeriod = fixTime(finalPeriod)

	if timeRemaining == "Final":
		if finalPeriod == "3rd":
			gameResult = "FINAL:"
		else:
			gameResult = "FINAL/{}:".format(finalPeriod)
	elif timeRemaining == "not started":
		gameResult = "{}".format(finalPeriod)
	else:
		gameResult = "{} {}".format(finalPeriod, timeRemaining)

	awayStats = linescore['teams']['away']; homeStats = linescore['teams']['home']

	awayPP = awayStats['powerPlay']; homePP = homeStats['powerPlay']
	awayNet = awayStats['goaliePulled']; homeStats['goaliePulled']
	awayTeamName = away['team']['name']; homeTeamName = home['team']['name']
	awayTeamAbbrev = away['team']['abbreviation']; homeTeamAbbrev = home['team']['abbreviation']
	awayGoals = awayStats['goals']; homeGoals = homeStats['goals']
	awayShots = awayStats['shotsOnGoal']; homeShots = homeStats['shotsOnGoal']
	# awayHits = awayStats['hits']; homeHits = homeStats['hits']

	result = ''
	result += "{}".format(gameResult)
	# result += "{}: {}\n".format(awayTeamName, awayGoals)
	# result += "  {} SOG\n".format(awayShots)
	# result += "{}: {}\n".format(homeTeamName, homeGoals)
	# result += "  {} SOG".format(homeShots)
	if awayPP == "true":
		result += "[{}]: {} {}: {}".format(awayTeamAbbrev, awayGoals, homeTeamAbbrev, homeGoals)
	elif homePP == "true":
		result += "\n{}: {} [{}]: {}".format(awayTeamAbbrev, awayGoals, homeTeamAbbrev, homeGoals)
	else:
		if timeRemaining != "not started":
			result += "\n{}: {} {}: {}".format(awayTeamAbbrev, awayGoals, homeTeamAbbrev, homeGoals)
		else:
			result += "\n{} @ {}".format(awayTeamAbbrev, homeTeamAbbrev)
	if timeRemaining != "not started":
		result += "\nSOG: {} | {}".format(awayShots, homeShots)
	return result



# /recap
# returns a list of the days scores
# WORKS // need to add times/game status
def dailySummary():
	date = getDate()
	result = historicalDailySummary(date)
	return result

# /recap <date>
# returns a list of scores from a given day
# WORKS // need to add game status (FINAL/FINAL(OT))
def historicalDailySummary(date):
	schedule = "https://statsapi.web.nhl.com/api/v1/schedule?date="+date
	response = requests.get(schedule)
	data = response.json()
	numGames = data['totalGames']
	summary = ""
	for i in range(0, numGames):
		liveLink = data['dates'][0]['games'][i]['link']
		link = "https://statsapi.web.nhl.com"+liveLink
		result = liveData(link)
		summary += result+'\n'
		if (i != numGames-1):
			summary += '\n'
	return summary

# /score <team>
# returns the score of a team currently playing, if not returns last final game score
# works... ***live to be tested***
def teamScore(team): 
	result = ''
	date = getDate()
	schedule = "https://statsapi.web.nhl.com/api/v1/schedule?teamId={}&startDate=2018-01-01&endDate={}".format(teamIDs[team.lower()], date)
	data = returnData(schedule)
	lastGameIndex = (data['totalGames'] - 1)
	lastGame = data['dates'][lastGameIndex]['games'][0]
	gameState = lastGame['status']['detailedState']
	if (gameState == "In Progress") | (gameState == "Final"):
		link = "https://statsapi.web.nhl.com"+lastGame['link']
		result = liveData(link)
	elif gameState == "Scheduled":
		lastGame = data['dates'][lastGameIndex-1]['games'][0]
		link = "https://statsapi.web.nhl.com"+lastGame['link']
		result = liveData(link)
	return result


# /score <team> <date>
# returns a teams score from a given day
# works //
def historicalTeamScore(team, date):
	result = ''
	schedule = "https://statsapi.web.nhl.com/api/v1/schedule?teamId="+teamIDs[team.lower()]+"&date="+date
	response = requests.get(schedule)
	data = response.json()
	try:
		games = data['dates'][0]['games'][0]
		link = "https://statsapi.web.nhl.com"+games['link']
		result = liveData(link)
		return result
	except IndexError:
		result = "That team did not play that day."
		return result

# /score <team> last
# returns a teams last final score
# WORKS // DONE
def teamLastScore(team):
	result = ''
	date = getDate()
	schedule = "https://statsapi.web.nhl.com/api/v1/schedule?teamId={}&startDate=2018-01-01&endDate={}".format(teamIDs[team.lower()], date)
	data = returnData(schedule)
	lastGameIndex = data['totalGames'] - 1
	print lastGameIndex
	lastGame = data['dates'][lastGameIndex]['games'][0]
	teams = lastGame['teams']
	gameState = lastGame['status']['detailedState']
	if gameState == "Final":
		result += "FINAL:\n"
		result += teams['away']['team']['name']+": "+str(teams['away']['score'])+'\n'
		result += teams['home']['team']['name']+": "+str(teams['home']['score'])+'\n'
		return result
	else:
		lastGame = data['dates'][lastGameIndex - 1]
		teams = lastGame['games'][0]['teams']
		result += "FINAL:\n"
		result += teams['away']['team']['name']+": "+str(teams['away']['score'])+'\n'
		result += teams['home']['team']['name']+": "+str(teams['home']['score'])+'\n'
		return result

# /standings <division>
# returns the current standings of a division
# WORKS // add games played.. make it not return as a phone number
def standings(division):
	i = 0
	result = ''
	divID = {"metro":0,"atlantic":1,"central":2,"pacific":3}
	standings = "https://statsapi.web.nhl.com/api/v1/standings"
	data = returnData(standings)
	x = data['records'][divID[division]]['teamRecords']
	for key in x:
		team = x[i]['team']['name']
		wins = x[i]['leagueRecord']['wins']
		losses = x[i]['leagueRecord']['losses']
		ot = x[i]['leagueRecord']['ot']
		pts = x[i]['points']
		result += "{} {}-{}-{} {}\n".format(team.encode('utf-8'), wins, losses, ot, pts)
		i = i +1
	return result

# /goal <team> <goalNumber>
# works.. not very well
def goalHighlight(team, goalNum): # fix this to work for live and not live games
	result = ''
	goals = {}; goalDescs = []
	i = 0; goalNumCt = 1
	date = getDate()
	schedule = "https://statsapi.web.nhl.com/api/v1/schedule?teamId={}&startDate=2018-01-01&endDate={}".format(teamIDs[team.lower()], date)
	data = returnData(schedule)
	lastGameIndex = data['totalGames'] - 1
	print lastGameIndex
	lastGame = data['dates'][lastGameIndex]['games'][0]
	gameState = lastGame['status']['detailedState']

	if gameState == "Scheduled":
		lastGameIndex = lastGameIndex - 1
		lastGame = data['dates'][lastGameIndex]['games'][0]

	link = data['dates'][lastGameIndex]['games'][0]['content']['link']
	content = returnData("https://statsapi.web.nhl.com/"+link)
	items = content['media']['milestones']['items']

	for key in items:
		if items[i]['title'] == "Goal":
			goalVideo = items[i]['highlight']['playbacks'][9]['url']
			blurb = items[i]['highlight']['blurb']
			goalDescs.append(blurb)
			goals.update({goalNumCt:goalVideo})
			goalNumCt = goalNumCt + 1
		i = i + 1


	if isinstance(goalNum, int):
		goalNum = goalNum
	else:
		goalNum = goalNumCt - 1

	result = ''
	try: 
		result += "{}\n".format(goalDescs[goalNum - 1])
		result += "{}".format(goals[goalNum])
	except IndexError:
		result += "No video for that goal found"
	return result


def teamGoalLast(team):
	schedule = "https://statsapi.web.nhl.com/api/v1/schedule?teamId={}&startDate=2018-01-01&endDate={}".format(teamIDs[team.lower()], date)
	data = returnData(schedule)
	lastGame = data['totalGames'] - 1



# /goal <team> last
# returns the last goal scored in the CURRENT LIVE or LAST FINAL  game 
# not built
# def goalHighlightLast(team):
	# get games from the first through date()
	# find last game
	# if last game = scheduled -> skip to next game
		# find last goal
		#return last goal
	# if last game = live ->
		#find last goal
		#return last goal
	# if last game = final ->
		#find last goal
		# return last goal

# /goal <team> <date> <goalnum>
# returns a given goal from a game on a given date... goal number or LAST for the last goal
# def historicalGoalHighlight(team, date, goalNum)
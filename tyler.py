import requests
key="<insert key here>"
IGN = "HULKSMASH1337" # 42 56 0.75
accountID = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+IGN+"?api_key="+key).json()["accountId"]
times = []

for index in [100*i for i in range(10)]:
    jso = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/"+accountID+"?beginIndex="+str(index)+"&api_key="+key).json()
    if len(jso["matches"]) == 0:
        break
    for match in jso["matches"]:
        times.append((match["timestamp"],match["gameId"]))

times = times[::-1]
endGames = []

# define a session: 5+ consecutive games, and 6+ hours pass between last game of session and first game of next session
consec = 0
for t in range(len(times)-1):
    consec+=1
    if times[t+1][0]-times[t][0] > 21600000: # over 6 hours. 1 hour = 3600000 ms
        if consec >= 5:
            endGames.append(times[t][1])
        consec = 0
    else:
        consec +=1

endGames.append(times[-1][1]) # append most recent game that hasn't been counted. no "next" session

def didTylerWin(num):
    jso = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/"+str(num)+"?api_key="+key).json()
    if jso["queueId"] != 420: # throw out non-ranked games. ranked=code 420 (xd)
        return "void"
    blueWin = jso["teams"][0]["win"] == "Win"
    for p in jso["participantIdentities"][:5]: # check if tyler was on blue team
        if p["player"]["summonerName"] == IGN:
            return blueWin
    return not blueWin

games = 0
wins = 0
for eg in endGames[:89]: # limit of 100 API requests. 100-1-10=89 left
    dtw = didTylerWin(eg)
    if dtw != "void":
        games+=1
        print(dtw)
        wins+=dtw

print(wins,games, wins/games)
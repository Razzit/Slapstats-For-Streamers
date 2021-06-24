# made by Razz :)
import json
import time
import glob
import os
import msvcrt as m

Home_key = "home"
Away_key = "away"
Stats_Key = "stats"

Score_key = "score"
Shots_key = "shots"
Saves_key = "saves"
FaceoffsWon_key = "faceoffs_won"
Takeaways_key = "takeaways"
Passes_key = "passes"
PossessionTime_key = "possession_time_sec"

#Note: this key is for a calculated field. Not present in json file.
FaceoffPercentage_key = "faceoffs_win_percentage"

def wait():
    m.getch()
    
def calculate_faceoff_percentage(homeFaceoffsWon, awayFaceoffsWon):
    #Calculate percentage of faceoffs
    homeFaceoffPercentage = 0
    if homeFaceoffsWon != 0:
        if awayFaceoffsWon == 0:
            homeFaceoffPercentage = 100
        else:
            homeFaceoffPercentage = (homeFaceoffsWon / (homeFaceoffsWon + awayFaceoffsWon)) * 100
    return homeFaceoffPercentage;

def write_file(data, teamName):
    fileName = teamName + "_stats" + ".txt"
    print('Getting Stats for Team Name: ' + teamName)
    # Write to file
    with open(fileName, "w") as f:
        #Goals
        print('Goals ' + str(data[Score_key]))
        f.write(str(data[Score_key]) + '\n')
        #Shots
        print('Shots ' + str(data[Shots_key]))
        f.write(str(data[Shots_key]) + '\n')
        #Saves
        print('Saves ' + str(data[Saves_key]))
        f.write(str(data[Saves_key]) + '\n')
        #Faceoff percentage
        print('Faceoff percentage ' + "{:.2f}".format(data[FaceoffPercentage_key]) + "%")
        f.write("{:.2f}".format(data[FaceoffPercentage_key]) + "%" + '\n')
        #Takeaways
        print('Takeaways ' + str(data[Takeaways_key]))
        f.write(str(data[Takeaways_key]) + '\n')
        #Passes
        print('Passes ' + str(data[Passes_key]))
        f.write(str(data[Passes_key]) + '\n')
        #Possession time
        print('Possession Time ' + time.strftime('%M:%S', time.gmtime(data[PossessionTime_key])) + '\n')
        f.write(time.strftime('%M:%S', time.gmtime(data[PossessionTime_key])) + '\n')
    print("Exported team '" + teamName + "' stats to " + fileName + "\n")

def tally_statistics(players, teamName):
    shots = 0
    saves = 0
    faceoffsWon = 0
    takeaways = 0
    passes = 0
    possessionTime = 0
    
    for player in players:
        stats = player[Stats_Key]
        #Check that keys exist, then append.
        if Shots_key in stats:
            shots += int(player[Stats_Key][Shots_key])
        if Saves_key in stats:
            saves += int(player[Stats_Key][Saves_key])
        if FaceoffsWon_key in stats:
            faceoffsWon += int(player[Stats_Key][FaceoffsWon_key])
        if Takeaways_key in stats:
            takeaways += int(player[Stats_Key][Takeaways_key])
        if Passes_key in stats:
            passes += int(player[Stats_Key][Passes_key])
        if PossessionTime_key in stats:
            possessionTime += int(player[Stats_Key][PossessionTime_key])
            
    #Return dictionary of stats
    return { Shots_key: shots,
             Saves_key: saves,
             FaceoffsWon_key: faceoffsWon,
             Takeaways_key: takeaways,
             Passes_key: passes,
             PossessionTime_key: possessionTime
            }

#Entry
max_file_modify_time = None
try:
    while True:
        list_of_files = glob.glob('./*.json')
        latest_file = max(list_of_files, key=os.path.getmtime)
        if max_file_modify_time == None or latest_file > max_file_modify_time:
            max_file_modify_time = latest_file
        else:
            time.sleep(3)
            continue
            
        with open(latest_file) as fp:
            print('Opened file name: ' + latest_file)
            data = json.load(fp)
            
            homePlayers = [];
            awayPlayers = [];
            for player in data['players']:
                if(player['team'] == Home_key):
                    homePlayers.append(player)
                else:
                    awayPlayers.append(player)

            homeStats = tally_statistics(homePlayers, Home_key)
            awayStats = tally_statistics(awayPlayers, Away_key)
            
            # Append Goals (Score).
            homeStats[Score_key] = data[Score_key][Home_key]
            awayStats[Score_key] = data[Score_key][Away_key]

            # Calculate and append face off percentage
            homeFaceoffPercentage = calculate_faceoff_percentage(homeStats[FaceoffsWon_key], awayStats[FaceoffsWon_key])
            awayFaceoffPercentage = 100 - homeFaceoffPercentage
            homeStats[FaceoffPercentage_key] = homeFaceoffPercentage
            awayStats[FaceoffPercentage_key] = awayFaceoffPercentage

            # Write to output files
            write_file(homeStats, Home_key)
            write_file(awayStats, Away_key)

            print("Exported successfully")
            #print("Press any key to continue...")
            
            print('Waiting for file updates. Press CTRL + C to exit.')
except KeyboardInterrupt:
    pass

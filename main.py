# Skribblscore aims to note the scores of each player as the game progresses and makes a graph out of it
import sys,json,time
import tkinter as tk
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import plotly.graph_objects as go # for plotly part
import plotly.express as px # for plotly part
import pandas as pd # for plotly part
import numpy as np #for matplotlib part
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg") #type: ignore


pwd = sys.path[0]
link = "https://skribbl.io/?3zGVXuWlwOb3"
games = dict() #Will store the data regarding each round. 
accuracyDict = dict() # Will store data regarding how accurate a player is and their total score.
endFile = open(pwd + "/skribblscore_result.txt", "w") # the program will store the results in orderly fashion in case in depth is needed.
graphSelection = 0

# ----------Portion of code that gets the input---------------START
firstWindow = tk.Tk()
firstWindow.title("Skribblscore")
firstWindow.geometry("420x100")
options = ['Plotly and Matplotlib','Matplotlib Only','Plotly only',"None"]
tk.Label(firstWindow, text="Enter the invite link if you have one", padx=5).grid(row = 0)
# following will keep donald duck as default. if clicked on it it will allow to change it,ie it clears the input
firstclick = True
def on_entry_click(event):
    # function that gets called whenever imageWord entry is clicked        
    global firstclick
    if firstclick: # if this is the first time they clicked it
        firstclick = False
        linkInput.delete(0, "end") # delete all the text in the entry

linkInput = tk.Entry(firstWindow) ; linkInput.insert(0,link) ; linkInput.bind('<FocusIn>', on_entry_click)
linkInput.grid(row=1)
cancel = tk.Button(text="Cancel",command=sys.exit)
cancel.grid(row=2,column=2)
variable = tk.StringVar(firstWindow)
variable.set(options[0])
graphOptions = tk.OptionMenu(firstWindow, variable,*options)
graphOptions.grid(row=2)

def updateInput():
    global link
    link = linkInput.get()
    firstWindow.destroy()
button_1 = tk.Button(text="Click to start!", command=updateInput)
button_1.grid(row=2,column=3)
# button_1.place(relx=0.85, rely=0.5, anchor=tk.CENTER)  
# Label Creation
firstWindow.mainloop()
# ----------Portion of code that gets the input---------------END


# ----------Portion of code that sets up the selenium driver---------------START
# Initial Setup : chromedriver and link
options = Options()
# Here Brave is used as the binary for the script. you can change the address to the chromium browser executable of your choice
options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
# here chromium driver for macos,64 bit is used. make sure to replace the chrome driver with the one that supports your operating system.(in the same directory)
driver_path = pwd + '/chromedriver' 
drvr = webdriver.Chrome(options = options, executable_path = driver_path)
# ----------Portion of code that sets up the selenium driver---------------END


# ----------The script will wait till the game actually starts. then the scraping bit will start. you are required to join and start game---------------START
drvr.get(link)
content = drvr.page_source
soup = BeautifulSoup(content,features="html.parser")
while soup.find('div',attrs={'id':'screenLobby','style':"display: none;"}) == None:
    time.sleep(5)
    content = drvr.page_source
    soup = BeautifulSoup(content,features="html.parser")
    continue
print("Game Started!")
# ---------------------------------------------------------------------------END




# ----------Scraping bit of the script---------------START
getScores = True
missingLength = 0 # missinglength in case a player leaves the game or experiences a disconnect
while(getScores):
    time.sleep(2)
    content = drvr.page_source
    soup = BeautifulSoup(content, features ='html.parser')
    getScores = soup.find('div',attrs={'id':'screenLobby','style':"display: none;"}) != None #if it is None it means we are in the lobby
    round = int(str(soup.find('div',attrs={'id':'round'}).text).replace('Round',"").strip()[0]) # type:ignore

    if round  not in games.keys(): # if the round just started
        players = []
        scorers = dict()
        missingLength = 0
        for player in soup.findAll('div',attrs={"class":"player"}):
            name = str(player.find('div',attrs={'class':'name'}).text).replace("(You)","").strip()
            score = player.find('div',attrs={'class':'score'}).text.replace("Points:",'').strip()
            if score.isnumeric() and '+' not in score:
                players.append((name, int(score)))
                scorers[name] = [int(score)]  
        games[round] = [players,scorers]
    else:
        # round is already taken. we need to note those who are gaining
        scorers = games[round][1]
        for player in soup.findAll('div',attrs={"class":"player"}):
            name = str(player.find('div',attrs={'class':'name'}).text).replace("(You)","").strip()
            score = player.find('div',attrs={'class':'score'}).text.replace("Points:",'').strip()
            if not '+' in score and score.isnumeric():
                s = int(score)
                # if a new player enters mid round
                if name not in scorers.keys():
                    scorers[name] = ([0] * (missingLength - 1) ) + [s]
                # if player left game and came back later
                if len(scorers[name]) < missingLength:
                    scorers[name] = scorers[name] + ([0] * (missingLength - len(scorers[name]) - 1)) + [s]
                elif scorers[name][-1] != s and s != 0:
                            scorers[name].append(s)
                            missingLength = max(len(scorers[name]),missingLength)
        games[round][1] = scorers
print("Game Ended!")
# ----------Scraping bit of the script---------------END

endFile.write("Games\n")
endFile.write(json.dumps(games))
endFile.write('\n\n\n')


# ----------DATA CLEANING AND PROCESSING---------------START
missingLength = 0 #here we use missinglength for fixing any bad values

##----------------- initialising accuracyDict 
for round in games.keys():
    players = games[round][0]
    scores = games[round][1]
    for name in scores.keys():
        if name not in accuracyDict.keys():
            arr = [0] * (missingLength - len(scores[name])) + scores[name] # add the missing round stuff, if it is initialisation nothing will happen.
            accuracyDict[name] = arr
        else:
            accuracyDict[name] = accuracyDict[name] +  scores[name]
            # if the updated score does not reflect proper length
            if len(accuracyDict[name]) < missingLength:
                accuracyDict[name] += [0] * ( missingLength - len(accuracyDict[name]))
            missingLength = max(len(accuracyDict[name]),missingLength)
##---------------------------------------

# # first cleansing
for name in accuracyDict.keys():
    arr = accuracyDict[name]
    if len(arr) < missingLength:
        arr = arr + ([0] * (missingLength - len(arr)))
    for i in range(1,len(arr)):
        if arr[i] == 0:
            arr[i] = arr[i - 1]
    accuracyDict[name] = arr


endFile.write("AccuracyDict - 1\n")
endFile.write(json.dumps(accuracyDict))
endFile.write('\n\n\n')


# Modifying accuracyDict to include the points in a proper manner
for name in accuracyDict.keys():
    arr = accuracyDict[name]
    pointsGainedEachPlay = []
    progressivePoints = []
    totalPointsGained = 0
    for i in range(1,len(arr)):
        diff = 0 if arr[i - 1] > arr[i] else arr[i] - arr[i - 1] 
        totalPointsGained += diff
        pointsGainedEachPlay.append(diff)
        if len(progressivePoints) != 0:
            progressivePoints.append(diff + progressivePoints[-1])
        else:
            progressivePoints.append(diff)
    accuracyDict[name] = [progressivePoints,pointsGainedEachPlay,totalPointsGained,0] # type [[int], [int], int]


# Cleanse 2 : in case a value was missed in any extreme case
for name in accuracyDict.keys():
    temp2 = accuracyDict[name][0]
    temp1 = accuracyDict[name][1]
    if len(temp2) < (missingLength - 1):
        accuracyDict[name][0] = accuracyDict[name][0] + ([accuracyDict[name][0][-1]] * (missingLength - len(accuracyDict[name][0])))
    if len(temp1) < missingLength:
        accuracyDict[name][1] = accuracyDict[name][1] + ([accuracyDict[name][1][-1]] * (missingLength - len(accuracyDict[name][1])))

# Counting how many wins each player has had in the play. A win here is if the person was first to answer
for ind in range(missingLength - 1):
    (maxAdd,win) = 0,''
    for name in accuracyDict.keys():
        val = accuracyDict[name][1][ind]
        if val  > maxAdd:
            maxAdd,win = val, name
    if win in accuracyDict.keys():
        accuracyDict[win][3] += 1

endFile.write("AccuracyDict - 2\n")
endFile.write(json.dumps(accuracyDict))
endFile.close()



#-----------plotting the data obtained using matplotlib. uncomment this section if you prefer individual graphs of each player.----------
if graphSelection == 0 or graphSelection == 1:
    plt.rcParams["figure.figsize"] = (50,50)  #type: ignore # Setting the plots to max width
    (max_i,max_j) = (3,4) if len(accuracyDict.keys()) > 8 else (2,4) if len(accuracyDict.keys()) > 4 else (2,2)
    fig, ax = plt.subplots(max_i, max_j)
    i = j = 0
    for a in accuracyDict.keys():
        y = np.array(accuracyDict[a][0])
        x = np.array(range(len(accuracyDict[a][0])))
        plt.xticks(x,x)
        for i_x,i_y in zip(x,y): #type: ignore
            ax[i,j].annotate("{}".format(i_y), (i_x, i_y + 30))

        ax[i, j].plot(x, y, '-go', mfc='black', mec='k')
        ax[i, j].set_title('{} - Total:{} - Wins : {}'.format(a,accuracyDict[a][2],accuracyDict[a][3]))
        i,j = (i + 1) % max_i, (j + 1) % max_j if (i + 1) % max_i == 0 else j
    plt.savefig(pwd + '/result.png')
    plt.show()
#-----------------------------------------------------------


#-----------This section is to be used if you prefer the plotly graph. Uncomment this and comment the matplotlib part
if graphSelection == 0 or graphSelection == 2:
    d = dict()
    fig = go.Figure() #type: ignore
    for key in accuracyDict.keys(): 
        l = len(accuracyDict[key][0])
        a = list(range(1,l + 1))
        if accuracyDict[key][3] != 0:
            d[key] = accuracyDict[key][3]
        fig.add_trace(go.Scatter(x=a,y=accuracyDict[key][0],name=(key))) #type: ignore


    data = pd.DataFrame(d,index=[0])
    accuracyDict = pd.DataFrame(d,index=[0])
    fig.write_image(pwd + "/scores.png")
    fig.show()
    fig = px.pie(data,values=d.values(),names=d.keys(),title="Scores distribution",)
    fig.update_traces(textinfo='label+value')
    fig.write_image(pwd + "/winners.png")
    fig.show()
# -------------------------------------------------------------------------------------------

# Skribblscore
## Python program to record skribbl.io scores with selenium for competitions
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Skribblscore is built with _ease of use_ in mind, and requires little to no user interaction. Just launch the program before you play and you will be presented with the scores in graphical format after the game.

## Features

- Works on public as well as private games
- Saves results of the game in text format (json)
- Option to choose from either plotly or matplotlib graphs
- Accuracy recording


## Usage:
Skribblscore uses Tkinter to first take input from the user who wants to record the scores:

- If the user wishes to play on a public game they can choose to leave the default link provided.
- Also, the option to get a graph drawn by either plotly or matplotlib is given.
[![Input Window](https://github.com/nandanhere/skribblscore/blob/main/readme/dialogWindow.pngr)](https://github.com/nandanhere/skribblscore/blob/main/readme/dialogWindow.png)


After clicking on the "Click to start!" button you will be directed to a new instance of your web browser.Click on Play! button and wait for the game to start. Skribblscore will automatically start scraping the scores when the game starts and stops when the game ends.
### Plotly Graphs
[![Graph1]( https://github.com/nandanhere/skribblscore/blob/main/result.png)](https://github.com/nandanhere/skribblscore/blob/main/result.png)
[![Graph2](https://github.com/nandanhere/skribblscore/blob/main/scores.png)](https://github.com/nandanhere/skribblscore/blob/main/scores.png)
### MatplotLib Graph
[![MatplotLib Graph](https://github.com/nandanhere/skribblscore/blob/main/readme/samplesc.png)](https://github.com/nandanhere/skribblscore/blob/main/readme/samplesc.png)

## Installation

Skribblscore requires selenium, tkinter, bs4 ,plotly,matplotlib and pandas be installed prior to use.
Install the dependencies and required imports.

```sh
pip install selenium
pip install tk
pip install bs4
pip install plotly
pip install pandas
pip install matplotlib
```
Run main.py in terminal or in a compiler of your choice.

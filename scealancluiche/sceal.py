
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class GaaMatch(object):

    def __init__(self, team1, colour1, team2, colour2):
        """
        
        Inputs
        ---------
        team1
            (str) Name of Team 1 (as appears in data file, eg D for Dublin)
        colour1
            (list) Pair of colour definitions, e.g 'r', 'opal', '#FFAA22'
        """
        self.halfTimeDuration_mins = 10
        
        self.data = None
        
        self.team1 = team1
        self.team2 = team2
        
        self.colour1 = colour1[:2]
        self.colour2 = colour2[:2]
        
        #Debugging code
        self.load_excel('MSFC_Final_DublinvMayo.xlsx')
        
    def load_csv(fn):
        """Untested"""
        
        cols = "Half Time Team Event Notes".split()
        usecols = np.arange(len(cols))
        data = np.loadtxt(team1, team2, usecols=usecols, dtype=str)

        team = data[:, cols.index('Team')]
        event = data[:,cols.index('Event')]
        
        score = self.parseScore(team, event)
        data = pd.DataFrame(data, columns=cols)
        pd.concat([data, score], axis=1)
        self.data = data
        
    def load_excel(self, fn):
        data = pd.read_excel(fn)
        
        team = data['Team'].as_matrix()
        event = data['Event'].as_matrix()
        
        score = self.parseScore(team, event)
        
        data = pd.concat([data, score], axis=1)
        self.data = data
        
        
    def parseScore(self, team, event):
        assert len(team) == len(event)  
        team1 = self.team1
        team2 = self.team2
        
        score = dict()
        score[team1] = np.zeros(len(team))
        score[team2] = np.zeros(len(team))
        
        for i in range(len(team)):
            t = team[i]
            e = event[i]
            if e == 'P':
                score[t][i:] += 1
            elif e == 'G':
                score[t][i:] += 3
                    
        #data = np.append(data, [score[team1], score[team2]], axis=1)
        arr = np.array([ score[team1], score[team2] ]).transpose()
        df = pd.DataFrame(arr, columns="Score1 Score2".split())
        return df
  
    
    def plotScoreHistory(self):
        
        half = self.data.loc[:, 'Half'].astype(float)
        time = self.data.loc[:,'Time'].astype(float)
        score1 = self.data.loc[:,'Score1'].astype(float)
        score2 = self.data.loc[:,'Score2'].astype(float)
        
        #Account for 2nd half being 10 minutes after the first
        idx = half == 2
        time[idx] += self.halfTimeDuration_mins
        
        c11 = self.colour1[0]
        c12 = self.colour1[1]
        c21 = self.colour2[0]
        c22 = self.colour2[1]
        
        plt.clf()
        plt.step(time, score1, '-', color=c11, lw=4, where='post')
        plt.plot(time, score1, color=c12, ls=':', drawstyle='steps-post', lw=4)
        plt.step(time, score2, '-', color=c21, lw=4, where='post')
        plt.plot(time, score2, color=c22, ls=':', drawstyle='steps-post', lw=4)

        #Fill between the lines
        if False:
            for i in range(len(data)):
                y1 = [score2[i], score2[i]]
                y2 = [score1[i], score1[i]]
                if score1[i] > score2[i]:
                    plt.fill_between(time[i:i+2], y1, y2, color=c12)
                else:
                    plt.fill_between(time[i:i+2], y2, y1, color=c22)  

        self.annotate()

    def annotate(self):
        half = self.data.loc[:, 'Half'].astype(float)
        time = self.data.loc[:,'Time'].astype(float)
        team = self.data.loc[:, 'Team']
        event = self.data.loc[:,'Event']
        score1 = self.data.loc[:,'Score1'].astype(float)
        score2 = self.data.loc[:,'Score2'].astype(float)
        
        #Account for 2nd half being 10 minutes after the first
        idx = half == 2
        time[idx] += self.halfTimeDuration_mins
        
        score = {self.team1:score1, self.team2:score2}
        
        for i in range(len(time)):
            tm = team[i]
            offset = .25
            if tm == self.team2:
                offset *= -1

            t = time[i]
            e = event[i]
            y = score[tm][i] + offset
            
                
            #import pdb; pdb.set_trace()
            if e in ['W', 'A']:
                markWide(t, y)
            elif e == 'Y':
                markCard(t, y, 'Y')
            elif e == 'R':
                markCard(t, y, 'R')
            elif e == 'B':
                markCard(t, y, 'B')
   
   
    def plotLead(self):
        half = self.data.loc[:, 'Half'].astype(float)
        time = self.data.loc[:,'Time'].astype(float)
        team = self.data.loc[:, 'Team']
        event = self.data.loc[:,'Event']
        score1 = self.data.loc[:,'Score1'].astype(float)
        score2 = self.data.loc[:,'Score2'].astype(float)

        #Account for 2nd half being 10 minutes after the first
        idx = half == 2
        time[idx] += self.halfTimeDuration_mins

        lead = score1 - score2
        
        plt.clf()
        c11 = self.colour1[0]
        c12 = self.colour1[1]
        c21 = self.colour2[0]
        c22 = self.colour2[1]

        plt.axhline(0, color='#222244', lw=2) 
        plt.step(time, lead, '-', color=c11, lw=4, where='post')
        plt.plot(time, lead, color=c12, ls=':', drawstyle='steps-post', lw=4)
  
        self.drawHalftime()
  
    def drawHalftime(self):
        half = self.data.Half.as_matrix()
        wh = np.where(half == 1)[0][-1]
        
        print self.data.iloc[wh]
        t1 = self.data.Time.iloc[wh]
        t2 = t1 + .5 * self.halfTimeDuration_mins

        plt.axvspan(t1, t2, color='#AAAAAA')
        
        plt.xlabel('Time', fontsize=16)
        plt.ylabel("Dublin's Lead", fontsize=16)
        

def markWide(t, y):
    plt.plot([t], [y], 'X', color='k')

    
    

def markCard(t, y, cardType):
    pass    



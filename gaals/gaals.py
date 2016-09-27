
import matplotlib.pyplot as mp
from fractions import Fraction
import scipy.special
import numpy as np
import re

def parse(fn):
    fp = open(fn)
    text = fp.readlines()

    team1 = []
    team2 = []
    score1 = []
    score2 = []
    for line in text:
        if not re.match("[0-9]", line):
            continue

        line = re.sub("New York", "NewYork", line)


        words = line.split()
        team1.append(words[4])
        score1.append(words[5])
        score2.append(words[7])
        team2.append(words[8])

    teamTotal = []
    teamTotal.extend(team1)
    teamTotal.extend(team2)
    teamList = np.array( teamTotal, dtype=str)
    teamList = np.unique(teamList)

    teamIndex = dict()
    for i,t in enumerate(teamList):
        teamIndex[t] = i

    numMatch = len(team1)
    numTeam = len(teamList)
    A = np.zeros( (numMatch, numTeam) )
    b = np.zeros( numMatch )

    for i in range(len(team1)):
        c1 = teamIndex[ team1[i]]
        c2 = teamIndex[ team2[i]]

        A[i, c1] = 1
        A[i, c2] = -1

        s1 = 3*float(score1[i][0]) + float(score1[i][2:])
        s2 = 3*float(score2[i][0]) + float(score2[i][2:])
        b[i] = s1-s2

    return teamList, A, b



def play():

    A = np.zeros((5,5))
    b = np.zeros((5,1))

    A = [ [ 1,-1, 0, 0, 0], \
          [ 0, 1, 0, 0, -1], \
          [ 0, 0, 1, -1, 0], \
          [ 1, 0, -1, 0, 0], \
          [ 0, 1, -1, 0, 0], \
          [ 0, 0,  0, 1, -1], \
        ]
    A = np.array(A)

    b = [1,5,2,3,-5, 5]
    b = np.array(b)

    print A, b
    print A.shape
    print b.shape
    print np.linalg.lstsq(A, b)[0]
    print np.linalg.lstsq(A, b)[1]


class Gaals():
    def __init__(self, fn='2015League.txt'):
        t, A, b = parse(fn)
        self.teamList = t
        self.A = A
        self.scoreDiff = b

        x = np.dot( np.matrix(A).I, b)
        x = np.array(x)[0]  #Convert to 1d array
        assert( np.fabs(np.mean(x)) < 1)
        self.teamRank = x

    def printRanks(self):
        x = self.teamRank
        t = self.teamList
        idx = np.argsort(x)[::-1]

        for team, value in zip(t[idx], x[idx]):
            print "%-12s %+.2f" %(team, value)

    def getPredictedScores(self):
        return np.dot(self.A, self.teamRank)

    def getResiduals(self):
        return self.scoreDiff - self.getPredictedScores()

    def getScatter(self):
        return np.std( self.getResiduals())

    def predict(self, teamA, teamB):
        iA = self.teamList == teamA
        iB = self.teamList == teamB

        x = self.teamRank
        score1 = x[iA]
        score2 = x[iB]

        prediction = score1-score2
        out = []

        msg = "%10s (%+3.1f) v %10s (%+3.1f): Prediction %+.1f" \
        %(teamA, score1, teamB, score2, prediction)
        out.append(msg)

        sigma = self.getScatter()
        #Computes integrated probability of winning team winning by
        #less than x points.
        erf = lambda x: .5 + .5*scipy.special.erf( \
            (x - prediction)/ (np.sqrt(2)*sigma))
        lwr = erf(-.5)
        mid = erf(+.5)

        out.append("%.1f %% %s wins " %(100*lwr, teamB))
        out.append("%.1f %% chance draw" %(100*(mid-lwr)))
        out.append("%.1f %% chance %s wins" %(100*(1-mid), teamA))

        return "\n".join(out)

    def plot1(self):
        bc = self.getResiduals()
        prediction = self.getPredictedScores()
        scoreDiff = self.scoreDiff

        #idx = np.argsort(bc)[::-1]
        idx = np.ones( len(bc), dtype=bool)
        mp.plot(bc[idx], 'ro-', label="Residual")
        mp.plot(scoreDiff[idx], 'ko-', label="Score difference")
        mp.plot(prediction, 'go-', label="Prediction")

        mp.legend(loc=0)
        #mp.plot

    def plotTeam(self, team):
        iA = np.where(self.teamList == team)[0]

        mp.clf()
        mp.ylabel(team)
        sigma = self.getScatter()
        for i, t in enumerate(self.teamList):
            iB = np.where(self.teamList == t)[0]
            prediction = self.teamRank[iA] - self.teamRank[iB]
            mp.errorbar(i, prediction[0], sigma, lw=2)

            A = self.A
            idx =np.logical_and(A[:, iA] != 0, A[:, iB] != 0)
            wh = np.where(idx)[0]
            #print wh
            if len(wh) == 1:
                actualScore = self.scoreDiff[wh]
                if A[wh, iA] < 0:
                    actualScore *= -1
                mp.plot(i, actualScore, 's', ms=14)

        mp.gca().xaxis.set_ticks(range(len(self.teamList)))
        mp.gca().xaxis.set_ticklabels(self.teamList)
        mp.xlim( -1, len(self.teamList)+1)

def main():
    t, A, b = parse('2016results.txt')


    inv = np.matrix(A).I

    mp.clf()
    mp.imshow(inv, interpolation="nearest", cmap=mp.cm.RdBu)
    mp.colorbar()
    #return

    #x = np.linalg.lstsq(A,b)[0]    #Unstable? Weird at least
    x = np.dot( np.matrix(A).I, b)
    x = np.array(x)[0]  #Convert to 1d array
    assert( np.fabs(np.mean(x)) < 1)
    bc = np.dot(A, x)

    idx = np.argsort(x)[::-1]
    #print idx
    #print t
    #print A
    #print b
    #print x
    #print bc

    print predict(t, x, "Dublin", "Donegal")
    print predict(t, x, "Dublin", "Kerry")
    print predict(t, x, "Dublin", "Tyrone")
    print predict(t, x, "Mayo", "Tyrone")
    print predict(t, x, "Dublin", "Mayo")

    #print predict(t, x, "Kerry", "Galway")
    #print predict(t, x, "Mayo", "Cork")
    #print ""
    #print predict(t, x, "Kerry", "Mayo")
    #print predict(t, x, "Dublin", "Donegal")
    #print predict(t, x, "Donegal", "Kerry")
    #print predict(t, x, "Dublin", "Monaghan")

    rms = np.std(b-bc)
    #print probability(t, x, "Dublin", "Derry", rms)
    #print probability(t, x, "Cork", "Mayo", rms)
    #print probability(t, x, "Kerry", "Monaghan", rms)
    #print probability(t, x, "Donegal", "Tyrone", rms)

    #mp.clf()
    #mp.plot(b, 'ko-', label="Points Diff")
    #mp.plot(bc, 'go-', label="Post hoc prediction")
    #mp.plot(b-bc, 'ro-', label="Difference")
    #print "Std is %.3f points" %(np.std( b-bc))
    #mp.legend(loc=0)


def predict(t, x, teamA, teamB):
    iA = t == teamA
    iB = t == teamB

    score1 = x[iA]
    score2 = x[iB]

    prediction = score1-score2
    return "%10s (%+3.1f) v %10s (%+3.1f): Prediction %+.1f" \
        %(teamA, score1, teamB, score2, prediction)


def probability(t, x, teamA, teamB, sigma):
    iA = t == teamA
    iB = t == teamB

    score1 = x[iA][0]
    score2 = x[iB][0]
    dScore  =  (score1-score2)

    #Computes integrated probability of winning team winning by
    #less than x points.
    erf = lambda x: .5 + .5*scipy.special.erf( (x - dScore)/ (np.sqrt(2)*sigma))
    lwr = erf(-.5)
    mid = erf(+.5)

    oddsLoss = oddsFromProbability(lwr)
    oddsDraw = oddsFromProbability(mid-lwr)
    oddsWin = oddsFromProbability(1-mid)
    print "%.1f %% chance (%s) of %s winning " %(100*lwr, oddsLoss, teamB)
    print "%.1f %% chance (%s) of a draw" %(100*(mid-lwr), oddsDraw)
    print "%.1f %% chance (%s) of %s winning" %(100*(1-mid), oddsWin, teamA)


def oddsFromProbability(frac):

    f = Fraction(frac).limit_denominator()
    a = f.numerator
    b = f.denominator

    div = float( min(a,b))
    a /= div
    b /= div
    return "%i/%i" %(b-a, b)

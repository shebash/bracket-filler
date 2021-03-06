import sys
import numpy
import pandas

eloFile = "best_elo_by_year_3.csv"
tourneyfile = "NCAA_Tourney_Data.csv"
teamNames = "teamnamematchset.csv"

tourney_names = ['YEAR','ROUND','SEED','TEAM','SCORE','OPP_SEED','OPPONENT','OPP_SCORE','RESULT']
teamNames_names = ['Games','NCAA']

eloDataset = pandas.read_csv(eloFile)
tourneyDataset = pandas.read_csv(tourneyfile)
namematchDataset = pandas.read_csv(teamNames)

namesHash = dict(zip(namematchDataset['NCAA'], namematchDataset['Games']))

# for k, v in namesHash.items():
#     print(k, v)

def nameswitch(x):
    return namesHash[x]

#print(tourneyDataset.head(20))

tourneyDataset['TEAM'] = tourneyDataset['TEAM'].map(nameswitch)
tourneyDataset['OPPONENT'] = tourneyDataset['OPPONENT'].map(nameswitch)

#eloDataset['score'] = 0

#print(eloDataset.head(20))

newset = tourneyDataset.merge(eloDataset,on=['TEAM','YEAR'])

eloDataset = eloDataset.rename(columns={'TEAM': 'OPPONENT', 'ELO': 'OPP_ELO'})
newerset = newset.merge(eloDataset,on=['OPPONENT','YEAR'])

def calcscore(j):
    if j['ELO'] > j['OPP_ELO'] and j['RESULT']=='WIN':
        return 1
    elif j['ELO']<j['OPP_ELO'] and j['RESULT']=='LOSS':
        return 1
    else:
        return -1


newerset['ELOSCORE'] = newerset.apply(calcscore,axis=1)

total_score = newerset['ELOSCORE'].sum()
print(total_score)

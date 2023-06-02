from geopy.distance import distance 

def pace2velocity(p):
    return (1000/60)/p

assert pace2velocity(10) == 1.666666666666666666

def v2p(v):
    return (1000/60)/v

assert v2p(1.666666666666666666) == 10

# Funktion som læser kontrolpunkterne fra .FIT filen
def read_from_fit(fname = r"C:\Users\TEC\source\repos\projektopgave\projektopgave\data\hok_klubmesterskab_2022\CA8D1347.FIT"):
    from fit_file import read
    points = read.read_points(fname)
    return points

punkter = read_from_fit()

run = list()
secondsRan = list()
metersRan = list()
walk = list()
metersWalked = list()
secondsWalked = list()
idle = list()
metersIdle = list()
secondsIdle = list()

def tempo_zones(msList, seconds, meters):

    for i, ms in enumerate(msList):
        if ms > pace2velocity(10):
            run.append(ms)
            secondsRan.append(seconds[i])
            metersRan.append(meters[i])
        if ms < pace2velocity(10) and ms > pace2velocity(50):
            walk.append(ms)
            secondsWalked.append(seconds[i])
            metersWalked.append(meters[i])
        elif ms < pace2velocity(50):
            idle.append(ms)
            secondsIdle.append(seconds[i])
            metersIdle.append(meters[i])

    global totalRanPercent
    global totalWalkedPercent
    global totalIdlePercent
    global totalPercentage
    
    totalRanPercent = round(sum(secondsRan) / sum(runtime) * 100, 1)
    totalWalkedPercent = round(sum(secondsWalked) / sum(runtime) * 100, 1)
    totalIdlePercent = round(sum(secondsIdle) / sum(runtime) * 100, 1)
    totalPercentage = totalIdlePercent + totalRanPercent + totalWalkedPercent

    totalMetersRan = sum(metersRan)
    totalMetersWalked = sum(metersWalked)
    totalMetersIdle = sum(metersIdle)
    totalMeters = totalMetersIdle + totalMetersRan + totalMetersWalked


    # print(round(sum(secondsRan) / sum(runtime) * 100, 1))
    # print(round(sum(secondsWalked) / sum(runtime) * 100, 1))
    # print(round(sum(secondsIdle) / sum(runtime) * 100, 1))
    # print(totalPercentage)

def printTable():
    d = {"Ran: ": [round(sum(metersRan), 1), sum(secondsRan), str(totalRanPercent) + " %"],
         "Walked: ": [round(sum(metersWalked), 1), sum(secondsWalked), str(totalWalkedPercent) + " %"],
         "Idle: ": [round(sum(metersIdle), 1), sum(secondsIdle), str(totalIdlePercent) + " %"],
         "Total: ": [round(sum(meterslist), 1), sum(runtime), str(round(totalPercentage, 1)) + " %"]
    }

    print("{:<8} {:<15} {:<10} {:<10}".format('','Meters','Seconds','Percentage'))
    for k, v in d.items():
         Meters, Seconds, Percent = v
         print ("{:<8} {:<15} {:<10} {:<10}".format(k, Meters, Seconds, Percent))
    
   
meterslist = list()
runtime = list()
vlist = list()
for i, p in enumerate(punkter[1:]):
    pp = punkter[i]

    dt = (p['timestamp'] - pp['timestamp']).seconds
    dd = distance( (pp['latitude'], pp['longitude']), (p['latitude'], p['longitude'])).meters

    # To calculate speed we divide distance by time.
    v = dd/dt
    vlist.append(v)
    runtime.append(dt)
    meterslist.append(dd)

tempo_zones(vlist, runtime, meterslist)
printTable()













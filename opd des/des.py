import salabim as sim
import pandas as pd
from scipy import stats
import statistics.stdev

sim.random_seed(10)

df = pd.read_excel('Assg_6_data.xlsx')
cols = list(df.columns)
data = [list() for i in range(3)]
for i in range(3):
    data[i] = df[cols[i]].tolist()

final_dist = list()

for i in range(3):
    arg_norm = stats.norm.fit(data[i])
    res_norm = stats.kstest(data[i], stats.norm.cdf, args = arg_norm)
    arg_expon = stats.expon.fit(data[i])
    res_expon = stats.kstest(data[i], stats.expon.cdf, args = arg_expon)

    if res_norm[1] > res_expon[1]:
        final_dist.append(sim.Normal(arg_norm[0], arg_norm[1]))
    else:
        final_dist.append(sim.Exponential(arg_expon[1]))
            
class patient1(sim.Component):  # <=30 years
    def process(self):
        self.enter(doc_waitline)
        if doctor.ispassive():
            doctor.activate()
        self.passivate()
        
        if self not in doc_waitline:
            self.enter(pharma_waitline)
            if pharma.ispassive():
                pharma.activate()
            self.passivate()
        
class patient2(sim.Component): # over 30 years of age
    def process(self):
        self.enter(nurse_waitline)
        if nurse.ispassive():
            nurse.activate()
        self.passivate()
        
        if self not in nurse_waitline:
            self.enter(doc_waitline)
            if doctor.ispassive():
                doctor.activate()
            self.passivate()
        
        if self not in doc_waitline and self not in nurse_waitline:
            self.enter(pharma_waitline)
            if pharma.ispassive():
                pharma.activate()
            self.passivate()
            
dtime = list()
ntime = list()
ptime = list()

class Doctor(sim.Component):
    def process(self):
        while True:
            while len(doc_waitline) == 0:
                self.passivate()
            self.patient = doc_waitline.pop()
            temp = final_dist[0].sample()
            dtime.append(temp)
            self.hold(temp)
            self.patient.activate()            

class Nurse(sim.Component):
    def process(self):
        while True:
            while len(nurse_waitline) == 0:
                self.passivate()
            self.patient = nurse_waitline.pop()
            temp = final_dist[1].sample()
            ntime.append(temp)
            self.hold(temp)
            self.patient.activate()            
    
class Pharma(sim.Component):
    def process(self):
        while True:
            while len(pharma_waitline) == 0:
                self.passivate()
            self.patient = pharma_waitline.pop()
            temp = final_dist[2].sample()
            ptime.append(temp)
            self.hold(temp)
            self.patient.activate()

               

time_spent = list()
dwait = list()
nwait = list()
pwait = list()
dutil = list()
nutil = list()
putil = list()
dts = list()
pts = list()
nts = list()

avg_timespent = list()
avgdwait = list()
avgnwait = list()
avgpwait = list()
avgdutil = list()
avgnutil = list()
avgputil = list()

for iter in range(100):
    for i in range(30):
        env = sim.Environment(trace=True)
        sim.ComponentGenerator(sim.Pdf((patient2, 0.6, patient1, 0.4)), iat=sim.Exponential(60/13), at=0, till=480)

        doctor = Doctor()
        nurse = Nurse()
        pharma = Pharma()

        nurse_waitline = sim.Queue("nurse_waitline")
        doc_waitline = sim.Queue("doc_waitline")
        pharma_waitline = sim.Queue("pharma_waitline")

        env.run()

        dwait.append(doc_waitline.length_of_stay.mean())
        pwait.append(pharma_waitline.length_of_stay.mean())
        nwait.append(nurse_waitline.length_of_stay.mean())

        dutil.append(sum(dtime))
        nutil.append(sum(ntime))
        putil.append(sum(ptime))

        dts = [dwait[i]+dutil[i]/len(dtime) for i in range(len(dwait))]
        pts = [pwait[i]+putil[i]/len(ptime) for i in range(len(pwait))]
        nts = [nwait[i]+nutil[i]/len(ntime) for i in range(len(nwait))]
        time_spent.append(sum(dts)/len(dts) + sum(pts)/len(pts) + sum(nts)/len(nts))

        env.reset_now()
        dtime = list()
        ptime = list()
        ntime = list()
    
    avg_timespent.append(sum(time_spent)/len(time_spent))
    avgdwait.append(sum(dwait)/(8*len(dwait)))
    avgpwait.append(sum(pwait)/(8*len(pwait)))
    avgnwait.append(sum(nwait)/(8*len(nwait)))
    avgdutil.append(sum(dutil)/len(dutil))
    avgnutil.append(sum(nutil)/len(nutil))
    avgputil.append(sum(putil)/len(putil))
    time_spent = list()
    dwait = list()
    pwait = list()
    nwait = list()
    dutil = list()
    putil = list()
    nutil = list()
    
        
    
print("Average time spent by patient in system: ", sum(avg_timespent)/len(avg_timespent))
print("Std Dev of time spent by patient in system: ", stdev(avg_timespent))

print("Average waiting time of patient for doctor: ", sum(avgdwait)/(len(avgdwait)))
print("Std dev of waiting time of patient for doctor: ", stdev(avgdwait))
print("Average waiting time of patient for nurse: ", sum(avgnwait)/(len(avgnwait)))
print("Std dev of waiting time of patient for nurse: ", stdev(avgnwait))
print("Average waiting time of patient for pharmacist: ", sum(avgpwait)/(len(avgpwait)))
print("Std dev of waiting time of patient for pharmacist: ", stdev(avgpwait))

print("Average Utilization of doctor: ", sum(avgdutil)/len(avgdutil))
print("Std Dev of Utilization of doctor: ", stdev(avgdutil))
print("Average Utilization of nurse: ", sum(avgnutil)/len(avgnutil))
print("Std Dev of Utilization of nurse: ", stdev(avgnutil))
print("Average Utilization of pharmacist: ", sum(avgputil)/len(avgputil))
print("Std Dev of Utilization of pharmacist: ", stdev(avgputil))

    
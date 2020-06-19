import math
import random as r
import pandas as blondish_panda
import numpy as np
import time as t



the_shorter_the_better = blondish_panda.read_excel('beer.xlsx')
##the_shorter_the_better.drop(['OG','FG'], axis=1)
boil_g_mean=np.mean(the_shorter_the_better['BoilGravity'])
the_shorter_the_better['BoilGravity']=the_shorter_the_better[['BoilGravity']].fillna(boil_g_mean)

Style = the_shorter_the_better['Style']
ABV = the_shorter_the_better['ABV']
IBU = the_shorter_the_better['IBU']
Color = the_shorter_the_better['Color']
BoilTime = the_shorter_the_better['BoilTime']
BoilGravity = the_shorter_the_better['BoilGravity']
Efficiency = the_shorter_the_better['Efficiency']

#-------special section made for configuration---------
How_many_robots = 50 ## Value must be >=1, first generation
duplicates = 2 ##How many copies (multiplied by 10) will be created from top 10 champions of previous gen
data_amount = 10 ##how many datas per robot used for training, can't be greater than beers_amount
testing_beers_count = 5000 ##amount of beers used to evaluate(test) a robot in the end
beers_amount = len(ABV)-testing_beers_count-0 ## total umber of beers in dataset, decrease (change the last int) to leave some untouched for comparison
SuperMutation = True ##Dangerous mutatuion, changing partners
SuperMutationAmount = 1 ##amount of super mutatuions
mods=2 ##amount of mutations in robots' dna per generation
powerX=3 ##max percentage of change in a mutation, 100 alllows for maximum mutations(from 1 to 0)
printstuff=True ##dev mode
passafter=True ## only print once
QNA = False ##print test results for each
chance=15 ## 1 in x for robot to become special (power 100)
# ------ end of section ------

#Current DNA form:

class Robot:
    def __init__(self,override=False):
        self.Perfection=0
        self.r1 = []
        self.r2 = []
        self.r3 = []
        self.r4 = []
        self.RobotID = 0
        self.Ale=[]
        self.IPA=[]
        self.Stout=[]
        self.Lager=[]
        self.Porter=[]
        self.Saison=[]
        self.Witbier=[]
        self.DNA1=[]
        self.DNA2=[]
        self.DNA3=[]
        self.DNA4=[]
        if override: self.Override=1
        else: self.Override=0

    def NodeAdd(self, x, y, m1, m2):

        v = float(x*m1+y*m2)
        #if v>0: return 1
        #else: return 0
        return v;

    #def NodeMultiply(self, x, y, m1, m2, whether): return float((x^m1*y^m2)*whether)
    #def NodeNothing(self, x, y, m1, m2, whether): return float(x*m1)

    def rf(self): ##random float
        return r.randint(-100,100)*0.01
##    def ri(self): ##random int
##        X = r.randint(0,1)
##        if X==0: M=-1
##        else: M=1
##        return M

    def Make_Buddies(self, mynr, total):
        buddies=[]
        for x in range(0,2):
            buddynr=r.randint(1,total)
            while buddynr==mynr:
                buddynr=r.randint(1,total)
            buddies.append(buddynr)
        return buddies

    def Receive_data(self,style,abv,ibu,color,boilt,boilg,eff):
        self.style=style
        self.r1.append(abv)
        self.r1.append(ibu)
        self.r1.append(color)
        self.r1.append(boilt)
        self.r1.append(boilg)
        self.r1.append(eff)
    def Clear_cache(self):
        self.r1=[]
        self.r2=[]
        self.r3=[]
        self.r4=[]

    def Recreate_beer_tabs(self):
        self.Ale=[]
        self.IPA=[]
        self.Stout=[]
        self.Lager=[]
        self.Porter=[]
        self.Saison=[]
        self.Witbier=[]

    def set_ID(self, x): self.RobotID = x
    def get_ID(self): return self.RobotID

    def Create_DNA_1(self):
        nr = 0
        for x in self.r1:

            w1 = self.rf()
            w2= self.rf()
            w3=self.rf()

            mynumber= nr
            nr+=1
            mybuddies = self.Make_Buddies(mynumber,len(self.r1))

            b1=mybuddies[0]-1
            b2=mybuddies[1]-1

            DNA = [b1,b2, w1,w2,w3]
            self.DNA1.append(DNA)
    def Create_DNA_2(self):
        nr = 0
        for x in self.r2:

            w1 = self.rf()
            w2= self.rf()
            w3=self.rf()

            mynumber= nr
            nr+=1
            mybuddies = self.Make_Buddies(mynumber,len(self.r2))

            b1=mybuddies[0]-1
            b2=mybuddies[1]-1

            DNA = [b1,b2, w1,w2,w3]
            self.DNA2.append(DNA)
    def Create_DNA_3(self):
        nr = 0
        for x in self.r3:

            w1 = self.rf()
            w2= self.rf()
            w3=self.rf()

            mynumber= nr
            nr+=1
            mybuddies = self.Make_Buddies(mynumber,len(self.r3))

            b1=mybuddies[0]-1
            b2=mybuddies[1]-1

            DNA = [b1,b2, w1,w2,w3]
            self.DNA3.append(DNA)
    def Create_DNA_4(self):
        for x in self.r4:
            w = self.rf()
            self.DNA4.append(w)

    def Layer_One(self):
        for x in range(0,len(self.r1)-1):
            try:
                value1 = self.r1[x]
                value2 = self.r1[self.DNA1[x][0]]
                value3 = self.r1[self.DNA1[x][1]]
                weight1 = self.DNA1[x][2]
                weight2 = self.DNA1[x][3]
                weight3 = self.DNA1[x][4]
            except:
                #print(x,'<-x ',self.DNA1[x][0],' <-0',self.DNA1[x][1],' <-1',self.DNA1[x][2],' <-2',self.DNA1[x][3],' <-3',self.DNA1[x][4],' <-4')
                #oops=1/0
                None

            result1 = self.NodeAdd(value1,value2,weight1,weight2)
            result2 = self.NodeAdd(value1,value3,weight1,weight3)

            self.r2.append(result1)
            self.r2.append(result2)

    def Layer_Two(self):
        for x in range(0,len(self.r2)-1):
            value1 = self.r2[x]
            value2 = self.r2[self.DNA2[x][0]]
            value3 = self.r2[self.DNA2[x][1]]
            weight1 = self.DNA2[x][2]
            weight2 = self.DNA2[x][3]
            weight3 = self.DNA2[x][4]

            result1 = self.NodeAdd(value1,value2,weight1,weight2)
            result2 = self.NodeAdd(value1,value3,weight1,weight3)

            self.r3.append(result1)
            self.r3.append(result2)
    def Layer_Three(self):
        for x in range(0,len(self.r3)-1):
            value1 = self.r3[x]
            value2 = self.r3[self.DNA3[x][0]]
            value3 = self.r3[self.DNA3[x][1]]
            weight1 = self.DNA3[x][2]
            weight2 = self.DNA3[x][3]
            weight3 = self.DNA3[x][4]


            result1 = self.NodeAdd(value1,value2,weight1,weight2)
            result2 = self.NodeAdd(value1,value3,weight1,weight3)

            self.r4.append(result1)
            self.r4.append(result2)

    def Layer_Four(self):
        FINAL_RESULT=0
        nr=0
        for x in self.r4:
            FINAL_RESULT+=x*self.DNA4[nr]
            nr+=1


        if self.style=='Stout': self.Stout.append(FINAL_RESULT)
        ##if self.style=='Stout': print(self.style)
        if self.style== 'Ale': self.Ale.append(FINAL_RESULT)
        if self.style=='IPA': self.IPA.append(FINAL_RESULT)
        if self.style=='Lager': self.Lager.append(FINAL_RESULT)
        if self.style=='Porter': self.Porter.append(FINAL_RESULT)
        if self.style=='Saison': self.Saison.append(FINAL_RESULT)
        if self.style=='Witbier': self.Witbier.append(FINAL_RESULT)

    def Layer_Four_TEST(self):
        FINAL_RESULT=0
        for x in range(0,len(self.r4)):
            FINAL_RESULT+=self.r4[x]*self.DNA4[x]
        return FINAL_RESULT


    def Summarize(self):
        self.r1x=len(self.r1)
        self.r2x=len(self.r2)
        self.r3x=len(self.r3)
        self.r4x=len(self.r4)
        s=0
        for x in self.Stout:
            s+=x
        try: self.StoutV=s/len(self.Stout)
        except: self.StoutV=0

        s=0
        for x in self.Ale:
            s+=x
        try: self.AleV=s/len(self.Ale)
        except: self.AleV=0
        s=0
        for x in self.IPA:
            s+=x
        try: self.IPAV=s/len(self.IPA)
        except: self.IPAV=0
        s=0
        for x in self.Lager:
            s+=x
        try: self.LagerV=s/len(self.Lager)
        except: self.LagerV=0
        s=0
        for x in self.Porter:
            s+=x
        try: self.PorterV=s/len(self.Porter)
        except: self.PorterV=0
        s=0
        for x in self.Saison:
            s+=x
        try: self.SaisonV=s/len(self.Saison)
        except: self.SaisonV = 0

        s=0
        for x in self.Witbier:
            s+=x
        try: self.WitbierV=s/len(self.Witbier)
        except: self.WitbierV = 0
        self.Values = [self.AleV,self.StoutV,self.IPAV,self.LagerV,self.PorterV,self.SaisonV,self.WitbierV]

    def Test(self, data):
        results=[]
        for x in range(0,len(data)):
            self.Clear_cache()
            self.Receive_data(Style[data[x]],ABV[data[x]],IBU[data[x]],Color[data[x]],BoilTime[data[x]],BoilGravity[data[x]],Efficiency[data[x]])
            self.Layer_One()
            self.Layer_Two()
            self.Layer_Three()
            number = self.Layer_Four_TEST()
            najm=abs(number-self.AleV)
            quess='Ale'
            nr=0
            for x in self.Values:
                if abs(number-x)<najm:
                        najm=abs(number-x)
                        if nr==0: quess='Ale'
                        elif nr==1: quess='Stout'
                        elif nr==2:quess='IPA'
                        elif nr==3:quess='Lager'
                        elif nr==4:quess='Porter'
                        elif nr==5: quess='Saison'
                        else: quess='Witbier'
                nr+=1
            if QNA: print("Guessed ",quess," was ",self.style, end='')
            if quess==str(self.style):
                if QNA: print("-> Correct!")
                results.append(int(1))
            else:
                results.append(int(0))
                if QNA: print("-> Incorrect!")
        score=0
        for x in results:
            score+=x

        self.Perfection = score/len(results)

    def Get_Acc(self):
        return self.Perfection

    def Modify_DNA(self, power, special=False):

        len1=len(self.DNA1)-1
        len1x=len(self.DNA1[0])-1
        len2=len(self.DNA2)-1
        len2x=len(self.DNA2[0])-1
        len3=len(self.DNA3)-1
        len3x=len(self.DNA3[0])-1
        len4=len(self.DNA4)-1


        for x in range(0,mods):
            dnaM=r.randint(1,4)
            if special: power=100
            mutation=1+r.randint(-power,+power)*0.01
            if dnaM==1:
                mutated1 = r.randint(0,len1)
                mutated2 = r.randint(3,len1x)
                #print(self.DNA1[mutated1][mutated2])
                self.DNA1[mutated1][mutated2]=self.DNA1[mutated1][mutated2]*mutation
            elif dnaM==2:
                mutated1 = r.randint(0,len2)
                mutated2 = r.randint(3,len2x)
                #print(self.DNA2[mutated1][mutated2])
                self.DNA2[mutated1][mutated2]=self.DNA2[mutated1][mutated2]*mutation
            elif dnaM==3:
                mutated1 = r.randint(0,len3)
                mutated2 = r.randint(3,len3x)
                #print(self.DNA3[mutated1][mutated2])
                self.DNA3[mutated1][mutated2]=self.DNA3[mutated1][mutated2]*mutation
            else:
                ##DNA4 is special
                mutated1 = r.randint(0,len4)
                #print(self.DNA4[mutated1])
                self.DNA4[mutated1]=mutation*self.DNA4[mutated1]
        if SuperMutation:
            for x in range(0,SuperMutationAmount):
                dnaM=r.randint(1,3+7)
                if dnaM==1:
                    mutated1 = r.randint(0,len1)
                    mutated2 = r.randint(1,2)
                    mutagen = self.DNA1[mutated1][0]
                    wut=r.randint(1,self.r1x-1)
                    while self.DNA1[mutated1][0]==wut:
                        wut=r.randint(1,self.r1x-1)
                    self.DNA1[mutated1][mutated2]=wut
                elif dnaM==2:
                    mutated1 = r.randint(0,len2)
                    mutated2 = r.randint(1,2)
                    mutagen = self.DNA2[mutated1][0]
                    wut=r.randint(1,self.r2x-1)
                    while self.DNA2[mutated1][0]==wut:
                        wut=r.randint(1,self.r1x-1)
                    self.DNA2[mutated1][mutated2]=wut
                elif dnaM==3:
                    mutated1 = r.randint(0,len3)
                    mutated2 = r.randint(1,2)
                    mutagen = self.DNA3[mutated1][0]
                    wut=r.randint(1,self.r3x-1)
                    while self.DNA3[mutated1][0]==wut:
                        wut=r.randint(1,self.r1x-1)
                    self.DNA3[mutated1][mutated2]=wut
                else: None
def Generate_Dataset():
    dataArr=[]
    for x in range(0,data_amount):
        new = r.randint(1,beers_amount)
        while (new in dataArr):
            new = r.randint(1,beers_amount)
        dataArr.append(new)
    if len(dataArr)==data_amount:
        None
    else: print("You focked up! Gen_dataset, len created:",len(dataArr),", len wanted:",data_amount)
    return dataArr

def Generate_Test(falses):
    data=[]
    for x in range(0,testing_beers_count):
        new = r.randint(1,beers_amount)
        while(new in data or new in falses):
            new = r.randint(1,beers_amount)
        data.append(new)
    if len(data)==testing_beers_count:
        None
    else: print("You focked up! Gen_test")
    return data

print("Creating robots...")
Generation=1
New=True
Robots=[]
for x in range(1,How_many_robots+1):
    robot = Robot()
    robot.set_ID(x)
    Robots.append(robot)
print("Done creating ",len(Robots)," robots!")

Champions=[0,0,0,0,0,0,0,0,0,0]
ChampionsScore=[0,0,0,0,0,0,0,0,0,0]
OldChampions=[]
OldChampScore=0
timetravel=False
while True:
    print("GENERATION: ",Generation)
    for robot in Robots:
        data = Generate_Dataset()
        test = Generate_Test(data)
        if New:
            x=0
            robot.Receive_data(Style[data[x]],ABV[data[x]],IBU[data[x]],Color[data[x]],BoilTime[data[x]],BoilGravity[data[x]],Efficiency[data[x]])
            robot.Create_DNA_1()
            robot.Layer_One()
            robot.Create_DNA_2()
            robot.Layer_Two()
            robot.Create_DNA_3()
            robot.Layer_Three()
            robot.Create_DNA_4()
            robot.Clear_cache()
        else:
            lucky = r.randint(1,chance)
            if lucky==1:
                robot.Modify_DNA(powerX,True)
                print("LB! ", end='')
            else: robot.Modify_DNA(powerX)
            robot.Recreate_beer_tabs()
        for x in range(0,len(data)-1):
            robot.Clear_cache()
            robot.Receive_data(Style[data[x]],ABV[data[x]],IBU[data[x]],Color[data[x]],BoilTime[data[x]],BoilGravity[data[x]],Efficiency[data[x]])
            robot.Layer_One()
            robot.Layer_Two()
            robot.Layer_Three()
            robot.Layer_Four()
        robot.Summarize()
        robot.Test(test)
        score= robot.Get_Acc()

        print("Robot nr ",robot.get_ID()," has an accuracy: ",score,"-> ", end='')
        #print(ChampionsScore)

        if score>ChampionsScore[0]:
            Champions.insert(0,robot)
            ChampionsScore.insert(0,score)
            print("Put 1st")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[1]:
            Champions.insert(1,robot)
            ChampionsScore.insert(1,score)
            print("Put 2nd")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[2]:
            Champions.insert(2,robot)
            ChampionsScore.insert(2,score)
            print("Put 3rd")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[3]:
            Champions.insert(3,robot)
            ChampionsScore.insert(3,score)
            print("Put 4th")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[4]:
            Champions.insert(4,robot)
            ChampionsScore.insert(4,score)
            print("Put 5th")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[5]:
            Champions.insert(5,robot)
            ChampionsScore.insert(5,score)
            print("Put 6th")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[6]:
            Champions.insert(6,robot)
            ChampionsScore.insert(6,score)
            print("Put 7th")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[7]:
            Champions.insert(7,robot)
            ChampionsScore.insert(7,score)
            print("Put 8th")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[8]:
            Champions.insert(8,robot)
            ChampionsScore.insert(8,score)
            print("Put 9th")
            Champions.pop()
            ChampionsScore.pop()
        elif score>ChampionsScore[9]:
            Champions[9]=robot
            ChampionsScore[9]=score
            print("Put 10th")
        else: print("Useless..")




    robot = Champions[0]

    if printstuff:
        print("Len of DNA:")
        print(len(robot.DNA1)+len(robot.DNA2)+len(robot.DNA3)+len(robot.DNA4))
        print("Len 1:",len(robot.DNA1)," len 2:",len(robot.DNA2)," len3:",len(robot.DNA3)," len 4:",len(robot.DNA4))
        print("Values per beer:")
        print(robot.Values)
        print("Champion box:")
        print(ChampionsScore)
        print("Old Champion master:")
        print(OldChampScore)
        print("Decision:",end='')
        if ChampionsScore[0]>OldChampScore:
            print(" Passing")
        else:
            print(" Terminated")
        continuePR=input("Click enter to continue")

        if passafter: printstuff=False



    ChampionFound=False

    if not New:
        if OldChampScore>ChampionsScore[0]:
                print("That gen SUCKED, going back in time")
                Champions=OldChampions
                ChampionsScore[0]=OldChampScore
                Robots=[]
                while len(Robots)<=duplicates*10:
                    for x in range(0,duplicates):
                        Robots.append(Champions[0])
                        Robots.append(Champions[0])
                        Robots.append(Champions[0])
                        Robots.append(Champions[0])
                        Robots.append(Champions[0])

                        Robots.append(Champions[1])
                        Robots.append(Champions[2])
                        Robots.append(Champions[3])
                        Robots.append(Champions[4])
        else:
            ChampionFound = True
            while len(Robots)<=duplicates*10:
                    for x in range(0,duplicates):
                        Robots.append(Champions[0])
                        Robots.append(Champions[0])
                        Robots.append(Champions[0])
                        Robots.append(Champions[0])
                        Robots.append(Champions[0])

                        Robots.append(Champions[1])
                        Robots.append(Champions[2])
                        Robots.append(Champions[3])
                        Robots.append(Champions[4])
    else:
        Robots=[]
        while len(Robots)<=duplicates*10:
            for x in range(0,duplicates):
                if Champions[0]!=0:Robots.append(Champions[0])
                if Champions[0]!=0:Robots.append(Champions[0])
                if Champions[0]!=0:Robots.append(Champions[0])

                if Champions[1]!=0:Robots.append(Champions[1])
                if Champions[2]!=0:Robots.append(Champions[2])
                if Champions[3]!=0:Robots.append(Champions[3])

    OldChampions=Champions
    OldChampScore=ChampionsScore[0]
    if ChampionFound:
        f = open("DNA Champion {} .txt".format(str(Generation)), "w+")
        f.write(str(robot.DNA1))
        f.write("\n")
        f.write(str(robot.DNA2))
        f.write("\n")
        f.write(str(robot.DNA3))
        f.write("\n")
        f.write(str(robot.DNA4))
        f.write("\n")
        f.write("\n")
        f.write("Accuracy: ")
        f.write(str(ChampionsScore[0]))
        f.close()
        ChampionFound=False
    print("Finished this gen, champion score: ",ChampionsScore[0],"best score: ",OldChampScore)
    Generation+=1
    New=False
    Champions=[0,0,0,0,0,0,0,0,0,0]
    ChampionsScore=[0,0,0,0,0,0,0,0,0,0]
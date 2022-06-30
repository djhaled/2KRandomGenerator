
from pymeow import *
import time
import requests
import json
import random
start_time = time.time()
alloff = []
process = process_by_name("NBA2K21.exe")
def HasKey(key,array):
	if key in array:
		return True
	else:
		return False
def read_bit(proc,addr, start,length):
    BytoRead = read_byte(proc,addr)
    return BytoRead >> start & ((1 << length) -1)
def GetNumByte(number,byte):
	return number*byte

class Attributes:
	Year1 = (0x1A4) ##### WORKING
	Year2 = (0x1A8) ##### WORKING
	Year3 = (0x1AC) ##### WORKING
	Year4 = (0x1B0) ##### WORKING
	Year5 = (0x1B4) ##### WORKING
	Year6 = (0x1B8) ##### WORKING
	YearsLeft = (0x32E) ##### WORKING 4bit
	BirthYear = (0x6E) ##### WORKING
	NoTrade = (0x18C) ##### working 64 bit
	ContractOption = (0x317)##### working 16bit
	PeakStart = (0x72) #####  working 16 bit --- bugged gemeos 1
	PeakEnd = (0x73) ##### working 4 bit     --- bugged gemeos 1
	PlayForWinner = (0x229) ##### 16 bit     --- bugged gemeos 2
	FinancialSecurity = (0x22A) ##### 8 bit  --- bugged gemeos 2
	Loyalty = (0x228) ##### 32 bit           --- bugged gemeos 2
############## json ##############
f = open("C:/Users/BERNA/Documents/2KRandomGN/player2K.json")
req = json.load(f)
def GetOverall():
	attr = req["ATTRIBUTES"]
	base_address = process["modules"]["NBA2K21.exe"]["baseaddr"] + 0x058AD9E0
	Addy = read_int64(process,base_address)
	for index, j in enumerate(attr):
		if HasKey("offset",j):
			offset = j['offset']
			nameoffset = j['name']
			offset = int(offset, base=16)
			newone = Addy + offset
			new = read_byte(process,newone)
			#print(f'Stat:{nameoffset} has value of: {new}')
			alloff.append(new)
	Overall = sum(alloff) / len(attr)
	RandomizeStats(Overall)
	alloff.clear()



## 190 max overall 
## 51 min overall
############### AGE ###################
############### AGE ###################
def RandomizeAge(proc,Addy):
	age = (random.randint(1991, 2000))
	NewBirthYear = Addy + Attributes.BirthYear
	write_int(proc,NewBirthYear,age)
	return 2020 - age
	############### PEAK ###################
	############### PEAK ###################
def RandomizePeak(proc,Addy):
	peakstart = (random.randint(19, 25))
	peakend = (random.randint(29, 36))
	NewPeakStart = Addy + Attributes.PeakStart
	NewPeakEnd = Addy + Attributes.PeakEnd
	write_int(proc,NewPeakStart,peakstart)
	write_int(proc,NewPeakEnd,peakend)
	############### Tends ###################
	############### Tends ###################
def RandomizeTends(proc,Addy):
	playforwinner = (random.randint(15, 100))
	loyalty = (random.randint(15, 100))
	financial = (random.randint(25, 100))
	NewPlayForWinner = Addy +Attributes.PlayForWinner
	NewPlayForLoyalty = Addy + Attributes.Loyalty
	NewPlayForFinancial = Addy + Attributes.FinancialSecurity
	write_int(proc,NewPlayForWinner,playforwinner)
	write_int(proc,NewPlayForLoyalty,loyalty)
	write_int(proc,NewPlayForFinancial,financial)
	############### CONTRACT ###################
	############### CONTRACT ###################
def RandomizeContract(proc,OVR,Addy,Age):
	yearsleft = (random.randint(1, 5))
	NewYearsLeft = Addy + Attributes.YearsLeft
	write_int(proc,NewYearsLeft,GetNumByte(yearsleft,4))
	ContractToGive = transRange(OVR,90,150,2000000,34000000)
	AgeTransRange = transRange(Age,20,29,1,0.95)
	ContractToGive = ContractToGive * AgeTransRange
	for i in range(yearsleft):
		NWYR = i + 1
		AttrRef = eval(f'Attributes.Year{NWYR}')
		NewContract = Addy + AttrRef
		write_int(proc,NewContract,int(ContractToGive))
		ContractToGive = ContractToGive * 1.05
	ContractToGive = 0
	############### OPTIONS ###################
	############### OPTIONS ###################
def RandomizeOptions(proc,Addy):
	ContractOptionRandom = (random.randint(0, 2))
	OptionContract = Addy + Attributes.ContractOption
	write_int(proc,OptionContract,GetNumByte(ContractOptionRandom,16))
	############### NO - TRADE ###################
	############### NO - TRADE ###################
def RandomizeNoTrade(proc,Addy):
	NoTradeRandom = (random.randint(0, 1))
	NoTradeOption = Addy + Attributes.NoTrade
	write_int(proc,NoTradeOption,GetNumByte(NoTradeRandom,64))
	############### MAIN() ###################
	############### MAIN() ###################
def RandomizeStats(overall):
	#process = process_by_name("NBA2K21.exe")
	base_address = process["modules"]["NBA2K21.exe"]["baseaddr"] + 0x058AD9E0
	Addy = read_int64(process,base_address)
	Age = RandomizeAge(process,Addy)
	RandomizePeak(process,Addy)
	RandomizeTends(process,Addy)
	RandomizeContract(process,overall,Addy,Age)
	RandomizeOptions(process,Addy)
	RandomizeNoTrade(process,Addy)




def transRange(value,leftMin,LeftMax,RightMin,RightMax):
	leftSpan = LeftMax - leftMin
	RightSpan = RightMax - RightMin

	valuescaled = float(value-leftMin) / float(leftSpan)
	return RightMin + (valuescaled * RightSpan)




start_time = time.time()
time.sleep(2)
while True:
	GetOverall()
	opa = random.randint(2,200)
	print(f"Player Done {opa}")
	time.sleep(0.04)

	








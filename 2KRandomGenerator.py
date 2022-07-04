
from pymeow import *
import time
import requests
import json
import random
start_time = time.time()
alloff = []
process = process_by_name("NBA2K21.exe")
DictPotential = []
DictTends = []
CurrentPlayer = 0
currentMultiplier = 0
BadgesDict = {0: 'NOBADGE',1: 'Bronze', 2: 'Silver', 3: 'Gold',4: 'HallOfFame'}
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
def clamp(minimum, x, maximum):
	return max(minimum, min(x, maximum))

class Attributes:
	Year1 = (0x1A4) ##### WORKING
	Year2 = (0x1A8) ##### WORKING
	Year3 = (0x1AC) ##### WORKING
	Year4 = (0x1B0) ##### WORKING
	Year5 = (0x1B4) ##### WORKING
	Year6 = (0x1B8) ##### WORKING
	Position = (0xF9)
	ShotTendence = (0x454)
	FirstName = (0x28)
	LastName = (0x0)
	Potential = (0x43D)
	YearsLeft = (0x32E) ##### WORKING 4bit
	BirthYear = (0x6E) ##### WORKING
	NoTrade = (0x18C) ##### working 64 bit
	ContractOption = (0x317)##### working 16bit
	PeakStart = (0x72) #####  working 16 bit --- bugged gemeos 1
	PeakEnd = (0x73) ##### working 4 bit     --- bugged gemeos 1
	PlayForWinner = (0x229) ##### 16 bit     --- bugged gemeos 2
	FinancialSecurity = (0x22A) ##### 8 bit  --- bugged gemeos 2
	Loyalty = (0x228) ##### 32 bit           --- bugged gemeos 2
	UniqueID = (0xF4)
############## json ##############
f = open("C:/Users/BERNA/Documents/2KRandomGN/player2K.json")
req = json.load(f)
def Get_Position(bit):
	if bit == 0:
		return 'PG'
	if bit == 1:
		return 'SG'
	if bit == 2:
		return 'SF'
	if bit == 3:
		return 'PF'
	if bit == 4:
		return 'C'
def GetPotential(proc,addr):
	if CurrentPlayer in DictPotential:
		return
	else:
		Potential = read_byte(proc,addr)
		NewPotential = random.randrange(Potential-15,Potential+15)
		write_byte(process,addr,NewPotential)
		DictPotential.append(CurrentPlayer)
def GetPlayer(proc,addr):
	UniqueID = read_bytes(proc,addr,2)
	address_int = int.from_bytes(UniqueID, "little")
	global CurrentPlayer
	CurrentPlayer = address_int
def GetOverall():
	attr = req["ATTRIBUTES"]
	Badges = req["BADGES"]
	Tendencies = req["TENDENCIES"]
	base_address = process["modules"]["NBA2K21.exe"]["baseaddr"] + 0x058AD9E0
	Addy = read_int64(process,base_address)
	####GetPosition#####
	GetPlayer(process,Addy+Attributes.UniqueID)
	GetPotential(process,Addy+Attributes.Potential)
	NewAddy = Addy + Attributes.Position
	PositionBit = read_bit(process,NewAddy,0,3)
	Position = Get_Position(PositionBit)
	#####GetName######
	#AddyFirstName = Addy + Attributes.FirstName
	#AddyLastName = Addy + Attributes.LastName

	#FirstName = read_string(process,AddyFirstName,40)
	#LastName = read_string(process,AddyLastName,40)
	for j in attr:
		if HasKey("multiplier",j):
			multi = j["multiplier"]
			Multiplier = multi[f"{Position}"]
		if HasKey("offset",j):
			offset = j['offset']
			nameoffset = j['name']
			offset = int(offset, base=16)
			newone = Addy + offset
			new = read_byte(process,newone)
			new = new * Multiplier
			alloff.append(new)
	for k in Badges:
		if HasKey("offset",k):
			offset = k['offset']
			nameoffset = k['name']
			offset = int(offset, base=16)
			newone = Addy + offset
			StartBit = k["info"]
			new = read_bit(process,newone,StartBit["startbit"],k["size"])
			Value = BadgesMultiplier(new)
			alloff.append(Value)
			#print(f'Stat:{nameoffset} has value of: {BadgesDict[new]}')

	Overall = sum(alloff) / len(attr)
	RandomizeStats(Overall)
	alloff.clear()
	###########################
	if CurrentPlayer in DictTends:
		return
	for f in Tendencies:
		if HasKey("offset",f):
			offset = f['offset']
			nameoffset = f['name']
			offset = int(offset, base=16)
			newone = Addy + offset
			stat = read_byte(process,newone)
			NewPotential = random.randrange(stat-10,stat+15)
			DictTends.append(CurrentPlayer)
			#print(f'Stat:{nameoffset} has value of: {NewPotential}')
			stat = write_byte(process,newone,NewPotential)


########## BEKA you need to give less power to defense stats and more to 3 pointers and more to offense at all... ###### do dat.
def BadgesMultiplier(value):
	if value == 0:
		return 0 
	if value == 1:
		return 25 
	if value == 2:
		return 50 
	if value == 3:
		return 100 
	if value == 4:
		return 150 
## 190 max overall 
## 51 min overall
############### AGE ###################
############### AGE ###################
def RandomizeAge(proc,Addy):
	age = (random.randint(1993, 2000))
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
	ContractToGive = transRange(OVR,105,200,1017781,40000000)
	if OVR <= 95:
		ContractToGive = 1017781
	if OVR >= 200:
		ContractToGive = 40000000
	AgeTransRange = transRange(Age,20,29,1,0.75)
	ContractToGive = ContractToGive * AgeTransRange
	#print(f'Age:{Age} Contract:{ContractToGive}')
	for i in range(yearsleft):
		NWYR = i + 1
		AttrRef = eval(f'Attributes.Year{NWYR}')
		NewContract = Addy + AttrRef
		write_int(proc,NewContract,int(ContractToGive))
		ContractToGive = ContractToGive * 1.15
	ContractToGive = 0
	############### OPTIONS ###################
	############### OPTIONS ###################
def RandomizeOptions(proc,Addy):
	Random = random.randint(0,7)
	ContractOption = 0
	if Random <= 1:
		ContractOption = 2
	if Random == 5:
		ContractOption = 1
	OptionContract = Addy + Attributes.ContractOption
	write_int(proc,OptionContract,GetNumByte(ContractOption,16))
	############### NO - TRADE ###################
	############### NO - TRADE ###################
def RandomizeNoTrade(proc,Addy):
	Random = random.randint(0,7)
	NoTradeRandom = 0
	if Random == 3:
		NoTradeRandom = 1
	NoTradeOption = Addy + Attributes.NoTrade
	write_int(proc,NoTradeOption,GetNumByte(NoTradeRandom,64))
	############### MAIN() ###################
	############### MAIN() ###################
def RandomizeStats(overall):
	#process = process_by_name("NBA2K21.exe")
	base_address = process["modules"]["NBA2K21.exe"]["baseaddr"] + 0x058AD9E0
	Addy = read_int64(process,base_address)
	Age = RandomizeAge(process,Addy)
	#RandomizePeak(process,Addy)
	#RandomizeTends(process,Addy)
	RandomizeContract(process,overall,Addy,Age)
	RandomizeOptions(process,Addy)
	RandomizeNoTrade(process,Addy)




def transRange(value,leftMin,LeftMax,RightMin,RightMax):
	leftSpan = LeftMax - leftMin
	RightSpan = RightMax - RightMin

	valuescaled = float(value-leftMin) / float(leftSpan)
	return RightMin + (valuescaled * RightSpan)




while True:
	GetOverall()
	time.sleep(0.04)
	








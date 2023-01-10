
from pymeow import * 
import json
import random
import time
process = process_by_name("NBA2K23.exe")


def read_bit(proc,addr, start,length):
	BytoRead = read_byte(proc,addr)
	return BytoRead >> start & ((1 << length) -1)


def GetNumByte(number,byte):
	return number*byte


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
	Potential = read_byte(proc,addr)
	NewPotential = random.randrange(Potential-15,Potential+15)
	write_byte(process,addr,NewPotential)

def GetPlayer(proc,addr):
	UniqueID = read_bytes(proc,addr,2)
	address_int = int.from_bytes(UniqueID, "little")
	global CurrentPlayer
	CurrentPlayer = address_int
	first_name = read_string(proc, addr + Attributes.FirstName, 256)
	last_name = read_string(proc, addr + Attributes.LastName, 256)

def GetOverall():
	## +3CE1190 BASE ADDY
	base_address = process["modules"]["NBA2K23.exe"]["baseaddr"] + 0x3CE1190
	Addy = read_int64(process,base_address)
	####GetPosition#####
	GetPlayer(process,Addy+Attributes.UniqueID)
	GetPotential(process,Addy+Attributes.Potential)
	NewAddy = Addy + Attributes.Position
	PositionBit = read_bit(process,NewAddy,0,3)
	Position = Get_Position(PositionBit)
	CacheOvrAddy = Addy + Attributes.CacheOVR
	Overall = read_float(process,CacheOvrAddy)
	RandomizeStats(Overall)
	###########################

def RandomizeAge(proc,Addy):
	age = (random.randint(1993, 2000))
	NewBirthYear = Addy + Attributes.BirthYear
	write_int(proc,NewBirthYear,age)
	return 2020 - age

def RandomizePeak(proc,Addy):
	peakstart = (random.randint(19, 25))
	peakend = (random.randint(29, 36))
	NewPeakStart = Addy + Attributes.PeakStart
	NewPeakEnd = Addy + Attributes.PeakEnd
	write_int(proc,NewPeakStart,peakstart)
	write_int(proc,NewPeakEnd,peakend)

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

def RandomizeContract(proc,OVR,Addy,Age):
	yearsleft = (random.randint(1, 5))
	NewYearsLeft = Addy + Attributes.YearsLeft
	write_int(proc,NewYearsLeft,GetNumByte(yearsleft,4))
	ContractToGive = transRange(OVR,75,92,1017781,40000000)
	if OVR <= 74:
		ContractToGive = 1017781
	if OVR >= 92:
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

def RandomizeOptions(proc,Addy):
	Random = random.randint(0,7)
	ContractOption = 0
	if Random <= 1:
		ContractOption = 2
	if Random == 5:
		ContractOption = 1
	OptionContract = Addy + Attributes.ContractOption
	write_int(proc,OptionContract,GetNumByte(ContractOption,16))


def RandomizeNoTrade(proc,Addy):
	Random = random.randint(0,7)
	NoTradeRandom = 0
	if Random == 3:
		NoTradeRandom = 1
	NoTradeOption = Addy + Attributes.NoTrade
	write_int(proc,NoTradeOption,GetNumByte(NoTradeRandom,64))


def RandomizeStats(overall):
	#process = process_by_name("NBA2K21.exe")
	base_address = process["modules"]["NBA2K23.exe"]["baseaddr"] + 0x3CE1190
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


class Attributes:
	Year1 = (0x180) ##### WORKING
	Year2 = (0x184) ##### WORKING
	Year3 = (0x188) ##### WORKING
	Year4 = (0x18C) ##### WORKING
	Year5 = (0x190) ##### WORKING
	Year6 = (0x194) ##### WORKING
	Position = (0xD1)
	ShotTendence = (0x45C)
	FirstName = (0x28)
	LastName = (0x0)
	CacheOVR = (0x148)
	Potential = (0x445)  
	YearsLeft = (0x32A) ##### WORKING 4bit
	BirthYear = (0x6E) ##### WORKING
	NoTrade = (0x342) ##### working 64 bit
	ContractOption = (0x313)##### working 16bit
	PeakStart = (0x72) #####  working 16 bit --- bugged gemeos 1
	PeakEnd = (0x73) ##### working 4 bit     --- bugged gemeos 1
	PlayForWinner = (0x209) ##### 16 bit     --- bugged gemeos 2
	FinancialSecurity = (0x20A) ##### 8 bit  --- bugged gemeos 2
	Loyalty = (0x208) ##### 32 bit           --- bugged gemeos 2
	UniqueID = (0xCC)
############## json ##############

while True:
	GetOverall()
	time.sleep(0.04)
	








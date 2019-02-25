import json 
import xlrd


def addDataToFile(fileName,new):
	if new==False:
		file=open(fileName,"r+")
		data=json.load(file)
		newdata=sheetDataExtractor(fileName)
		data[newdata[1]]=newdata[0]
		json.dump(data,file,ensure_ascii=False,indent=4)
		file.close()
		
	else:
		file=open("database.txt","w",encoding = "utf-8")
		data=sheetDataExtractor(fileName)
		dataclass={}
		dataclass[data[1]]=data[0]
		json.dump(dataclass,file,ensure_ascii=False,indent=4)
		file.close()


def sheetDataExtractor(sheetName):
	book = xlrd.open_workbook(sheetName)
	sheet = book.sheet_by_index(0)
	namelist = sheet.col_values(2,9)

	data2 = []
	term1=[]
	term2=[]
	term3=[]
	Terms=[term1,term2,term3]
	num=9
	count=0
	for learner in range(0, len(namelist)):
		if namelist[learner] != '':
			data2.append(sheet.row_values(num,2))
			num=num+1
	tasksindex=[]
	t=sheet.row_values(5,3)
	for i in range(0,len(t)):
		if t[i]!="":
			tasksindex.append(i)
			Terms[count].append(i)
		if t[i-1]!="" and t[i]=="":
				count=count+1


	data={}
	data["subject"]=(sheet.row_values(3,0,1)[0]).split(":")[0]
	data["Teacher"]=sheet.row_values(0,17,18)
	data["Grade"]=sheet.row_values(1,16,18)
	data["taskNames"]=sheet.row_values(7,3)
	data["tasksindex"]=tasksindex
	data["DefaultMarks"]=sheet.row_values(8,3)
	data["Terms"]=Terms
	data["SchoolName"]=sheet.row_values(0,0,3)
	data["database"]=data2
	className="".join(sheet.row_values(1,16,18))
	ls=[data,className]
	return ls

def ReadFile(filename):
	loadData=json.load(filename)
	return loadData


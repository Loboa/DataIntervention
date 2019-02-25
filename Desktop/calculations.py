import numpy as np 

class Calc(object):
	def __init__(self,data):
		self.data=data
		self.terms=data["Terms"]
		self.tasknames=data["taskNames"]
		self.database=data["database"]
		self.teacherNam=data["Teacher"]
		self.grade=data["Grade"]
		self.names=[]
		for i in self.database:
			self.names.append(i[0])

		self.defaultmarks=data["DefaultMarks"]

	def taskMark(self,index):
	
		tasklist=[]
		defaultmrk=self.defaultmarks[index]
		taskname=self.tasknames[index]
		for j in self.database:
			if j[index+1]=='':
				tasklist.append(0.00)
			else:
				tasklist.append(j[index+1])
			
		x=np.array(tasklist)
		return [defaultmrk,np.average(x),np.sum(x),np.min(x),np.max(x),taskname,tasklist]
	

	def termCount(self,term):
		taskArray=[]
		defaultSum=[]
		lowTaskmrk=[]
		hightTaskmrk=[]
		meanTask=[]
		tasknames=[]
		Tlist=self.terms[term]
		for tsk in  Tlist:
			taskArray.append(self.taskMark(tsk))

		for item in taskArray:
			defaultSum.append(item[0])
			lowTaskmrk.append(item[3])
			meanTask.append(item[1])
			hightTaskmrk.append(item[4])
			tasknames.append(item[5])

		return [taskArray,defaultSum,lowTaskmrk,hightTaskmrk,meanTask,tasknames]

	def toPercent(self,mark,totmark):
		percList=[]
		for i in range(0,len(totmark)):
			perc=(mark[i]/float(totmark[i]))
			perc=perc*100
			percList.append(perc)

		return percList

	def locateName(self,number,tasklist):
		x=tasklist.index(number)
		for i in range(0,len(self.database)):
			if number==self.database[i][x+1]:
				name=self.database[i][0]
				return name

			
		return "No name"


	def LearnerNamesPerc(self,name,term,n):
		tasklist=[]
		totmark=[]
		taskname=[]
		for i in range(0,len(self.database)):
			if name==self.database[i][0]:
				for j in self.terms[term]:
					if self.database[i][j+1]=="":
						tasklist.append(0)
					else:
						tasklist.append(self.database[i][j+1])
					totmark.append(self.defaultmarks[j])
		for k in self.terms[term]:
			taskname.append(self.tasknames[k])
		if n==True:
			perclst=self.toPercent(tasklist,totmark)
			return perclst
		else :
			return [tasklist,totmark,taskname]
		
	def learnerNames(self):
		return self.names

	def Teacher(self):
		return self.teacherNam

	def classGrade(self):
		return self.grade 
		

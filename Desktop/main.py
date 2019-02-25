import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from new_Ui import *
import fileHandler as dt
import Charts as ch
from calculations import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class mainClass(QMainWindow):
	"""This is the main class of the system application"""
	def __init__(self,parent=None):
		super(mainClass,self).__init__(parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)

		#On the first display these are the seetings for the tabs 
		self.ui.tabWidget.setTabEnabled(1, 0)
		self.ui.tabWidget.setTabEnabled(2, 0)
		self.ui.tabWidget.setTabEnabled(3, 0)
		self.ui.tabWidget.setTabEnabled(4, 0)
		self.ui.tabWidget.setCurrentIndex(0)
		self.ui.radioButton.setChecked(True)
		self.ui.comboBox.setEnabled(False)
		self.ui.radioButton_3.setChecked(True)
		self.ui.radioButton_5.setChecked(True)
		
		self.checkFile()

		#SIGNAL AND SLOTS---------------------------------------------------
		self.ui.listWidget_2.itemClicked.connect(self.displayData)
		self.ui.comboBox_2.currentIndexChanged.connect(self.classPerform)
		self.ui.radioButton.toggled.connect(self.classPerform)
		self.ui.listWidget.itemClicked.connect(self.learnerDisplay)
		self.ui.listWidget_3.itemClicked.connect(self.taskSelected)
		self.ui.comboBox.currentIndexChanged.connect(self.learnerDisplay)
		self.ui.pushButton.pressed.connect(self.UploadButton)
		#-------------------------------------------------------------------

	def closeApp(self):
		"""This method exist the systems"""
		QtCore.QCoreApplication.quit()


	def checkFile(self):
		try:
			m_file=open('database.txt')
			self.readFiles(m_file)

		except IOError:
			"""IF there is no file stored in the database display a text"""
			self.upLoadFile()
			#Send out a warning 

	def upLoadFile(self):
		m_fileString = QFileDialog.getOpenFileName(self, "Open File", "c:\\", "Document files (*.xlsx *.xls)")
		m_fileName = m_fileString[0]
		if m_fileName != "":
			self.storeData(m_fileName,True)

	def readFiles(self,fileName):
		"""This function extracts the data from the file """
		self.fileData=dt.ReadFile(fileName)
		clsslist=[]
		for clss in self.fileData.keys():
			clsslist.append(clss)

		self.classesList(clsslist)

	def storeData(self,filename,new):
		dt.addDataToFile(filename,new)


	def classesList(self,classlist):
		for item in classlist:
			self.ui.listWidget_2.addItem(item)
	
	def displayData(self):
		self.ui.tabWidget.setTabEnabled(1, 1)
		self.ui.tabWidget.setTabEnabled(2, 1)
		self.ui.tabWidget.setTabEnabled(3, 0)
		self.ui.tabWidget.setTabEnabled(4, 1)
		self.ui.tabWidget.setCurrentIndex(0)
		self.activedata=self.fileData.get(self.ui.listWidget_2.currentItem().text())
		self.calc=Calc(self.activedata)
		#x=self.calc.termCount(2)
		self.ui.label.setText(self.activedata["SchoolName"][2])
		self.ui.label_2.setText("class: "+self.activedata["Grade"][0] +self.activedata["Grade"][1] )
		self.ui.label_16.setText("subject: "+self.activedata["subject"])
		self.mainDonuts()


	def mainDonuts(self):
		
		col = ["green", "blue", "orange", "red"]
		s = ["year average", "Term One", "Term Two", "Term Three"]
		avglist=[]
		total=[]
		for i in range(3):
			t=np.array(self.calc.termCount(i)[4])
			e=np.array(self.calc.termCount(i)[1])
			avg=np.sum(t)
			tot=np.sum(e)
			avglist.append(avg)
			total.append(tot)
		pielist=self.calc.toPercent(avglist,total)
		self.pielist=pielist

		
		m_mainDonut=ch.donutchart(0,0,327,468,col,s,pielist,True)

		scene1=QtWidgets.QGraphicsScene()
		scene1.addWidget(m_mainDonut)
		
		self.ui.graphicsView_3.setScene(scene1)

		col = ["blue", "grey"]
		labelitem=QLabel()
		labelitem.setText("%0.1f"%pielist[0] +"%")
		labelitem.setStyleSheet("border-radius: 1px;\n"
"font: 75 18pt \"Source Sans Pro ExtraLight\";\n"
"background-color: rgb(130, 130, 130,10);")
		labelitem.setGeometry(QRect(95, 39, 100, 100))
		m_t1Donut=ch.donutchart(0,0, 180, 250,col,s,[pielist[0],100-pielist[0]],False)
		scene2=QGraphicsScene()
		scene2.addWidget(m_t1Donut)
		scene2.addWidget(labelitem)
		self.ui.graphicsView_6.setScene(scene2)

		col = ["green", "grey"]
		labelitem=QLabel()
		labelitem.setText("%0.1f"%pielist[1] +"%")
		labelitem.setGeometry(QRect(95, 39, 100, 100))
		labelitem.setStyleSheet("border-radius: 1px;\n"
"font: 75 18pt \"Source Sans Pro ExtraLight\";\n"
"background-color: rgb(130, 130, 130,10);")
		m_t1Donut=ch.donutchart(0,0, 180, 250,col,s,[pielist[1],100-pielist[1]],False)
		scene2=QGraphicsScene()
		scene2.addWidget(m_t1Donut)
		scene2.addWidget(labelitem)
		self.ui.graphicsView_7.setScene(scene2)

		col = ["orange", "grey"]
		labelitem=QLabel()
		labelitem.setText("%0.1f"%pielist[2] +"%")
		labelitem.setGeometry(QRect(95, 39, 100, 100))
		labelitem.setStyleSheet("border-radius: 1px;\n"
"font: 75 18pt \"Source Sans Pro ExtraLight\";\n"
"background-color: rgb(130, 130, 130,10);")
		m_t1Donut=ch.donutchart(0,0, 180, 250,col,s,[pielist[2],100-pielist[2]],False)
		scene2=QGraphicsScene()
		scene2.addWidget(m_t1Donut)
		scene2.addWidget(labelitem)
		self.ui.graphicsView_9.setScene(scene2)
		s=["Term One", "Term Two", "Term Three"]
		scart=ch.scatterPlot(s,pielist)
		scene=QGraphicsScene()
		scene.addWidget(scart)
		self.ui.graphicsView_10.setScene(scene)
		self.LeanerChartDisplay()
		self.classPerform()
		self.taskTab()


	def classPerform(self):

		if self.ui.comboBox_2.itemText(self.ui.comboBox_2.currentIndex()) == "Term One":
			tasknams=self.calc.termCount(0)[-1]
			classmarklist=self.calc.termCount(0)[-2]
			self.classdefaultlist=self.calc.termCount(0)[1]
			self.ui.label_30.setVisible(True)
			self.ui.label_31.setVisible(True)
			self.ui.label_32.setVisible(True)
			self.ui.label_24.setText(tasknams[0])
			self.ui.label_25.setText(tasknams[1])
			self.ui.label_26.setText(tasknams[2])
			self.ui.label_30.setText(tasknams[3])
			self.ui.label_31.setText(tasknams[4])
			self.ui.label_32.setVisible(False)
			self.ui.lineEdit_21.setVisible(True)
			self.ui.lineEdit_22.setVisible(True)
			self.ui.lineEdit_23.setVisible(False)
			self.ui.lineEdit_18.setText("%0.2f" % (classmarklist[0]))
			self.ui.lineEdit_19.setText("%0.2f" % (classmarklist[1]))
			self.ui.lineEdit_20.setText("%0.2f" % (classmarklist[2]))
			self.ui.lineEdit_21.setText("%0.2f" % (classmarklist[3]))
			self.ui.lineEdit_22.setText("%0.2f" % (classmarklist[4]))
			self.classdatalist=[classmarklist[0],classmarklist[1],classmarklist[2],classmarklist[3],classmarklist[4]]
			data=self.calc.toPercent(self.classdatalist,self.classdefaultlist)
			self.portchart(0,data)
		if self.ui.comboBox_2.itemText(self.ui.comboBox_2.currentIndex()) == "Term Two":
			tasknams=self.calc.termCount(1)[-1]
			classmarklist=self.calc.termCount(1)[-2]
			self.classdefaultlist=self.calc.termCount(1)[1]

			self.ui.label_30.setVisible(True)
			self.ui.label_31.setVisible(True)
			self.ui.label_32.setVisible(True)
			self.ui.label_24.setText(tasknams[0])
			self.ui.label_25.setText(tasknams[1])
			self.ui.label_26.setText(tasknams[2])
			self.ui.label_30.setText(tasknams[3])
			self.ui.label_31.setText(tasknams[4])
			self.ui.label_32.setVisible(True)
			self.ui.label_32.setText(tasknams[5])
			self.ui.lineEdit_21.setVisible(True)
			self.ui.lineEdit_22.setVisible(True)
			self.ui.lineEdit_23.setVisible(True)

			self.ui.lineEdit_18.setText("%0.2f" % (classmarklist[0]))
			self.ui.lineEdit_19.setText("%0.2f" % (classmarklist[1]))
			self.ui.lineEdit_20.setText("%0.2f" % (classmarklist[2]))
			self.ui.lineEdit_21.setText("%0.2f" % (classmarklist[3]))
			self.ui.lineEdit_22.setText("%0.2f" % (classmarklist[4]))
			self.ui.lineEdit_23.setText("%0.2f" % (classmarklist[5]))
			self.classdatalist=[classmarklist[0],classmarklist[1],classmarklist[2],classmarklist[3],classmarklist[4],classmarklist[5]]
			data=self.calc.toPercent(self.classdatalist,self.classdefaultlist)
			self.portchart(1,data)


		if self.ui.comboBox_2.itemText(self.ui.comboBox_2.currentIndex()) == "Term Three":
			tasknams=self.calc.termCount(2)[-1]
			classmarklist=self.calc.termCount(2)[-2]
			self.classdefaultlist=self.calc.termCount(2)[1]

			self.ui.label_30.setVisible(True)
			self.ui.label_31.setVisible(True)
			self.ui.label_32.setVisible(False)
			self.ui.lineEdit_21.setVisible(True)
			self.ui.lineEdit_22.setVisible(True)
			self.ui.lineEdit_23.setVisible(False)
			self.ui.label_24.setText(tasknams[0])
			self.ui.label_25.setText(tasknams[1])
			self.ui.label_26.setText(tasknams[2])
			self.ui.label_30.setText(tasknams[3])
			self.ui.label_31.setText(tasknams[4])
			self.ui.lineEdit_18.setText("%0.2f" % (classmarklist[0]))
			self.ui.lineEdit_19.setText("%0.2f" % (classmarklist[1]))
			self.ui.lineEdit_20.setText("%0.2f" % (classmarklist[2]))
			self.ui.lineEdit_21.setText("%0.2f" % (classmarklist[3]))
			self.ui.lineEdit_22.setText("%0.2f" % (classmarklist[4]))
			self.classdatalist=[classmarklist[0],classmarklist[1],classmarklist[2],classmarklist[3],classmarklist[4]]
			data=self.calc.toPercent(self.classdatalist,self.classdefaultlist)
			self.portchart(2,data)

	def portchart(self,index,data):
		"""This function creates the dount charts"""
		s=["Term",""]
		col = ["green", "grey"]
		labelitem=QLabel()
		labelitem.setText("%0.1f"%self.pielist[index] +"%")
		labelitem.setGeometry(QRect(95, 39, 100, 100))
		labelitem.setStyleSheet("border-radius: 1px;\n"
"font: 75 18pt \"Source Sans Pro ExtraLight\";\n"
"background-color: rgb(130, 130, 130,10);")
		m_t1Donut=ch.donutchart(0,0, 180, 250,col,s,[self.pielist[index],100-self.pielist[index]],False)
		scene2=QGraphicsScene()
		scene2.addWidget(m_t1Donut)
		scene2.addWidget(labelitem)
		self.ui.graphicsView_5.setScene(scene2)

		if self.ui.radioButton.isChecked():
			self.classMarkCharts(data)
		if self.ui.radioButton_2.isChecked():
			self.ClassMarkBar(data)

	def classMarkCharts(self,data):
		figure = Figure()
		canvas = FigureCanvas(figure)
		canvas.setGeometry(QtCore.QRect(290, 70, 660, 335))
		
		ax = figure.add_subplot(111)
		ax.clear()
		ax.plot(data, "*-")
		#ax.legend(leg)
		#ax.grid()	
		scen = QtWidgets.QGraphicsScene()
		scen.addWidget(canvas)
		self.ui.graphicsView_4.setScene(scen)

	def ClassMarkBar(self, list1):
		self.chart = QChart()
		if self.ui.comboBox_2.itemText(self.ui.comboBox_2.currentIndex()) == "Term Three":
			classAVG = QBarSet("Class Avarage")
			for i in range(0, len(list1)):
				classAVG << list1[i]
			self.termSeries = QBarSeries()
			self.termSeries.append(classAVG)
			self.chart.addSeries(self.termSeries)

		if self.ui.comboBox_2.itemText(self.ui.comboBox_2.currentIndex()) == "Term One":
			classAVG = QBarSet("Class Avarage")
			for i in range(0, len(list1)):
				classAVG << list1[i]

		

			self.termSeries = QBarSeries()
			self.termSeries.append(classAVG)
			self.chart.addSeries(self.termSeries)

		if self.ui.comboBox_2.itemText(self.ui.comboBox_2.currentIndex()) == "Term Two":
			classAVG = QBarSet("Class Avarage")
			for i in range(0, len(list1)):
				classAVG << list1[i]

			self.termSeries = QBarSeries()
			self.termSeries.append(classAVG)
			self.chart.addSeries(self.termSeries)

		self.chart.setAnimationOptions(QChart.SeriesAnimations)
		theme = self.chart.ChartTheme(0)
		self.chart.setTheme(theme)
		self.axis = QBarCategoryAxis()
		#self.axis.append(termlist)
		self.axis = QBarCategoryAxis()
		self.axis.setTitleText("TESTS")
		self.chart.createDefaultAxes()
		#self.chart.setAxisX(self.axis, self.termSeries)
		self.chart.axisY(self.termSeries).setTitleText("Performance")
		self.chart.legend().setVisible(True)
		self.chartView1 = QChartView(self.chart)
		self.chartView1.setGeometry(QtCore.QRect(10, 10, 660, 335))
		self.chartView1.setRenderHint(QPainter.Antialiasing)
		scen = QtWidgets.QGraphicsScene()
		scen.addWidget(self.chartView1)
		self.ui.graphicsView_4.setScene(scen)


	def LeanerChartDisplay(self):
		names=self.calc.learnerNames()
		self.ui.listWidget.clear()
		for name in names:
			item = QtWidgets.QListWidgetItem(name)
			#item.setIcon(QIcon("person.png"))
			self.ui.listWidget.addItem(item)




	def learnerDisplay(self):
		self.ui.comboBox.setEnabled(True)
		self.ui.label_3.setText("Learner :  " + self.ui.listWidget.currentItem().text())
		if self.ui.comboBox.itemText(self.ui.comboBox.currentIndex()) == "Term One":
			alList=self.calc.LearnerNamesPerc(self.ui.listWidget.currentItem().text(),0,False)
			self.ui.lineEdit.setText(str(alList[0][0]))
			self.ui.lineEdit_2.setText(str(alList[0][1]))
			self.ui.lineEdit_3.setText(str(alList[0][2]))
			self.ui.lineEdit_4.setText(str(alList[0][3]))
			self.ui.lineEdit_5.setText(str(alList[0][4]))
			self.ui.lineEdit_11.setVisible(False)
			self.ui.label_4.setText(alList[2][0])
			self.ui.label_5.setText(alList[2][1])
			self.ui.label_6.setText(alList[2][2])
			self.ui.label_7.setText(alList[2][3])
			self.ui.label_8.setText(alList[2][4])
			self.ui.label_18.setVisible(False)
			self.ui.lineEdit_12.setText(str(alList[1][0]))
			self.ui.lineEdit_13.setText(str(alList[1][1]))
			self.ui.lineEdit_14.setText(str(alList[1][2]))
			self.ui.lineEdit_15.setText(str(alList[1][3]))
			self.ui.lineEdit_16.setText(str(alList[1][4]))
			self.ui.lineEdit_17.setVisible(False)
			
			perc = self.calc.toPercent(self.calc.termCount(0)[-2],self.calc.termCount(0)[1])
			self.TermAvg(alList,perc)

		if self.ui.comboBox.itemText(self.ui.comboBox.currentIndex()) == "Term Two":
			alList = self.calc.LearnerNamesPerc(self.ui.listWidget.currentItem().text(),1,False)
			self.ui.lineEdit.setText(str(alList[0][0]))
			self.ui.lineEdit_2.setText(str(alList[0][1]))
			self.ui.lineEdit_3.setText(str(alList[0][2]))
			self.ui.lineEdit_4.setText(str(alList[0][3]))
			self.ui.lineEdit_5.setText(str(alList[0][4]))
			self.ui.lineEdit_11.setVisible(True)
			self.ui.lineEdit_11.setText(str(alList[0][5]))
			self.ui.label_4.setText(alList[2][0])
			self.ui.label_5.setText(alList[2][1])
			self.ui.label_6.setText(alList[2][2])
			self.ui.label_7.setText(alList[2][3])
			self.ui.label_8.setText(alList[2][4])
			self.ui.label_18.setVisible(True)
			self.ui.label_18.setText(alList[2][5])
			self.ui.lineEdit_12.setText(str(alList[1][0]))
			self.ui.lineEdit_13.setText(str(alList[1][1]))
			self.ui.lineEdit_14.setText(str(alList[1][2]))
			self.ui.lineEdit_15.setText(str(alList[1][3]))
			self.ui.lineEdit_16.setText(str(alList[1][4]))
			self.ui.lineEdit_17.setVisible(True)
			self.ui.lineEdit_17.setText(str(alList[1][5]))
			
			if alList[0][4]< (alList[1][4])*0.3:
				self.ui.label_8.setStyleSheet("background-color: rgb(255, 0,4 ,255);color:rgb(255, 255,255 ,255);")

			else :
				self.ui.label_8.setStyleSheet("background-color:rgb(0, 0,0 ,0;color:rgb(0, 0,0 ,0);")
			perc=self.calc.toPercent(self.calc.termCount(1)[-2],self.calc.termCount(1)[1])	
			self.TermAvg(alList,perc)

		if self.ui.comboBox.itemText(self.ui.comboBox.currentIndex()) == "Term Three":
			alList=self.calc.LearnerNamesPerc(self.ui.listWidget.currentItem().text(),2,False)
			self.ui.lineEdit.setText(str(alList[0][0]))
			self.ui.lineEdit_2.setText(str(alList[0][1]))
			self.ui.lineEdit_3.setText(str(alList[0][2]))
			self.ui.lineEdit_4.setText(str(alList[0][3]))
			self.ui.lineEdit_5.setText(str(alList[0][4]))

			self.ui.lineEdit_11.setVisible(False)
			self.ui.label_4.setText(alList[2][0])
			self.ui.label_5.setText(alList[2][1])
			self.ui.label_6.setText(alList[2][2])
			self.ui.label_7.setText(alList[2][3])
			self.ui.label_8.setText(alList[2][4])
			self.ui.label_18.setVisible(False)

			self.ui.lineEdit_12.setText(str(alList[1][0]))
			self.ui.lineEdit_13.setText(str(alList[1][1]))
			self.ui.lineEdit_14.setText(str(alList[1][2]))
			self.ui.lineEdit_15.setText(str(alList[1][3]))
			self.ui.lineEdit_16.setText(str(alList[1][4]))
			self.ui.lineEdit_17.setVisible(False)
			if alList[0][4]< (alList[1][4])*0.3:
				self.ui.label_8.setStyleSheet("background-color: rgb(255, 0,4 ,255);color:rgb(255, 255,255,255);")

			else :
				self.ui.label_8.setStyleSheet("background-color:rgb(0, 0,0 ,0;color:rgb(0, 0,0 ,0);")

			perc=self.calc.toPercent(self.calc.termCount(2)[-2],self.calc.termCount(2)[1])	
			self.TermAvg(alList,perc)
	
	def TermAvg(self,listy,perc):
		termpercent=self.calc.toPercent(listy[0],listy[1])
		avg=np.array(termpercent)
		avg=np.average(avg)
		self.ui.label_35.setText(str("%.1f"%avg +"%"))
		if self.ui.radioButton_3.isChecked():
			self.diplaMarkBar(termpercent,perc)
		if self.ui.radioButton_4.isChecked():
			self.displMarkScatter(termpercent,perc)

	def diplaMarkBar(self,list1,list2):
		self.chart = QChart()
		classAvg = QBarSet("Learner Mark")
		for i in range(0, len(list1)):
			classAvg << list1[i]

		learnerMark = QBarSet("Class Average")
		for k in range(0, len(list2)):
			learnerMark << list2[k]
		self.termSeries = QBarSeries()
		self.termSeries.append(classAvg)
		self.termSeries.append(learnerMark)
		self.chart.addSeries(self.termSeries)
		self.chart.setAnimationOptions(QChart.SeriesAnimations)
		theme = self.chart.ChartTheme(0)
		self.chart.setTheme(theme)
		self.axis = QBarCategoryAxis()
		# self.axis.append(termlist)
		self.axis = QBarCategoryAxis()
		self.axis.setTitleText("TESTS")
		self.chart.createDefaultAxes()
		self.chart.setAxisX(self.axis, self.termSeries)
		self.chart.axisY(self.termSeries).setTitleText("Perofrmance")
		self.chart.legend().setVisible(True)
		self.chartView1 = QChartView(self.chart)
		self.chartView1.setGeometry(QtCore.QRect(0, 0, 518, 408))
		self.chartView1.setRenderHint(QPainter.Antialiasing)
		scen = QtWidgets.QGraphicsScene()
		scen.addWidget(self.chartView1)
		self.ui.graphicsView.setScene(scen)


	def displMarkScatter(self,list1,list2):
		tasknams=self.calc.termCount(2)[-1]
		self.figure = Figure()
		self.canvas = FigureCanvas(self.figure)
		self.canvas.setGeometry(QtCore.QRect(290, 70, 518, 408))
		scen = QtWidgets.QGraphicsScene()
		scen.addWidget(self.canvas)
		self.ui.graphicsView.setScene(scen)

		ax = self.figure.add_subplot(111)
		ax.clear()
		ax.plot(tasknams,list1, "*-")
		ax.plot(list2, "o-")
		ax.legend([self.ui.listWidget.currentItem().text(), 'class average'])
		ax.grid()
		self.canvas.show()

	def taskTab(self):
		taskNames=self.calc.tasknames
		termz=self.calc.terms
		if self.ui.radioButton_5.isChecked():
			for k in termz[0]:
				self.ui.listWidget_3.addItem(taskNames[k])

		if self.ui.radioButton_6.isChecked():
			for k in termz[1]:
				self.ui.listWidget_3.addItem(taskNames[k])

		if self.ui.radioButton_7.isChecked():
			for k in termz[2]:
				self.ui.listWidget_3.addItem(taskNames[k])

	def taskSelected(self):
		taskDetail=self.calc.taskMark(self.calc.tasknames.index(self.ui.listWidget_3.currentItem().text()))
		self.distribGraph(taskDetail[6])

	def distribGraph(self, taskmarklist):
		"""This function is for diplaying the data into the Graph
		This graph has the following fuctions 
		#Mean
		#Number of learners 
		#Number of passed learners 
		#Number of failed learners 
		#Percentage of passed learners 


		"""

		figure = Figure(linewidth=1.0)
		figure.add_axes(ylabel="Number of Learners")
		canvas = FigureCanvas(figure)
		canvas.setGeometry(QtCore.QRect(0, 0, 688, 328))
		scen = QtWidgets.QGraphicsScene()
		scen.addWidget(canvas)
		self.ui.graphicsView_2.setScene(scen)
		nam=self.ui.listWidget_3.currentItem().text()
		ax = figure.add_subplot(111,facecolor=(0.1,0.3,0.5,0.2),position=[0.05,0.09,0.93,0.9],xbound=(0.8,0.6))
		ax.clear()
		ax.hist(taskmarklist,)
		ax.legend([nam])
		# ax.legend(["TASK NAME"])
		canvas.show()


	def UploadButton(self):
		self.filename = QFileDialog.getOpenFileName(self, "Open File", "c:\\", "Document files (*.xlsx *.xls)")
		self.direw = self.filename[0]
		if self.direw != "":
			self.ui.lineEdit_9.setText(str(self.direw))
			self.ui.label_53.setText(str((self.calc.Teacher)[0]))
			self.ui.label_57.setText(str(self.calc.classGrade))

if __name__ == "__main__":
	app = QApplication(sys.argv)
	#app.setStyle(QStyleFactory.create("Fusion"))
	schoolui = mainClass()
	schoolui.show()
	sys.exit(app.exec_())

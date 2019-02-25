from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def donutchart(posx,posy,height,width,colors,labels,datalist,labflag):
	charty=QChartView()
	charty.chart().setGeometry(QRectF(posx,posy,width,height))
	#charty.chart().setBackgroundVisible(True)
	charty.chart().setTheme(QChart.ChartThemeDark)
	charty.setBackgroundBrush(QBrush(QColor(90, 86, 73,200)))
	charty.chart().setBackgroundBrush(QBrush(QColor(255, 255, 255, 50)))
	charty.setRenderHint(QPainter.Antialiasing)
	charty.setRenderHint(QPainter.Antialiasing)
	charty.chart().setPlotAreaBackgroundVisible(True)
	#charty.chart().setPlotAreaBackgroundBrush(QColor(255, 255, 255,200))
	chartplot = charty.chart()
	chartplot.legend().setVisible(labflag)
	chartplot.legend().setAlignment(Qt.AlignRight)
	chartplot.setAnimationOptions(QChart.AllAnimations)
	donut=QPieSeries()
	for i in range(0,len(datalist)):
		m_slice = QPieSlice(labels[i],datalist[i])
		m_slice.setExploded(False)
		m_slice.setLabelVisible(False)
		m_slice.setColor(QColor(colors[i]))
		#m_slice = setLabelPosition(QpieSLice.Label)
		donut.append(m_slice)
	donut.setHoleSize(0.6)
	donut.setPieSize(0.95)
	charty.chart().addSeries(donut)
	

	return charty


def scatterPlot(labels,list1):
	figure = Figure()
	canvas = FigureCanvas(figure)
	canvas.setGeometry(QRect(290, 70, 530, 325))	
	ax = figure.add_subplot(111)
	ax.clear()
	ax.plot(labels,list1)
	#ax.legend(labels)
	#ax.grid()
	#canvas.show()
	return canvas




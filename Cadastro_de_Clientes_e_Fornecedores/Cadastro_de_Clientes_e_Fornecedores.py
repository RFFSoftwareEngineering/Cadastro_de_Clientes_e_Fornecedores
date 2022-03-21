import sys
from PyQt6 import QtWidgets, QtGui, QtCore, QtSql
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtSql import *
import time
from datetime import date

today = date.today()
strf_today = today.strftime("%d/%m/%Y")


class MainTree(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Some Company") # let's do a vertical-based layout as the main layout
        self.setStyleSheet("background-color: #e9f2f0")
        self.setWindowIcon(QIcon("SomeLogo"))
        self.move(375, 75)

        self.main_layout = QGridLayout(self)  # but a grid layout for the main window
        self.setLayout(self.main_layout)

        self.Logo = QPixmap("SomeLogo")
        self.Logolbl = QLabel("", self)
        self.Logolbl.setPixmap(self.Logo)
        self.Logolbl.setStyleSheet("padding-left: 190px; padding-top: 80px; padding-right: 150px; padding-bottom: 325px;")

        self.main_layout.addWidget(self.Logolbl, 0, 0)

        self.widget_main = QWidget(self)

        self.main_layout2 = QHBoxLayout(self.widget_main) #layout for the buttons

        self.widget_main.setLayout(self.main_layout2)

        self.CadIcon = QPixmap("cadastro")
        self.CadIcon = self.CadIcon.scaledToWidth(49)
        self.CadLbl = QLabel("", self.widget_main)
        self.CadLbl.setPixmap(self.CadIcon)

        self.CadastroBtn = QPushButton("Cadastros", self.widget_main)
        self.CadastroBtn.setFont(QFont("Arial", 12, 2))
        self.CadastroBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px; padding-right: 600px;} QPushButton:hover {background-color: #5ac47e}")
        self.CadastroBtn.clicked.connect(self.CreateRegistersWindow)

        self.main_layout2.addWidget(self.CadLbl)
        self.main_layout2.addWidget(self.CadastroBtn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.main_layout.addWidget(self.widget_main)
    
        self.show()

    def CreateRegistersWindow(self):
        self.ClientsWindow = QScrollArea()  # QScrollArea as Parent of a Widget to the application works as we expect
        self.widget = QWidget(self.ClientsWindow)
        self.ClientsWindow.setGeometry(480, 200, 1300, 720)
        self.ClientsWindow.showMaximized()
        self.ClientsWindow.setWindowTitle("Some Company - Cadastros")
        self.ClientsWindow.setStyleSheet("background-color: #e9f2f0")
        self.ClientsWindow.setWindowIcon(QIcon("SomeLogo"))
        self.ClientsWindow.show()

        self.layout = QVBoxLayout(self.widget) # let's override the scrollbar this way
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ClientsWindow.setWidget(self.widget)
        self.ClientsWindow.setWidgetResizable(True)
        self.widget.setLayout(self.layout)

        self.lblcls = QLabel("Clientes e Fornecedores", self.ClientsWindow)
        self.lblcls.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lblcls.setFont(QFont("Arial", 16, 12))
        self.lblcls.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; font-weight: bold;")

        self.search_widget = QWidget(self.widget)

        self.search_layout = QHBoxLayout(self.search_widget) # treating every 'bunch' of widgets as a div

        self.search_widget.setLayout(self.search_layout)

        self.layout.addWidget(self.lblcls)

        self.buscaedt = QLineEdit("Selecionar método de busca e digitar:", self.search_widget)
        self.buscaedt.setStyleSheet("border-radius: 7px; background-color: white; color: gray; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;")
        self.buscaedt.setMaximumWidth(450)
        self.buscaedt.returnPressed.connect(self.ClearBusca)
        self.buscaedt.mousePressEvent = self.ClearBusca

        self.layout.addWidget(self.search_widget)
        self.search_layout.addWidget(self.buscaedt)
        
        self.btnbusca = QPushButton("", self.search_widget)
        self.btnbusca.setIcon(QIcon("search-icon.png"))
        self.btnbusca.setIconSize(QSize(25, 25))
        self.btnbusca.setMaximumWidth(35)
        self.btnbusca.setAutoDefault(True)
        self.btnbusca.clicked.connect(self.RegSrchOne)

        self.search_layout.addSpacing(30)

        self.layout.addWidget(self.search_widget)
        self.search_layout.addWidget(self.btnbusca, alignment=Qt.AlignmentFlag.AlignLeft)

        self.searchby = QComboBox(self.search_widget)
        self.searchby.setStyleSheet("border-radius: 7px; background-color: white; color: gray; padding: 7px 12px; border-width:1px; border-color: gray; border-style: solid;")
        self.searchby.addItems(["Nome", "CNPJ", "ID"])
        self.searchby.activated.connect(self.ActivatedCB)
        self.searchby.currentTextChanged.connect(self.ItemSelectedCB)

        self.search_layout.addSpacing(-941)

        self.search_layout.addWidget(self.searchby, alignment=Qt.AlignmentFlag.AlignLeft)

        self.regdata = QLabel("Dados Cadastrais", self.ClientsWindow)
        self.regdata.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; font-weight: bold; padding-top: 10px;")
        self.regdata.setFont(QFont("Arial", 16, 12))

        self.layout.addWidget(self.regdata)

        self.data_widget = QWidget(self.widget)

        self.data_layout = QGridLayout(self.data_widget)        

        self.data_widget.setLayout(self.data_layout)

        self.lblcls2 = QLabel("Nome*", self.data_widget)
        self.lblcls2.setFont(QFont("Arial", 10, 4))
        self.lblcls2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.data_layout.addWidget(self.lblcls2, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.data_widget)

        self.fantasylbl = QLabel("Fantasia", self.data_widget)
        self.fantasylbl.setFont(QFont("Arial", 10, 4))
        self.fantasylbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.data_layout.addWidget(self.fantasylbl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.persontypelbl = QLabel("Tipo de Pessoa", self.data_widget)
        self.persontypelbl.setFont(QFont("Arial", 10, 4))
        self.persontypelbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top: 15px;")

        self.data_layout.addWidget(self.persontypelbl, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.nameedt = QLineEdit("", self.data_widget)
        self.nameedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.nameedt.setFixedWidth(500)
        self.nameedt.setFont(QFont("Arial", 12, 12))

        self.data_layout.addWidget(self.nameedt, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.fanedt = QLineEdit("", self.data_widget)
        self.fanedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.fanedt.setFixedWidth(500)
        self.fanedt.setFont(QFont("Arial", 12, 12))

        self.data_layout.addWidget(self.fanedt, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.personbox = QComboBox(self.data_widget)
        self.personbox.setStyleSheet("QComboBox {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QComboBox:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.personbox.setFixedWidth(500)
        self.personbox.setFont(QFont("Arial", 12, 12))
        self.personbox.addItems(["Pessoa Jurídica", "Pessoa Física", "Estrangeiro"])
        self.personbox.activated.connect(self.ActivatedPerson)
        self.personbox.currentTextChanged.connect(self.SelectedPerson)

        self.data_layout.addWidget(self.personbox, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.input3 = self.personbox.currentText()

        self.data_widget2 = QWidget(self.widget)

        self.data_layout2 = QGridLayout(self.data_widget2)

        self.cnpjorcpflbl = QLabel("CNPJ", self.data_widget2)
        self.cnpjorcpflbl.setFont(QFont("Arial", 10, 4))
        self.cnpjorcpflbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top: 15px;")

        self.data_layout2.addWidget(self.cnpjorcpflbl, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.codelbl = QLabel("Código de Regime Tributário", self.data_widget2)
        self.codelbl.setFont(QFont("Arial", 10, 4))
        self.codelbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px; padding-left: 0px;")

        self.data_layout2.addWidget(self.codelbl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.clientlbl = QLabel("Cliente desde", self.data_widget2)
        self.clientlbl.setFont(QFont("Arial", 10, 4))
        self.clientlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px; padding-left: 4px;")

        self.data_layout2.addWidget(self.clientlbl, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.cnpjedt = QLineEdit("", self.data_widget2)
        self.cnpjedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cnpjedt.setFixedWidth(500)
        self.cnpjedt.setFont(QFont("Arial", 12, 12))

        self.cpfedt = QLineEdit("", self.data_widget2)
        self.cpfedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cpfedt.setFixedWidth(500)
        self.cpfedt.setFont(QFont("Arial", 12, 12))
        self.cpfedt.hide()

        self.data_layout2.addWidget(self.cnpjedt, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.data_layout2.addWidget(self.cpfedt, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.codebox = QComboBox(self.data_widget2)
        self.codebox.setStyleSheet("QComboBox {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid; padding-left: 15px;} QComboBox:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.codebox.setFixedWidth(500)
        self.codebox.setFont(QFont("Arial", 12, 12))
        self.codebox.addItems(["Não Definido", "Simples Nacional", "Simples Nacional - Excesso de sublimite de receita bruta", "Regime Normal"])
        self.codebox.activated.connect(self.ActivatedPerson)
        self.codebox.currentTextChanged.connect(self.SelectedPerson)

        self.data_layout2.setHorizontalSpacing(20)
        self.data_layout2.addWidget(self.codebox, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.desdeedt = QLineEdit(f"{strf_today}", self.data_widget2)
        self.desdeedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.desdeedt.setFixedWidth(235)
        self.desdeedt.setFont(QFont("Arial", 12, 12))
        self.desdeedt.setInputMask("99/99/9999")

        self.data_layout2.addWidget(self.desdeedt, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.contriblbl = QLabel("Contribuinte", self.data_widget2)
        self.contriblbl.setFont(QFont("Arial", 10, 4))
        self.contriblbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.data_layout2.addWidget(self.contriblbl, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        self.contribbox = QComboBox(self.data_widget2)
        self.contribbox.setStyleSheet("QComboBox {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QComboBox:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;} QComboBox QAbstractItemView {min-width: 500px;}")
        self.contribbox.setFixedWidth(230)
        self.contribbox.setFont(QFont("Arial", 12, 12))
        self.contribbox.addItems(["1 - Contribuinte ICMS", "2 - Contribuinte isento de inscrição no cadastro de contribuintes", "3 - Não contribuinte que pode ou não possuir inscrição estadual"])
        self.contribbox.activated.connect(self.ActivatedPerson)
        self.contribbox.currentTextChanged.connect(self.SelectedPerson)

        self.countryedt = QLineEdit(self.data_widget2)
        self.countryedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.countryedt.setFixedWidth(230)
        self.countryedt.setFont(QFont("Arial", 12, 12))
        self.countryedt.hide()

        self.data_layout2.addWidget(self.contribbox, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        self.data_layout2.addWidget(self.countryedt, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        self.layout.addWidget(self.data_widget2)

        self.statereglbl = QLabel("Inscrição Estadual", self.data_widget2)
        self.statereglbl.setFont(QFont("Arial", 10, 4))
        self.statereglbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:35px;")

        self.cityreglbl = QLabel("Inscrição Municipal", self.data_widget2)
        self.cityreglbl.setFont(QFont("Arial", 10, 4))
        self.cityreglbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:35px;")

        self.data_layout2.addWidget(self.statereglbl, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.data_layout2.addWidget(self.cityreglbl, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.stateregedt = QLineEdit("", self.data_widget2)
        self.stateregedt.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stateregedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.stateregedt.setFixedWidth(500)
        self.stateregedt.setFont(QFont("Arial", 12, 12))

        self.RGEdt = QLineEdit("", self.data_widget2)
        self.RGEdt.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.RGEdt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.RGEdt.setFixedWidth(500)
        self.RGEdt.setFont(QFont("Arial", 12, 12))
        self.RGEdt.hide()

        self.cityregedt = QLineEdit("", self.data_widget2)
        self.cityregedt.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cityregedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cityregedt.setFixedWidth(500)
        self.cityregedt.setFont(QFont("Arial", 12, 12))

        self.emissedt = QLineEdit("", self.data_widget2)
        self.emissedt.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.emissedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.emissedt.setFixedWidth(500)
        self.emissedt.setFont(QFont("Arial", 12, 12))
        self.emissedt.hide()

        self.data_layout2.addWidget(self.stateregedt, 3, 0)
        self.data_layout2.addWidget(self.RGEdt, 3, 0)
        self.data_layout2.addWidget(self.cityregedt, 3, 1)
        self.data_layout2.addWidget(self.emissedt, 3, 1)

        self.IEchck = QCheckBox("IE Isento", self.data_widget2)
        self.IEchck.setStyleSheet("""
                                    QCheckBox {
                                    color: rgb(102, 102, 102); 
                                    letter-spacing: 1px; 
                                    padding-top: 2px; 
                                    spacing: 8px; 
                                    padding-left: 15px;
                                    } 
                                    QCheckBox::indicator {
                                    width: 30px;
                                    height: 30px;
                                    }
                                    QCheckBox::indicator:unchecked {
                                    image: url(IEcheck-unchecked.png);
                                    }
                                    QCheckBox::indicator:checked {
                                    image: url(IEcheck-checked.png);
                                    }
                                    QCheckBox::indicator:hover {
                                    image: url(IEcheck-hover.png);
                                    }
                                    QCheckBox::indicator:checked:hover {
                                    image: url(IEcheck-checked-hover.png);
                                    }
                                 """)
        self.IEchck.setFont(QFont("Arial", 10, 12))
        self.IEchck.stateChanged.connect(self.IE_Check)

        self.data_layout2.addWidget(self.IEchck, 3, 2)

        self.lbladr = QLabel("Endereço", self.widget)
        self.lbladr.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lbladr.setFont(QFont("Arial", 16, 12))
        self.lbladr.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; font-weight: bold; padding-top: 15px;")

        self.layout.addWidget(self.lbladr)

        self.AdrTab = QTabWidget(self.ClientsWindow)
        self.AdrTab.setFont(QFont("Arial", 12, 12))
        self.AdrTab.setStyleSheet("""
                                     QTabWidget::pane {
                                       border: 1px solid lightgray;
                                       top:-1px; 
                                       background: #e9f2f0;
                                       color: rgb(102, 102, 102);
                                     } 
                                     QTabBar::tab {
                                       background: #e9f2f0; 
                                       border: 1px solid lightgray; 
                                       padding: 15px;
                                       color: rgb(102, 102, 102);
                                     } 
                                     QTabBar::tab:selected { 
                                       background: #e9f2f0; 
                                       margin-bottom: -1px; 
                                       color: #44a665;
                                       font-weight: bold;
                                       text-decoration: underline;
                                     }       
                                  """)
        

        """
            Ok, the logic here is:
                -> We set a QScrollArea as the main widget of the 'frame' QTabWidget...
                -> Then we make a normal QWidget with QScrollArea as parent to the layout work as we expect and add automatically a srcoll bar if it needs
                -> Then we set the layout of QWidget(frame) as a QVBoxLayout to add layouts (frames) as divs in html
                -> Then we use this as the main layout to add new divs
                -> Then we make QWidgets as is were 'divs' and the desired layout for them
                -> Then we just add using main_layout and everything will work just fine
        """


        self.ChargerTabs = QScrollArea()  
        self.charger_widget = QWidget(self.ChargerTabs)

        self.charger_layout_main = QVBoxLayout(self.charger_widget) 
        self.charger_layout_main.setAlignment(Qt.AlignmentFlag.AlignTop) 
        self.ChargerTabs.setWidget(self.charger_widget)
        self.ChargerTabs.setWidgetResizable(True)
        self.charger_widget.setLayout(self.charger_layout_main)


        self.charger_widget1 = QWidget(self.charger_widget) # widget 1 for tab 1

        self.layoutadr1 = QGridLayout(self.charger_widget1) # with a QGridLayout layout within a VBoxLayout

        self.charger_widget1.setLayout(self.layoutadr1) 

        self.charger_layout_main.addWidget(self.charger_widget1)

        self.ChargerTabs2 = QScrollArea()  
        self.charger_widget2 = QWidget(self.ChargerTabs2)

        self.charger_layout_main2 = QVBoxLayout(self.charger_widget2) 
        self.charger_layout_main2.setAlignment(Qt.AlignmentFlag.AlignTop) 
        self.ChargerTabs2.setWidget(self.charger_widget2)
        self.ChargerTabs2.setWidgetResizable(True)
        self.charger_widget2.setLayout(self.charger_layout_main2)

        self.charger_widget3 = QWidget(self.charger_widget2) # widget 1 for tab 2

        self.layoutadr2 = QGridLayout(self.charger_widget3) # with a QGridLayout layout within a VBoxLayout

        self.charger_widget3.setLayout(self.layoutadr2) 
        self.charger_layout_main2.addWidget(self.charger_widget3)

        self.charger_widget4 = QWidget(self.charger_widget2) # widget 2 for tab 1

        self.layoutadr3 = QGridLayout(self.charger_widget4) # with a QGridLayout layout within a VBoxLayout

        self.charger_widget4.setLayout(self.layoutadr3) 

        self.charger_layout_main.addWidget(self.charger_widget4)

        self.charger_widget5 = QWidget(self.charger_widget2) # widget 2 for tab 2

        self.layoutadr4 = QGridLayout(self.charger_widget5) # with a QGridLayout layout within a VBoxLayout

        self.charger_widget5.setLayout(self.layoutadr4) 

        self.charger_layout_main2.addWidget(self.charger_widget5)

        self.layoutadr1.setHorizontalSpacing(35)

        self.layoutadr2.setHorizontalSpacing(35)

        self.layoutadr3.setHorizontalSpacing(35)

        self.layoutadr4.setHorizontalSpacing(35)

        self.charger_widget1.setMaximumHeight(150)

        self.AdrTab.addTab(self.charger_widget, "Geral")
        self.AdrTab.addTab(self.charger_widget2, "Cobrança")
        
        self.layout.addWidget(self.AdrTab)

        self.CEPlbl = QLabel("CEP", self.charger_widget1)
        self.CEPlbl.setFont(QFont("Arial", 10, 4))
        self.CEPlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top: 15px;")   
        
        self.CEPlbl2 = QLabel("CEP", self.charger_widget3)
        self.CEPlbl2.setFont(QFont("Arial", 10, 4))
        self.CEPlbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top: 15px;")

        self.layoutadr1.addWidget(self.CEPlbl, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.CEPlbl2, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self.cepedt1 = QLineEdit("", self.charger_widget1)
        self.cepedt1.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cepedt1.setFixedWidth(220)
        self.cepedt1.setFont(QFont("Arial", 12, 12))
        self.cepedt1.setInputMask("99999-999")
        self.cepedt1.returnPressed.connect(self.RegSrch)
        self.cepedt1.mousePressEvent = self.RegSrch

        self.cepedt2 = QLineEdit("", self.charger_widget3)
        self.cepedt2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cepedt2.setFixedWidth(220)
        self.cepedt2.setFont(QFont("Arial", 12, 12))
        self.cepedt2.setInputMask("99999-999")

        self.layoutadr1.addWidget(self.cepedt1, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr2.addWidget(self.cepedt2, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.adrsearch = QPushButton("", self.charger_widget1)
        self.adrsearch.setIcon(QIcon("search-icon.png"))
        self.adrsearch.setIconSize(QSize(25, 25))
        self.adrsearch.setAutoDefault(True) 
        self.adrsearch.setMaximumWidth(35)

        self.adrsearch2 = QPushButton("", self.charger_widget3)
        self.adrsearch2.setIcon(QIcon("search-icon.png"))
        self.adrsearch2.setIconSize(QSize(25, 25))
        self.adrsearch2.setAutoDefault(True)
        self.adrsearch2.setMaximumWidth(35)

        self.layoutadr2.addWidget(self.adrsearch2, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr1.addWidget(self.adrsearch, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.buscalbl = QLabel(" ", self.charger_widget1)
        self.buscalbl.setFont(QFont("Arial", 10, 4))
        self.buscalbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.buscalbl2 = QLabel(" ", self.charger_widget3)
        self.buscalbl2.setFont(QFont("Arial", 10, 4))
        self.buscalbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.layoutadr1.addWidget(self.buscalbl, 0, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.buscalbl2, 0, 1, alignment=Qt.AlignmentFlag.AlignTop)

        self.uflbl = QLabel("UF", self.charger_widget1)
        self.uflbl.setFont(QFont("Arial", 10, 4))
        self.uflbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.uflbl2 = QLabel("UF", self.charger_widget3)
        self.uflbl2.setFont(QFont("Arial", 10, 4))
        self.uflbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.layoutadr1.addWidget(self.uflbl, 0, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.uflbl2, 0, 2, alignment=Qt.AlignmentFlag.AlignTop)

        self.statebox = QComboBox(self.charger_widget1)
        self.statebox.setStyleSheet("QComboBox {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QComboBox:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.statebox.setFont(QFont("Arial", 12, 12))
        self.statebox.addItems(["SP", "RJ", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RN", "RS", "RO", "RR", "SC", "SE", "TO"])
        self.statebox.setFixedWidth(220)
        self.statebox.activated.connect(self.ActivatedPerson)
        self.statebox.currentTextChanged.connect(self.SelectedPerson)

        self.statebox2 = QComboBox(self.charger_widget3)
        self.statebox2.setStyleSheet("QComboBox {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QComboBox:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.statebox2.setFont(QFont("Arial", 12, 12))
        self.statebox2.addItems(["SP", "RJ", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RN", "RS", "RO", "RR", "SC", "SE", "TO"])
        self.statebox2.setFixedWidth(220)
        self.statebox2.activated.connect(self.ActivatedPerson)
        self.statebox2.currentTextChanged.connect(self.SelectedPerson)

        self.foreign_state = QLineEdit(self.charger_widget1)
        self.foreign_state.setFont(QFont("Arial", 12, 12))
        self.foreign_state.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.foreign_state.setFixedWidth(220)
        self.foreign_state.hide()

        self.foreign_state2 = QLineEdit(self.charger_widget1)
        self.foreign_state2.setFont(QFont("Arial", 12, 12))
        self.foreign_state2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.foreign_state2.setFixedWidth(220)
        self.foreign_state2.hide()

        self.layoutadr1.addWidget(self.statebox, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.statebox2, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr1.addWidget(self.foreign_state, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.foreign_state2, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)


        self.citylbl = QLabel("Cidade", self.charger_widget1)
        self.citylbl.setFont(QFont("Arial", 10, 4))
        self.citylbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.citylbl2 = QLabel("Cidade", self.charger_widget3)
        self.citylbl2.setFont(QFont("Arial", 10, 4))
        self.citylbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.layoutadr1.addWidget(self.citylbl, 0, 3, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.citylbl2, 0, 3, alignment=Qt.AlignmentFlag.AlignTop)

        self.cityedt = QLineEdit("", self.charger_widget1)
        self.cityedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cityedt.setFont(QFont("Arial", 12, 12))
        self.cityedt.setFixedWidth(500)

        self.cityedt2 = QLineEdit("", self.charger_widget3)
        self.cityedt2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cityedt2.setFont(QFont("Arial", 12, 12))
        self.cityedt2.setFixedWidth(500)

        self.layoutadr1.addWidget(self.cityedt, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.cityedt2, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)

        self.bairrolbl = QLabel("Bairro", self.charger_widget1)
        self.bairrolbl.setFont(QFont("Arial", 10, 4))
        self.bairrolbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.bairrolbl2 = QLabel("Bairro", self.charger_widget3)
        self.bairrolbl2.setFont(QFont("Arial", 10, 4))
        self.bairrolbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.layoutadr1.addWidget(self.bairrolbl, 0, 4, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.bairrolbl2, 0, 4, alignment=Qt.AlignmentFlag.AlignTop)

        self.bairroedt = QLineEdit("", self.charger_widget1)
        self.bairroedt.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bairroedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.bairroedt.setFont(QFont("Arial", 12, 12))
        self.bairroedt.setFixedWidth(420)

        self.bairroedt2 = QLineEdit("", self.charger_widget3)
        self.bairroedt2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bairroedt2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.bairroedt2.setFont(QFont("Arial", 12, 12))
        self.bairroedt2.setFixedWidth(420)

        self.layoutadr1.addWidget(self.bairroedt, 1, 4, alignment=Qt.AlignmentFlag.AlignTop)
        self.layoutadr2.addWidget(self.bairroedt2, 1, 4, alignment=Qt.AlignmentFlag.AlignTop)

        # widget 2 for tab 1 and 2 below:
        
        self.enderecolbl = QLabel("Endereço", self.charger_widget4)
        self.enderecolbl.setFont(QFont("Arial", 10, 4))
        self.enderecolbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")   
        
        self.enderecolbl2 = QLabel("Endereço", self.charger_widget5)
        self.enderecolbl2.setFont(QFont("Arial", 10, 4))
        self.enderecolbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.layoutadr3.addWidget(self.enderecolbl, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr4.addWidget(self.enderecolbl2, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.enderecoedt1 = QLineEdit("", self.charger_widget4)
        self.enderecoedt1.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.enderecoedt1.setFixedWidth(650)
        self.enderecoedt1.setFont(QFont("Arial", 12, 12))

        self.enderecoedt2 = QLineEdit("", self.charger_widget5)
        self.enderecoedt2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.enderecoedt2.setFixedWidth(650)
        self.enderecoedt2.setFont(QFont("Arial", 12, 12))

        self.layoutadr3.addWidget(self.enderecoedt1, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr4.addWidget(self.enderecoedt2, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.numerolbl = QLabel("Número", self.charger_widget4)
        self.numerolbl.setFont(QFont("Arial", 10, 4))
        self.numerolbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.numerolbl2 = QLabel("Número", self.charger_widget5)
        self.numerolbl2.setFont(QFont("Arial", 10, 4))
        self.numerolbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.layoutadr3.addWidget(self.numerolbl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr4.addWidget(self.numerolbl2, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.numeroedt = QLineEdit("", self.charger_widget4)
        self.numeroedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.numeroedt.setFont(QFont("Arial", 12, 12))
        self.numeroedt.setFixedWidth(250)

        self.numeroedt2 = QLineEdit("", self.charger_widget5)
        self.numeroedt2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.numeroedt2.setFixedWidth(250)
        self.numeroedt2.setFont(QFont("Arial", 12, 12))

        self.layoutadr3.addWidget(self.numeroedt, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr4.addWidget(self.numeroedt2, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.complementlbl = QLabel("Complemento", self.charger_widget4)
        self.complementlbl.setFont(QFont("Arial", 10, 4))
        self.complementlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.complementlbl2 = QLabel("Complemento", self.charger_widget5)
        self.complementlbl2.setFont(QFont("Arial", 10, 4))
        self.complementlbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.layoutadr3.addWidget(self.complementlbl, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr4.addWidget(self.complementlbl2, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.complementedt = QLineEdit("", self.charger_widget4)
        self.complementedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.complementedt.setFont(QFont("Arial", 12, 12))
        self.complementedt.setFixedWidth(560)

        self.complementedt2 = QLineEdit("", self.charger_widget5)
        self.complementedt2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.complementedt2.setFont(QFont("Arial", 12, 12))
        self.complementedt2.setFixedWidth(560)

        self.layoutadr3.addWidget(self.complementedt, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr4.addWidget(self.complementedt2, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.contatolbl = QLabel("Contato", self.ClientsWindow)
        self.contatolbl.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contatolbl.setFont(QFont("Arial", 16, 12))
        self.contatolbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; font-weight: bold; padding-top: 15px;")

        self.layout.addWidget(self.contatolbl, alignment=Qt.AlignmentFlag.AlignLeft)

        self.infolbl = QLabel("Informações do Contato", self.ClientsWindow)
        self.infolbl.setFont(QFont("Arial", 10, 4))
        self.infolbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")
        
        self.layout.addWidget(self.infolbl)

        self.infoedt = QLineEdit("", self.ClientsWindow)
        self.infoedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.infoedt.setFixedWidth(840)
        self.infoedt.setFont(QFont("Arial", 12, 12))

        self.layout.addWidget(self.infoedt, alignment=Qt.AlignmentFlag.AlignLeft)

        self.peoplelbl = QLabel("Pessoas de Contato", self.ClientsWindow)
        self.peoplelbl.setFont(QFont("Arial", 10, 4))
        self.peoplelbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")
        
        self.layout.addWidget(self.peoplelbl, alignment=Qt.AlignmentFlag.AlignLeft)

        self.pessoasedt = QLineEdit("", self.ClientsWindow)
        self.pessoasedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.pessoasedt.setFixedWidth(840)
        self.pessoasedt.setFont(QFont("Arial", 12, 12))

        self.layout.addWidget(self.pessoasedt, alignment=Qt.AlignmentFlag.AlignLeft)

        self.contact_widget = QWidget(self.ClientsWindow) # widget for contact information

        self.contact_layout = QGridLayout(self.contact_widget) # with a QGridLayout layout within a VBoxLayout

        self.contact_layout.setHorizontalSpacing(16)

        self.layout.addWidget(self.contact_widget)

        self.fonelbl = QLabel("Fone", self.contact_widget)
        self.fonelbl.setFont(QFont("Arial", 10, 4))
        self.fonelbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.foneedt = QLineEdit("", self.contact_widget)
        self.foneedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.foneedt.setFont(QFont("Arial", 12, 12))
        self.foneedt.setFixedWidth(250)

        self.contact_layout.addWidget(self.fonelbl, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout.addWidget(self.foneedt, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.faxlbl = QLabel("Fax", self.contact_widget)
        self.faxlbl.setFont(QFont("Arial", 10, 4))
        self.faxlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.faxedt = QLineEdit("", self.contact_widget)
        self.faxedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.faxedt.setFont(QFont("Arial", 12, 12))
        self.faxedt.setFixedWidth(250)

        self.contact_layout.addWidget(self.faxlbl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout.addWidget(self.faxedt, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.cellbl = QLabel("Celular", self.contact_widget)
        self.cellbl.setFont(QFont("Arial", 10, 4))
        self.cellbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.celedt = QLineEdit("", self.contact_widget)
        self.celedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.celedt.setFont(QFont("Arial", 12, 12))
        self.celedt.setFixedWidth(250)

        self.contact_layout.addWidget(self.cellbl, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout.addWidget(self.celedt, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.cellbl2 = QLabel("Celular 2", self.contact_widget)
        self.cellbl2.setFont(QFont("Arial", 10, 4))
        self.cellbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.celedt2 = QLineEdit("", self.contact_widget)
        self.celedt2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.celedt2.setFont(QFont("Arial", 12, 12))
        self.celedt2.setFixedWidth(250)

        self.contact_layout.addWidget(self.cellbl2, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout.addWidget(self.celedt2, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        self.emaillbl = QLabel("E-mail", self.charger_widget1)
        self.emaillbl.setFont(QFont("Arial", 10, 4))
        self.emaillbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.emailedt = QLineEdit("", self.charger_widget1)
        self.emailedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.emailedt.setFont(QFont("Arial", 12, 12))
        self.emailedt.setFixedWidth(475)

        self.contact_layout.addWidget(self.emaillbl, 0, 4, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout.addWidget(self.emailedt, 1, 4, alignment=Qt.AlignmentFlag.AlignLeft)

        self.contact_widget2 = QWidget(self.ClientsWindow) # widget for contact information part 2

        self.contact_layout2 = QGridLayout(self.contact_widget2) # with a QGridLayout layout within a VBoxLayout

        self.contact_layout2.setHorizontalSpacing(16)

        self.layout.addWidget(self.contact_widget2)

        self.emaillblnfe = QLabel("E-mail para envio de NFe", self.contact_widget2)
        self.emaillblnfe.setFont(QFont("Arial", 10, 4))
        self.emaillblnfe.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.emailedtnfe = QLineEdit("", self.contact_widget2)
        self.emailedtnfe.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.emailedtnfe.setFont(QFont("Arial", 12, 12))
        self.emailedtnfe.setFixedWidth(519)

        self.contact_layout2.addWidget(self.emaillblnfe, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout2.addWidget(self.emailedtnfe, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.sitelbl = QLabel("WebSite", self.contact_widget2)
        self.sitelbl.setFont(QFont("Arial", 10, 4))
        self.sitelbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.siteedt = QLineEdit("", self.contact_widget2)
        self.siteedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.siteedt.setFont(QFont("Arial", 12, 12))
        self.siteedt.setFixedWidth(490)

        self.contact_layout2.addWidget(self.sitelbl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout2.addWidget(self.siteedt, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.cellbl3 = QLabel("Celular 3", self.contact_widget2)
        self.cellbl3.setFont(QFont("Arial", 10, 4))
        self.cellbl3.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.celedt3 = QLineEdit("", self.contact_widget2)
        self.celedt3.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.celedt3.setFont(QFont("Arial", 12, 12))
        self.celedt3.setFixedWidth(250)

        self.contact_layout2.addWidget(self.cellbl3, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout2.addWidget(self.celedt3, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.cellbl4 = QLabel("Celular 4", self.contact_widget2)
        self.cellbl4.setFont(QFont("Arial", 10, 4))
        self.cellbl4.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.celedt4 = QLineEdit("", self.contact_widget2)
        self.celedt4.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.celedt4.setFont(QFont("Arial", 12, 12))
        self.celedt4.setFixedWidth(250)

        self.contact_layout2.addWidget(self.cellbl4, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        self.contact_layout2.addWidget(self.celedt4, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        self.addlbl = QLabel("Dados Adicionais", self.ClientsWindow)
        self.addlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; font-weight: bold; padding-top: 10px;")
        self.addlbl.setFont(QFont("Arial", 16, 12))

        self.layout.addWidget(self.addlbl)

        self.add_widget3 = QWidget(self.ClientsWindow) # widget for contact information part 2

        self.add_layout3 = QGridLayout(self.add_widget3) # with a QGridLayout layout within a VBoxLayout

        self.add_layout3.setHorizontalSpacing(16)

        self.layout.addWidget(self.add_widget3)

        self.cargalbl = QLabel("Carga Média %", self.add_widget3)
        self.cargalbl.setFont(QFont("Arial", 10, 4))
        self.cargalbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.cargaedt = QLineEdit("", self.add_widget3)
        self.cargaedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cargaedt.setFont(QFont("Arial", 12, 12))
        self.cargaedt.setFixedWidth(525)

        self.add_layout3.addWidget(self.cargalbl, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_layout3.addWidget(self.cargaedt, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.contratolbl = QLabel("Tipo de Contrato", self.add_widget3)
        self.contratolbl.setFont(QFont("Arial", 10, 4))
        self.contratolbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.contratoedt = QLineEdit("", self.add_widget3)
        self.contratoedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.contratoedt.setFont(QFont("Arial", 12, 12))
        self.contratoedt.setFixedWidth(475)

        self.add_layout3.addWidget(self.contratolbl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_layout3.addWidget(self.contratoedt, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.situationlbl = QLabel("Situação", self.add_widget3)
        self.situationlbl.setFont(QFont("Arial", 10, 4))
        self.situationlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.situation_box = QComboBox(self.add_widget3)
        self.situation_box.setStyleSheet("QComboBox {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QComboBox:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.situation_box.setFont(QFont("Arial", 12, 12))
        self.situation_box.addItems(["Ativo", "Inativo"])
        self.situation_box.setFixedWidth(220)
        self.situation_box.activated.connect(self.ActivatedPerson)
        self.situation_box.currentTextChanged.connect(self.SelectedPerson)

        self.add_layout3.addWidget(self.situationlbl, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_layout3.addWidget(self.situation_box, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.piclbl = QLabel("Foto", self.add_widget3)
        self.piclbl.setFont(QFont("Arial", 10, 4))
        self.piclbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.PicBtn = QPushButton("+ Img", self.add_widget3)
        self.PicBtn.setFont(QFont("Arial", 12, 2))
        self.PicBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.PicBtn.clicked.connect(self.Browse_Image)

        self.add_layout3.addWidget(self.piclbl, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_layout3.addWidget(self.PicBtn, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        self.piclbl2 = QLabel("", self.add_widget3)
        self.piclbl2.setFont(QFont("Arial", 10, 4))
        self.piclbl2.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px;")
        self.picpix = QPixmap("addpic.png")
        self.picpix2 = self.picpix.scaledToWidth(80)
        self.piclbl2.setPixmap(self.picpix2)

        self.add_layout3.addWidget(self.piclbl2, 1, 4, alignment=Qt.AlignmentFlag.AlignBottom)

        self.PicBtn2 = QPushButton("Zoom", self.add_widget3)
        self.PicBtn2.setFont(QFont("Arial", 12, 2))
        self.PicBtn2.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.PicBtn2.clicked.connect(self.zoom)

        self.add_layout3.addWidget(self.PicBtn2, 2, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        self.zoomedt = QLineEdit("", self)
        self.zoomedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.zoomedt.setFont(QFont("Arial", 12, 12))
        self.zoomedt.setFixedWidth(250)
        self.zoomedt.setPlaceholderText("Digite o Zoom desejado:")

        self.Vendlbl = QLabel("Vendedor", self.add_widget3)
        self.Vendlbl.setFont(QFont("Arial", 10, 4))
        self.Vendlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.VendEdt = QLineEdit("", self.add_widget3)
        self.VendEdt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.VendEdt.setFont(QFont("Arial", 12, 12))
        self.VendEdt.setFixedWidth(500)

        self.add_layout3.addWidget(self.Vendlbl, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_layout3.addWidget(self.VendEdt, 3, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.Condlbl = QLabel("Natureza da Operação Padrão", self.add_widget3)
        self.Condlbl.setFont(QFont("Arial", 10, 4))
        self.Condlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.CondEdt = QLineEdit("", self.add_widget3)
        self.CondEdt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.CondEdt.setFont(QFont("Arial", 12, 12))
        self.CondEdt.setFixedWidth(475)

        self.add_layout3.addWidget(self.Condlbl, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_layout3.addWidget(self.CondEdt, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.inscrlbl = QLabel("Inscrição Suframa", self.add_widget3)
        self.inscrlbl.setFont(QFont("Arial", 10, 4))
        self.inscrlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.InscrEdt = QLineEdit("", self.add_widget3)
        self.InscrEdt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.InscrEdt.setFont(QFont("Arial", 12, 12))
        self.InscrEdt.setFixedWidth(250)

        self.add_layout3.addWidget(self.inscrlbl, 2, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_layout3.addWidget(self.InscrEdt, 3, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.finlbl = QLabel("Financeiro", self.ClientsWindow)
        self.finlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; font-weight: bold; padding-top: 15px;")
        self.finlbl.setFont(QFont("Arial", 16, 12))

        self.layout.addWidget(self.finlbl)

        self.fin_widget = QWidget(self.ClientsWindow) # widget for contact information part 2

        self.fin_layout = QGridLayout(self.fin_widget) # with a QGridLayout layout within a VBoxLayout

        self.fin_layout.setHorizontalSpacing(16)

        self.layout.addWidget(self.fin_widget)

        self.credlbl = QLabel("Limite de Crédito", self.fin_widget)
        self.credlbl.setFont(QFont("Arial", 10, 4))
        self.credlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.CredEdt = QLineEdit("", self.fin_widget)
        self.CredEdt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.CredEdt.setFont(QFont("Arial", 12, 12))
        self.CredEdt.setFixedWidth(475)

        self.fin_layout.addWidget(self.credlbl, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.fin_layout.addWidget(self.CredEdt, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.condlbl = QLabel("Condição de Pagamento", self.fin_widget)
        self.condlbl.setFont(QFont("Arial", 10, 4))
        self.condlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.CondEdt = QLineEdit("", self.fin_widget)
        self.CondEdt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.CondEdt.setFont(QFont("Arial", 12, 12))
        self.CondEdt.setFixedWidth(475)

        self.fin_layout.addWidget(self.condlbl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.fin_layout.addWidget(self.CondEdt, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.categorylbl = QLabel("Categoria", self.fin_widget)
        self.categorylbl.setFont(QFont("Arial", 10, 4))
        self.categorylbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px;")

        self.CategoryEdt = QLineEdit("", self.fin_widget)
        self.CategoryEdt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.CategoryEdt.setFont(QFont("Arial", 12, 12))
        self.CategoryEdt.setFixedWidth(475)

        self.fin_layout.addWidget(self.categorylbl, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.fin_layout.addWidget(self.CategoryEdt, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.obslbl = QLabel("Observações", self.ClientsWindow)
        self.obslbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; font-weight: bold; padding-top: 15px;")
        self.obslbl.setFont(QFont("Arial", 16, 12))

        self.layout.addWidget(self.obslbl)

        self.final_widget_obs = QWidget(self.ClientsWindow) # widget for contact information part 2

        self.final_layout_obs = QHBoxLayout(self.final_widget_obs) # with a QHBoxLayout layout within a VBoxLayout

        self.Comment = QTextEdit("", self.final_widget_obs)
        self.Comment.setFont(QFont("Arial", 16, 8, True))
        self.Comment.setStyleSheet("color: black; background-color: white; border-radius: 7px; padding: 7px 14px; border-width: 1px; border-color: gray; border-style:solid")
        self.Comment.setFixedHeight(200)

        self.final_layout_obs.addWidget(self.Comment)

        self.layout.addWidget(self.final_widget_obs)

        ### Front-end (clients register window) widgets done, functions below:

    def IE_Check(self, int):                           # The function isCecked returns 1 or 0 that's why the int aux var value 
        if self.IEchck.isChecked():
            self.stateregedt.setText("ISENTO")
            self.stateregedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: #b5b5b5; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;}")
            self.stateregedt.setReadOnly(True)
            self.contribbox.setCurrentIndex(1)
        else:
            self.stateregedt.setText("")
            self.stateregedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
            self.stateregedt.setReadOnly(False)
            self.contribbox.setCurrentIndex(0)

    def zoom(self):
        self.fname = QFileDialog.getOpenFileName(self, "Open File", "C\\", "Image Files (*.jpg *.png)")
        self.fnamepath = self.fname[0]

        self.pic_pixmap = QPixmap(self.fnamepath)
        self.textpic, self.zoom1 = QInputDialog.getText(self, "Input Dialog", "Digite o Zoom desejado(está em 80):")
        if self.zoom1 == True:
            self.zoomedt.setText(str(self.textpic))
        self.input4 = self.zoomedt.text()
        self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(int(self.input4))
        self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
        #self.piclbl2.resize(20, 20)

    def Browse_Image(self):
        self.fname = QFileDialog.getOpenFileName(self, "Open File", "C\\", "Image Files (*.jpg *.png)")
        self.fnamepath = self.fname[0]

        self.pic_pixmap = QPixmap(self.fnamepath)
        self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(80)
        self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
        self.piclbl2.resize(20, 20)

    def ActivatedPerson(self, index):
        print(f"index na list da pessoa tipo selecionado:{index}")

    def SelectedPerson(self, s):
        print(f"selecionado pessoa tipo:{s}")
        if s == "Pessoa Física":
            self.cnpjorcpflbl.setText("CPF")
            self.cnpjedt.hide()
            self.cpfedt.show()
            self.statereglbl.setText("RG")
            self.stateregedt.hide()
            self.RGEdt.show()
            self.cityreglbl.setText("Órgão Emissor")
            self.cityregedt.hide()
            self.emissedt.show()
            self.contribbox.setCurrentIndex(2)
            self.IEchck.hide()
            self.contriblbl.setText("Contribuinte")
            self.countryedt.hide()
            self.cnpjorcpflbl.show()
            self.statereglbl.show()
            self.cityreglbl.show()
            self.contriblbl.show()
            self.contribbox.show()
            self.codelbl.show()
            self.codebox.show()
            self.statebox.show()
            self.statebox2.show()
            self.adrsearch.show()
            self.adrsearch2.show()
            self.clientlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px; padding-left: 12px;")
        elif s == "Pessoa Jurídica":
            self.cnpjorcpflbl.setText("CNPJ")
            self.cpfedt.hide()
            self.cnpjedt.show()
            self.statereglbl.setText("Inscrição Estadual")            
            self.RGEdt.hide()
            self.stateregedt.show()
            self.cityreglbl.show()
            self.cityreglbl.setText("Inscrição Municipal")
            self.emissedt.hide()
            self.cityregedt.show()
            self.IEchck.show()
            self.countryedt.hide()
            self.contriblbl.setText("Contribuinte")
            self.contribbox.show()
            self.contribbox.setCurrentIndex(0)
            self.codelbl.show()
            self.codebox.show()
            self.statebox.show()
            self.statebox2.show()
            self.adrsearch.show()
            self.adrsearch2.show()
            self.cnpjorcpflbl.show()
            self.contriblbl.show()
            self.clientlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px; padding-left: 12px;")
            self.statereglbl.show()

        elif s == "Estrangeiro":
            self.countryedt.show()
            self.cnpjorcpflbl.hide()
            self.cnpjedt.hide()
            self.cpfedt.hide()
            self.statereglbl.hide()
            self.contribbox.hide()
            self.contriblbl.setText("País")
            self.stateregedt.hide()
            self.statereglbl.hide()
            self.RGEdt.hide()
            self.cityreglbl.hide()
            self.cityregedt.hide()
            self.emissedt.hide()
            self.IEchck.hide()
            self.codelbl.hide()
            self.codebox.hide()
            self.desdeedt.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.clientlbl.setAlignment(Qt.AlignmentFlag.AlignLeft)  
            self.clientlbl.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; padding-top:15px; padding-left: 275px;")
            self.statebox.hide()
            self.statebox2.hide()
            self.foreign_state.show()
            self.foreign_state2.show()
            self.adrsearch.hide()
            self.adrsearch2.hide()

    def ActivatedCB(self, index):
        print(f"index na list do item selecionado:{index}")

    def ItemSelectedCB(self, s):
        print(f"selecionado:{s}")

    def RegSrch(self, event):
        #self.input1 = self.buscaedt.text()
        #self.input2 = self.searchby.currentText()
        #print(f"buscar:{self.input1}\npor:{self.input2}")
        #self.buscaedt.setFont(QFont("Arial", 9, 4))
        #self.buscaedt.setStyleSheet("border-radius: 7px; background-color: white; color: gray; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;")
        #self.buscaedt.setText("Selecionar método de busca e digitar:")
        print(event)
        self.cepedt1.setCursorPosition(0)
        self.cepedt2.setCursorPosition(0)

    def RegSrchOne(self, event):
        self.input1 = self.buscaedt.text()
        self.input2 = self.searchby.currentText()
        print(f"buscar:{self.input1}\npor:{self.input2}")
        self.buscaedt.setFont(QFont("Arial", 9, 4))
        self.buscaedt.setStyleSheet("border-radius: 7px; background-color: white; color: gray; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;")
        self.buscaedt.setText("Selecionar método de busca e digitar:")        

    def ClearBusca(self, event):
        self.buscaedt.clear()
        self.buscaedt.setFont(QFont("Arial", 12, 12))
        self.buscaedt.setStyleSheet("border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;")



app = QApplication(sys.argv)

SomeEnterpriseApp = MainTree()
SomeEnterpriseApp.show()
app.exec()

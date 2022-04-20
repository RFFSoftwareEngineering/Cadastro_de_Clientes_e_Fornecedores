import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtSql import *
from datetime import date
from screeninfo import get_monitors
import mysql.connector as mc
import keyring
from pycep_correios import *
from package_viacep import viacep

today = date.today()
strf_today = today.strftime("%d/%m/%Y")

for m in get_monitors():
    x_screen = m.width


class MainTree(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("xxxxxxxxxxxxx") # let's do a vertical-based layout as the main layout
        self.setStyleSheet("background-color: #e9f2f0")
        self.setWindowIcon(QIcon("xxxxxxxxxxxxx"))
        self.move(350, 50)

        self.main_layout = QGridLayout(self)  # but a grid layout for the main window
        self.setLayout(self.main_layout)

        self.Logo = QPixmap("original-logo")
        self.Logolbl = QLabel("", self)
        self.Logolbl.setPixmap(self.Logo)
        self.Logolbl.setStyleSheet("padding-left: 150px; padding-top: 50px; padding-right: 150px; padding-bottom: 325px;")


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

        service_id = 'xxxxxxxxxxxxx'
        keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')

        try:
            password_key = keyring.get_password(service_id, None)
            con = mc.connect(
                host="xxxxxxxxxxxxx",
                user="xxxxxxxxxxxxx",
                password=password_key,
                database="xxxxxxxxxxxxx"
            )
            
            query = f"""
                    CREATE TABLE IF NOT EXISTS knowhow.cadastro_clientes_fornecedores (
                    ID integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
                    Nome TEXT,
                    Fantasia TEXT,
                    TipoPessoa TEXT,
                    CNPJ TEXT,
                    CPF TEXT,
                    RegimeTributario TEXT, 
                    ClienteDesde TEXT, 
                    Contribuinte TEXT, 
                    InscricaoEstadual TEXT, 
                    InscricaoMunicipal TEXT, 
                    IEIsento TEXT, 
                    RG TEXT, 
                    OrgaoEmissor TEXT, 
                    Pais TEXT, 
                    CEP TEXT, 
                    UF TEXT, 
                    Cidade TEXT, 
                    Bairro TEXT, 
                    Endereco TEXT,
                    Numero TEXT,
                    Complemento TEXT,
                    CEP2 TEXT,
                    UF2 TEXT,
                    Cidade2 TEXT,
                    Bairro2 TEXT,
                    Endereco2 TEXT,
                    Numero2 TEXT,
                    Complemento2 TEXT,
                    Estrangeiro TEXT,
                    Estrangeiro2 TEXT,
                    ContactInfo TEXT,
                    PessoasDeContato TEXT,
                    Fone TEXT,
                    Fax TEXT,
                    Celular TEXT,
                    Celular2 TEXT,
                    Email TEXT,
                    EmailNfe TEXT,
                    WebSite TEXT,
                    Celular3 TEXT,
                    Celular4 TEXT,
                    CargaMedia TEXT,
                    TipoContrato TEXT,
                    Situacao TEXT,
                    Vendedor TEXT,
                    NaturezaOperacao TEXT,
                    InscricaoSuframa TEXT,
                    Image MEDIUMBLOB,
                    LimiteCredito TEXT,
                    CondicaoPagament TEXT,
                    Categoria TEXT,
                    Observacoes TEXT
                    );
                    """
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            cursor.close()
            con.close()            
        except mc.Error as e:
            msg = QMessageBox()
            msg.setText(f"Falha ao Conectar ao Banco de Dados:{e}")
            msg.setWindowTitle("Conexão")
            msg.exec()
            sys.exit(1)

    def CreateRegistersWindow(self):
        self.ClientsWindow = QScrollArea()  # QScrollArea as Parent of a Widget to the application works as we expect
        self.widget = QWidget(self.ClientsWindow)
        self.ClientsWindow.setGeometry(480, 200, 1300, 720)
        self.ClientsWindow.showMaximized()
        self.ClientsWindow.setWindowTitle("xxxxxxxxxxxxx - Cadastros")
        self.ClientsWindow.setStyleSheet("background-color: #e9f2f0")
        self.ClientsWindow.setWindowIcon(QIcon("xxxxxxxxxxxxx"))
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

        self.btntable = QPushButton("Mostrar/Esconder Tabela", self.search_widget)
        self.btntable.setFont(QFont("Arial", 12, 8, True))
        self.btntable.setMaximumWidth(350)
        self.btntable.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.btntable.setAutoDefault(True)
        self.btntable.clicked.connect(self.ShowHideTable)

        self.search_layout.addSpacing(30)

        self.layout.addWidget(self.search_widget)
        self.search_layout.addWidget(self.btnbusca, alignment=Qt.AlignmentFlag.AlignLeft)

        self.searchby = QComboBox(self.search_widget)
        self.searchby.setStyleSheet("border-radius: 7px; background-color: white; color: gray; padding: 7px 12px; border-width:1px; border-color: gray; border-style: solid;")
        self.searchby.addItems(["Nome", "CNPJ", "ID", "CPF"])
        self.searchby.activated.connect(self.ActivatedCB)
        self.searchby.currentTextChanged.connect(self.ItemSelectedCB)

        self.search_layout.addSpacing(-261)

        self.search_layout.addWidget(self.searchby, alignment=Qt.AlignmentFlag.AlignLeft)

        self.search_layout.addWidget(self.btntable, alignment=Qt.AlignmentFlag.AlignLeft)

        self.BtnChk = QPushButton("Usar Linha Selecionada", self.search_widget)
        self.BtnChk.setFont(QFont("Arial", 12, 8, True))
        self.BtnChk.setMaximumWidth(350)
        self.BtnChk.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.BtnChk.setAutoDefault(True)
        self.BtnChk.clicked.connect(self.retrieve_checkbox_linha)

        self.search_layout.addWidget(self.BtnChk, alignment=Qt.AlignmentFlag.AlignLeft)

        self.regdata = QLabel("Dados Cadastrais", self.ClientsWindow)
        self.regdata.setStyleSheet("color: rgb(102, 102, 102); letter-spacing: 1px; font-weight: bold; padding-top: 10px;")
        self.regdata.setFont(QFont("Arial", 16, 12))

        self.layout.addWidget(self.regdata)

        self.data_widget = QWidget(self.widget)

        self.data_layout = QGridLayout(self.data_widget)        

        self.data_widget.setLayout(self.data_layout)

        self.lblcls2 = QLabel("Nome", self.data_widget)
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
        self.cnpjedt.setInputMask("99.999.999/9999-99")
        self.cnpjedt.mousePressEvent = self.RegSrch

        self.cpfedt = QLineEdit("", self.data_widget2)
        self.cpfedt.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cpfedt.setFixedWidth(500)
        self.cpfedt.setFont(QFont("Arial", 12, 12))
        self.cpfedt.setInputMask("999.999.999-99")
        self.cpfedt.mousePressEvent = self.RegSrch
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
        self.RGEdt.setInputMask("99.999.999-9")
        self.RGEdt.mousePressEvent = self.RegSrch
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
        self.cepedt1.returnPressed.connect(self.BuscaCep1)
        self.cepedt1.mousePressEvent = self.RegSrch

        self.cepedt2 = QLineEdit("", self.charger_widget3)
        self.cepedt2.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")
        self.cepedt2.setFixedWidth(220)
        self.cepedt2.setFont(QFont("Arial", 12, 12))
        #self.cepedt2.setInputMask("99999-999")

        self.layoutadr1.addWidget(self.cepedt1, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layoutadr2.addWidget(self.cepedt2, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.adrsearch = QPushButton("", self.charger_widget1)
        self.adrsearch.setIcon(QIcon("search-icon.png"))
        self.adrsearch.setIconSize(QSize(25, 25))
        self.adrsearch.setAutoDefault(True) 
        self.adrsearch.setMaximumWidth(35)
        self.adrsearch.clicked.connect(self.BuscaCep1)
        self.cepedt1.returnPressed.connect(self.BuscaCep1)

        self.adrsearch2 = QPushButton("", self.charger_widget3)
        self.adrsearch2.setIcon(QIcon("search-icon.png"))
        self.adrsearch2.setIconSize(QSize(25, 25))
        self.adrsearch2.setAutoDefault(True)
        self.adrsearch2.setMaximumWidth(35)
        #self.adrsearch2.clicked.connect(self.BuscaCep2)
        #self.cepedt2.returnPressed.connect(self.BuscaCep2)

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
        self.foneedt.setInputMask("(99) 9999-9999")
        self.foneedt.mousePressEvent = self.RegSrch

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
        self.celedt.setInputMask("(99) 99999-9999")
        self.celedt.mousePressEvent = self.RegSrch

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
        self.fname = None
        self.fnamepath = None

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

        self.TableView = QTableWidget(self.ClientsWindow)        
        self.TableView.setGeometry(0, 400, x_screen - 20, 420)
        self.TableView.setRowCount(1)
        self.TableView.setColumnCount(53)
        columns = ["ID", "Nome", "Fantasia", "Tipo de Pessoa", "CNPJ", "CPF", "Regime Tributário", "Cliente Desde", "Contribuinte ", "Inscrição Estadual ", "Inscrição Municipal", "IE Isento", "RG", "Órgao Emissor", "País", "CEP", "UF", "Cidade", "Bairro", "Endereço", "Número", "Complemento", "CEP Cobrança", "UF Cobrança", "Cidade Cobrança", "Bairro Cobrança", "Endereço Cobrança", "Número Cobrança", "Complemento Cobrança", "UF Estrangeiro", "UF Estrangeiro Cobrança", "Informações de Contato", "Pessoas De Contato", "Fone", "Fax", "Celular", "Celular2", "E-mail", "E-mail para envio de Nfe", "WebSite", "Celular3", "Celular4", "Carga Média", "Tipo de Contrato", "Situação", "Vendedor", "Natureza da Operação", "Inscrição Suframa", "Logo", "Limite de Credito", "Condição de Pagamento", "Categoria", "Observações"]
        self.TableView.setHorizontalHeaderLabels(columns)
        self.TableView.resizeRowsToContents()
        self.TableView.resizeColumnsToContents()
        self.TableView.setStyleSheet("""
                                        QTableWidget::item {
                                        background-color: white;
                                        color: rgb(102, 102, 102);
                                        font-weight: bold;
                                        border-radius: 7px;
                                        }
                                        QTableWidget::indicator {
                                        width: 25px;
                                        height: 25px;
                                        }
                                        QTableWidget::indicator:unchecked {
                                        image: url(IEcheck-unchecked.png);
                                        }
                                        QTableWidget::indicator:checked {
                                        image: url(IEcheck-checked.png);
                                        }
                                        QTableWidget::indicator:hover {
                                        image: url(IEcheck-hover.png);
                                        }
                                        QTableWidget::indicator:checked:hover {
                                        image: url(IEcheck-checked-hover.png);
                                        }
                                        QHeaderView::section {
                                        background-color: #e9f2f0;
                                        color: rgb(102, 102, 102);
                                        font-weight: bold;
                                        border-radius: 7px;
                                        }
                                    """)
        self.TableView.setFont(QFont("Arial", 12, 6, True))        
        self.hidden = True

        self.buttons_widget = QWidget(self.ClientsWindow)

        self.buttons_layout = QHBoxLayout(self.buttons_widget) 

        self.buttons_widget.setLayout(self.buttons_layout)

        self.layout.addWidget(self.buttons_widget)        

        self.CadastrarBtn = QPushButton("Cadastrar", self.buttons_widget)
        self.CadastrarBtn.setFont(QFont("Arial", 14, 8, True))
        self.CadastrarBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.CadastrarBtn.setAutoDefault(True)
        self.CadastrarBtn.clicked.connect(self.Cadastrar)

        self.buttons_layout.addWidget(self.CadastrarBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.buttons_layout.addSpacing(-250)

        self.TodosBtn = QPushButton("Ver Todos", self.buttons_widget)
        self.TodosBtn.setFont(QFont("Arial", 14, 8, True))
        self.TodosBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.TodosBtn.clicked.connect(self.VerTodos)

        self.buttons_layout.addWidget(self.TodosBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.buttons_layout.addSpacing(-250)

        self.PrevBtn = QPushButton("<", self.buttons_widget)
        self.PrevBtn.setFont(QFont("Arial", 14, 8, True))
        self.PrevBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.PrevBtn.clicked.connect(self.Previous)

        self.buttons_layout.addWidget(self.PrevBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.buttons_layout.addSpacing(-400)

        self.ClearBtn = QPushButton("limpar", self.buttons_widget)
        self.ClearBtn.setFont(QFont("Arial", 14, 8, True))
        self.ClearBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.ClearBtn.clicked.connect(self.Clear)

        self.buttons_layout.addWidget(self.ClearBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.buttons_layout.addSpacing(-350)

        self.NextBtn = QPushButton(">", self.buttons_widget)
        self.NextBtn.setFont(QFont("Arial", 14, 8, True))
        self.NextBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.NextBtn.clicked.connect(self.Next)

        self.buttons_layout.addWidget(self.NextBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.buttons_layout.addSpacing(-350)

        self.UpdateBtn = QPushButton("Modificar", self.buttons_widget)
        self.UpdateBtn.setFont(QFont("Arial", 14, 8, True))
        self.UpdateBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.UpdateBtn.clicked.connect(self.Modify)

        self.buttons_layout.addWidget(self.UpdateBtn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.DelBtn = QPushButton("Deletar", self.buttons_widget)
        self.DelBtn.setFont(QFont("Arial", 14, 8, True))
        self.DelBtn.setStyleSheet("QPushButton {border-radius: 9px; background-color: #44a665; color :white; padding: 7px 14px;} QPushButton:hover {background-color: #5ac47e}")
        self.DelBtn.clicked.connect(self.Deletar)

        self.buttons_layout.addWidget(self.DelBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.buttons_layout.addSpacing(-350)

        self.IDdel = QLineEdit("id", self.buttons_widget)
        self.IDdel.setFont(QFont("Arial", 14, 8, True))
        self.IDdel.setMaximumWidth(50)
        self.IDdel.setStyleSheet("QLineEdit {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;} QLineEdit:hover {border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;}")

        self.buttons_layout.addWidget(self.IDdel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.buttons_layout.addSpacing(-350)

# ============================================================ Del Function ============================================================


    def Deletar(self):
        self.IDInput = self.IDdel.text()
        if not self.IDInput:
            msg = QMessageBox()
            msg.setText("Você precisa informar o ID (ao lado do botão) para deletar")
            msg.setWindowTitle("User Error")
            msg.exec()
        else:
            try:
                service_id = 'xxxxxxxxxxxxx'
                keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
                password_key = keyring.get_password(service_id, None)

                con = mc.connect(
                        host="xxxxxxxxxxxxx",
                        user="xxxxxxxxxxxxx",
                        password=password_key,
                        database="xxxxxxxxxxxxx"
                    )

                query = (f"DELETE FROM knowhow.cadastro_clientes_fornecedores WHERE ID = ({self.IDInput})")

                cursor = con.cursor()
                cursor.execute(query)
                con.commit()
                cursor.close()
                con.close()
                msg5 = QMessageBox()
                msg5.setText("Dados Deletados com Sucesso")
                msg5.setWindowTitle("msg")
                msg5.exec()

            except mc.Error as e:
                msg = QMessageBox()
                msg.setText(f"Falha ao deletar: {e}\n lembre-se de digitar o id")
                msg.setWindowTitle("Busca")
                msg.exec() 
            
            except Exception as b:
                msg = QMessageBox()
                msg.setText(f"Falha: {b}")
                msg.setWindowTitle("Fail")
                msg.exec() 


# =========================================================== Clear function ===========================================================

    def Clear(self):
        self.IDdel.setText("")
        self.nameedt.setText("")
        self.fanedt.setText("")
        self.personbox.setCurrentIndex(0)
        self.cnpjedt.setText("")
        self.cpfedt.setText("")
        self.codebox.setCurrentIndex(0)
        self.desdeedt.setText("")
        self.contribbox.setCurrentIndex(0)
        self.stateregedt.setText("")
        self.cityregedt.setText("")
        self.IEchck.setChecked(False)
        self.RGEdt.setText("")
        self.emissedt.setText("")
        self.countryedt.setText("")
        self.cepedt1.setText("")
        self.statebox.setCurrentIndex(0)
        self.cityedt.setText("")
        self.bairroedt.setText("")
        self.enderecoedt1.setText("")
        self.numeroedt.setText("")
        self.complementedt.setText("")
        self.cepedt2.setText("")
        self.statebox2.setCurrentIndex(0)
        self.cityedt2.setText("")
        self.bairroedt2.setText("")
        self.enderecoedt2.setText("")
        self.numeroedt2.setText("")
        self.complementedt2.setText("")
        self.foreign_state.setText("")
        self.foreign_state2.setText("")
        self.infoedt.setText("")
        self.pessoasedt.setText("")
        self.foneedt.setText("")
        self.faxedt.setText("")
        self.celedt.setText("")
        self.celedt2.setText("")
        self.emailedt.setText("")
        self.emailedtnfe.setText("")
        self.siteedt.setText("")
        self.celedt3.setText("")
        self.celedt4.setText("")
        self.cargaedt.setText("")
        self.contratoedt.setText("")
        self.situation_box.setCurrentIndex(0)
        self.VendEdt.setText("")
        self.CondEdt.setText("")
        self.InscrEdt.setText("")
        self.piclbl2.setPixmap(self.picpix2)
        self.CredEdt.setText("")
        self.CondEdt.setText("")
        self.CategoryEdt.setText("")
        self.Comment.setText("")

# =========================================================== Previous and Next ========================================================
   
    def Next(self):
        self.IDInput = self.IDdel.text()
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )

            query = f"SELECT * FROM knowhow.cadastro_clientes_fornecedores WHERE ID = (SELECT max(ID) FROM knowhow.cadastro_clientes_fornecedores WHERE ID > {self.IDInput})"

            cursor = con.cursor()
            cursor.execute(query)
            result = cursor

            for row_number, row_data in enumerate(result):
                for column_number , data in enumerate(row_data):

                    self.IDdel.setText(str(row_data[0]))
                    self.nameedt.setText(str(row_data[1]))
                    self.fanedt.setText(str(row_data[2]))
                    self.personbox.setCurrentText(str(row_data[3]))
                    self.cnpjedt.setText(str(row_data[4]))
                    self.cpfedt.setText(str(row_data[5]))
                    self.codebox.setCurrentText(str(row_data[6]))
                    self.desdeedt.setText(str(row_data[7]))
                    self.contribbox.setCurrentText(str(row_data[8]))
                    self.stateregedt.setText(str(row_data[9]))
                    self.cityregedt.setText(str(row_data[10]))
                    if str(row_data[11]) == "Sim":
                        self.IEchck.setChecked(True)
                    else:
                        self.IEchck.setChecked(False)
                    self.RGEdt.setText(str(row_data[12]))
                    self.emissedt.setText(str(row_data[13]))
                    self.countryedt.setText(str(row_data[14]))
                    self.cepedt1.setText(str(row_data[15]))
                    self.statebox.setCurrentText(str(row_data[16]))
                    self.cityedt.setText(str(row_data[17]))
                    self.bairroedt.setText(str(row_data[18]))
                    self.enderecoedt1.setText(str(row_data[19]))
                    self.numeroedt.setText(str(row_data[20]))
                    self.complementedt.setText(str(row_data[21]))
                    self.cepedt2.setText(str(row_data[22]))
                    self.statebox2.setCurrentText(str(row_data[23]))
                    self.cityedt2.setText(str(row_data[24]))
                    self.bairroedt2.setText(str(row_data[25]))
                    self.enderecoedt2.setText(str(row_data[26]))
                    self.numeroedt2.setText(str(row_data[27]))
                    self.complementedt2.setText(str(row_data[28]))
                    self.foreign_state.setText(str(row_data[29]))
                    self.foreign_state2.setText(str(row_data[30]))
                    self.infoedt.setText(str(row_data[31]))
                    self.pessoasedt.setText(str(row_data[32]))
                    self.foneedt.setText(str(row_data[33]))
                    self.faxedt.setText(str(row_data[34]))
                    self.celedt.setText(str(row_data[35]))
                    self.celedt2.setText(str(row_data[36]))
                    self.emailedt.setText(str(row_data[37]))
                    self.emailedtnfe.setText(str(row_data[38]))
                    self.siteedt.setText(str(row_data[39]))
                    self.celedt3.setText(str(row_data[40]))
                    self.celedt4.setText(str(row_data[41]))
                    self.cargaedt.setText(str(row_data[42]))
                    self.contratoedt.setText(str(row_data[43]))
                    self.situation_box.setCurrentText(str(row_data[44]))
                    self.VendEdt.setText(str(row_data[45]))
                    self.CondEdt.setText(str(row_data[46]))
                    self.InscrEdt.setText(str(row_data[47]))
                    """
                    a lógica aqui é o seguinte: pegar o caminho descrito no db
                    tratá-lo e passá-lo como argumento do pixmap
                    fazendo asism, aparecer o pixmap no label no local correto para cada registro
                    """
                    self.teste = row_data[48]
                    self.y = str(self.teste)
                    self.z = self.y.split("b")
                    imagem = ""
                    imagem = str(self.z[1]) # tratamento caminho da imagem
                    imagem = imagem.split("b") # forma uma lista
                    imagex = ""
                    imagex = imagem[0]
                    imagex = imagex.replace("'", "") # caminho tratado
                    if str(row_data[48]) != "None":
                        self.pic_pixmap = QPixmap(imagex) # exibir imagem a parir do path tratado
                        self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(80) # fixa tamanho imagem para 80 pixel
                        self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
                        self.piclbl2.resize(20, 20)
                        print("1442 Entrou na funcao exibir imagem")
            
                    else:
                        print("none img")
                    self.CredEdt.setText(str(row_data[49]))
                    self.CondEdt.setText(str(row_data[50]))
                    self.CategoryEdt.setText(str(row_data[51]))
                    self.Comment.setText(str(row_data[52]))

        except:
            msg = QMessageBox()
            msg.setText("você está tentando acessar um registro inexistente")
            msg.setWindowTitle("Fail")
            msg.exec()
            print("você está tentando acessar um registro inexistente")
            pass

    def Previous(self):
        self.IDInput = self.IDdel.text()
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )

            query = f"SELECT * FROM knowhow.cadastro_clientes_fornecedores WHERE ID = (SELECT max(ID) FROM knowhow.cadastro_clientes_fornecedores WHERE ID < {self.IDInput})"

            cursor = con.cursor()
            cursor.execute(query)
            result = cursor

            for row_number, row_data in enumerate(result):
                for column_number , data in enumerate(row_data):

                    self.IDdel.setText(str(row_data[0]))
                    self.nameedt.setText(str(row_data[1]))
                    self.fanedt.setText(str(row_data[2]))
                    self.personbox.setCurrentText(str(row_data[3]))
                    self.cnpjedt.setText(str(row_data[4]))
                    self.cpfedt.setText(str(row_data[5]))
                    self.codebox.setCurrentText(str(row_data[6]))
                    self.desdeedt.setText(str(row_data[7]))
                    self.contribbox.setCurrentText(str(row_data[8]))
                    self.stateregedt.setText(str(row_data[9]))
                    self.cityregedt.setText(str(row_data[10]))
                    if str(row_data[11]) == "Sim":
                        self.IEchck.setChecked(True)
                    else:
                        self.IEchck.setChecked(False)
                    self.RGEdt.setText(str(row_data[12]))
                    self.emissedt.setText(str(row_data[13]))
                    self.countryedt.setText(str(row_data[14]))
                    self.cepedt1.setText(str(row_data[15]))
                    self.statebox.setCurrentText(str(row_data[16]))
                    self.cityedt.setText(str(row_data[17]))
                    self.bairroedt.setText(str(row_data[18]))
                    self.enderecoedt1.setText(str(row_data[19]))
                    self.numeroedt.setText(str(row_data[20]))
                    self.complementedt.setText(str(row_data[21]))
                    self.cepedt2.setText(str(row_data[22]))
                    self.statebox2.setCurrentText(str(row_data[23]))
                    self.cityedt2.setText(str(row_data[24]))
                    self.bairroedt2.setText(str(row_data[25]))
                    self.enderecoedt2.setText(str(row_data[26]))
                    self.numeroedt2.setText(str(row_data[27]))
                    self.complementedt2.setText(str(row_data[28]))
                    self.foreign_state.setText(str(row_data[29]))
                    self.foreign_state2.setText(str(row_data[30]))
                    self.infoedt.setText(str(row_data[31]))
                    self.pessoasedt.setText(str(row_data[32]))
                    self.foneedt.setText(str(row_data[33]))
                    self.faxedt.setText(str(row_data[34]))
                    self.celedt.setText(str(row_data[35]))
                    self.celedt2.setText(str(row_data[36]))
                    self.emailedt.setText(str(row_data[37]))
                    self.emailedtnfe.setText(str(row_data[38]))
                    self.siteedt.setText(str(row_data[39]))
                    self.celedt3.setText(str(row_data[40]))
                    self.celedt4.setText(str(row_data[41]))
                    self.cargaedt.setText(str(row_data[42]))
                    self.contratoedt.setText(str(row_data[43]))
                    self.situation_box.setCurrentText(str(row_data[44]))
                    self.VendEdt.setText(str(row_data[45]))
                    self.CondEdt.setText(str(row_data[46]))
                    self.InscrEdt.setText(str(row_data[47]))
                    """
                    a lógica aqui é o seguinte: pegar o caminho descrito no db
                    tratá-lo e passá-lo como argumento do pixmap
                    fazendo asism, aparecer o pixmap no label no local correto para cada registro
                    """
                    self.teste = row_data[48]
                    self.y = str(self.teste)
                    self.z = self.y.split("b")
                    imagem = ""
                    imagem = str(self.z[1]) # tratamento caminho da imagem
                    imagem = imagem.split("b") # forma uma lista
                    imagex = ""
                    imagex = imagem[0]
                    imagex = imagex.replace("'", "") # caminho tratado
                    if str(row_data[48]) != "None":
                        self.pic_pixmap = QPixmap(imagex) # exibir imagem a parir do path tratado
                        self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(80) # fixa tamanho imagem para 80 pixel
                        self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
                        self.piclbl2.resize(20, 20)
                        print("1442 Entrou na funcao exibir imagem")
            
                    else:
                        print("none img")
                    self.CredEdt.setText(str(row_data[49]))
                    self.CondEdt.setText(str(row_data[50]))
                    self.CategoryEdt.setText(str(row_data[51]))
                    self.Comment.setText(str(row_data[52]))

        except:
            msg = QMessageBox()
            msg.setText("você está tentando acessar um registro inexistente")
            msg.setWindowTitle("Fail")
            msg.exec()
            print("você está tentando acessar um registro inexistente")
            pass

     
# =========================================================== Modify (Update) ==============================================================


    def Modify(self):
        self.IDInput = self.IDdel.text()
        self.NomeInput = self.nameedt.text()
        self.FantasyInput = self.fanedt.text()
        self.KindInput = str(self.personbox.currentText())
        self.CNPJInput = self.cnpjedt.text()
        self.CPFInput = self.cpfedt.text()
        self.RegimeInput = str(self.codebox.currentText())
        self.SinceInput = self.desdeedt.text()
        self.ContribInput = str(self.contribbox.currentText())
        self.IEInput = self.stateregedt.text()
        self.IMInput = self.cityregedt.text()
        if self.IEchck.isChecked():
            self.IEChkInput = "Sim"
        else:
            self.IEChkInput = "Não"
        self.RGInput = self.RGEdt.text()
        self.OrgaoInput = self.emissedt.text()
        self.CountryInput = self.countryedt.text()
        self.CEPInput = self.cepedt1.text()
        self.UFInput = str(self.statebox.currentText())
        self.CityInput = self.cityedt.text()
        self.HoodInput = self.bairroedt.text()
        self.StreetInput = self.enderecoedt1.text()
        self.NumInput = self.numeroedt.text()
        self.ComplInput = self.complementedt.text()
        self.CEPInput2 = self.cepedt2.text()
        self.UFInput2 = str(self.statebox2.currentText())
        self.CityInput2 = self.cityedt2.text()
        self.HoodInput2 = self.bairroedt2.text()
        self.StreetInput2 = self.enderecoedt2.text()
        self.NumInput2 = self.numeroedt2.text()
        self.ComplInput2 = self.complementedt2.text()
        self.EstrangeiroInput = self.foreign_state.text()
        self.EstrangeiroInput2 = self.foreign_state2.text()
        self.ContactInfoInput = self.infoedt.text()
        self.PeopleInput = self.pessoasedt.text()
        self.FoneInput = self.foneedt.text()
        self.FAXInput = self.faxedt.text()
        self.Cel1Input = self.celedt.text()
        self.Cel2Input = self.celedt2.text()
        self.EmailInput = self.emailedt.text()
        self.NFeInput = self.emailedtnfe.text()
        self.SiteInput = self.siteedt.text()
        self.Cel3Input = self.celedt3.text()
        self.Cel4Input = self.celedt4.text()
        self.CargaInput = self.cargaedt.text()
        self.ContrTypeInput = self.contratoedt.text()
        self.SituacaoInput = str(self.situation_box.currentText())
        self.SellerInput = self.VendEdt.text()
        self.CondInput = self.CondEdt.text()
        self.SuframaInput = self.InscrEdt.text()
        try:
            self.teste = row_data[48]
            self.y = str(self.teste)
            self.z = self.y.split("b")
            imagem = ""
            imagem = str(self.z[1]) # tratamento caminho da imagem
            imagem = imagem.split("b") # forma uma lista
            imagex = ""
            imagex = imagem[0]
            imagex = imagex.replace("'", "") # caminho tratado
            if str(row_data[48]) != "None":
                self.pic_pixmap = QPixmap(imagex) # exibir imagem a parir do path tratado
                self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(80) # fixa tamanho imagem para 80 pixel
                self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
                self.piclbl2.resize(20, 20)
                print("1442 Entrou na funcao exibir imagem")
            
            else:
                print("none img")
                try:
                    self.ImgInput = None
                except:
                    self.ImgInput = "None"
        except:
            try:
                self.ImgInput = None
            except:
                self.ImgInput = "None"
        
        self.LimitInput = self.CredEdt.text()
        self.CondInput = self.CondEdt.text()
        self.CategoryInput = self.CategoryEdt.text()
        self.OBSInput = self.Comment.toPlainText()
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="1xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )

            query = f"""UPDATE knowhow.cadastro_clientes_fornecedores
            SET
                Nome = '{self.NomeInput}',
                Fantasia = '{self.FantasyInput}',
                TipoPessoa = '{self.KindInput}',
                CNPJ = '{self.CNPJInput}',
                CPF = '{self.CPFInput}',
                RegimeTributario = '{self.RegimeInput}',
                ClienteDesde = '{self.SinceInput}',
                Contribuinte = '{self.ContribInput}',
                InscricaoEstadual = '{self.IEInput}',
                InscricaoMunicipal = '{self.IMInput}',
                IEIsento = '{self.IEChkInput}',
                RG = '{self.RGInput}',
                OrgaoEmissor = '{self.OrgaoInput}', 
                Pais = '{self.CountryInput}', 
                CEP = '{self.CEPInput}', 
                UF = '{self.UFInput}', 
                Cidade = '{self.CityInput}', 
                Bairro = '{self.HoodInput}', 
                Endereco = '{self.StreetInput}',
                Numero = '{self.NumInput}',
                Complemento = '{self.ComplInput}',
                CEP2 = '{self.CEPInput2}',
                UF2 = '{self.UFInput2}',
                Cidade2 = '{self.CityInput2}',
                Bairro2 = '{self.HoodInput2}',
                Endereco2 = '{self.StreetInput2}',
                Numero2 = '{self.NumInput2}',
                Complemento2 = '{self.ComplInput2}',
                Estrangeiro = '{self.EstrangeiroInput}',
                Estrangeiro2 = '{self.EstrangeiroInput2}',
                ContactInfo = '{self.ContactInfoInput}',
                PessoasDeContato = '{self.PeopleInput}',
                Fone = '{self.FoneInput}',
                Fax = '{self.FAXInput}',
                Celular = '{self.Cel1Input}',
                Celular2 = '{self.Cel2Input}',
                Email = '{self.EmailInput}',
                EmailNfe = '{self.NFeInput}',
                WebSite = '{self.SiteInput}',
                Celular3 = '{self.Cel3Input}',
                Celular4 = '{self.Cel4Input}',
                CargaMedia = '{self.CargaInput}',
                TipoContrato = '{self.ContrTypeInput}',
                Situacao = '{self.SituacaoInput}',
                Vendedor = '{self.SellerInput}',
                NaturezaOperacao = '{self.CondInput}',
                InscricaoSuframa = '{self.SuframaInput}',
                Image = '{self.ImgInput}',
                LimiteCredito = '{self.LimitInput}',
                CondicaoPagament = '{self.CondInput}',
                Categoria = '{self.CategoryInput}',
                Observacoes = '{self.OBSInput}'
            WHERE
                ID = '{self.IDInput}';
            """

            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            cursor.close()
            con.close()
            msg = QMessageBox()
            msg.setText("Atualizado com Sucesso")
            msg.setWindowTitle("Modify/Update")
            msg.exec()


        except Exception as e:
            msg = QMessageBox()
            msg.setText(f"exceção: {e}")
            msg.setWindowTitle("Modify")
            msg.exec()


#==================================================== Ver Todos ========================================================================
    def VerTodos(self):
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )

            query = "SELECT * FROM knowhow.cadastro_clientes_fornecedores"
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            self.TableView.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.TableView.insertRow(row_number)
                for column_number , data in enumerate(row_data):
                    if column_number == 0:
                        self.item = QTableWidgetItem(f"{row_data[0]}") # ID together with checkbox
                        self.item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                        self.item.setCheckState(Qt.CheckState.Unchecked)
                        self.TableView.setItem(row_number, column_number, self.item)                     
                    else:
                        self.TableView.setItem(row_number, column_number, QTableWidgetItem(str(data)))                    
            

            
        except mc.Error as e:
            msg = QMessageBox()
            msg.setText(f"Falha ao buscar: {e}")
            msg.setWindowTitle("Busca")
            msg.exec()

        except Exception as b:
            msg = QMessageBox()
            msg.setText(f"Falha: {b}")
            msg.setWindowTitle("Fail")
            msg.exec()

        self.TableView.resizeRowsToContents()
        self.TableView.resizeColumnsToContents()
        self.TableView.setColumnWidth(0, 70)
        self.TableView.show()

        print(str(row_data))
        self.IDdel.setText(str(row_data[0]))
        self.nameedt.setText(str(row_data[1]))
        self.fanedt.setText(str(row_data[2]))
        self.personbox.setCurrentText(str(row_data[3]))
        self.cnpjedt.setText(str(row_data[4]))
        self.cpfedt.setText(str(row_data[5]))
        self.codebox.setCurrentText(str(row_data[6]))
        self.desdeedt.setText(str(row_data[7]))
        self.contribbox.setCurrentText(str(row_data[8]))
        self.stateregedt.setText(str(row_data[9]))
        self.cityregedt.setText(str(row_data[10]))
        if str(row_data[11]) == "Sim":
            self.IEchck.setChecked(True)
        else:
            self.IEchck.setChecked(False)
        self.RGEdt.setText(str(row_data[12]))
        self.emissedt.setText(str(row_data[13]))
        self.countryedt.setText(str(row_data[14]))
        self.cepedt1.setText(str(row_data[15]))
        self.statebox.setCurrentText(str(row_data[16]))
        self.cityedt.setText(str(row_data[17]))
        self.bairroedt.setText(str(row_data[18]))
        self.enderecoedt1.setText(str(row_data[19]))
        self.numeroedt.setText(str(row_data[20]))
        self.complementedt.setText(str(row_data[21]))
        self.cepedt2.setText(str(row_data[22]))
        self.statebox2.setCurrentText(str(row_data[23]))
        self.cityedt2.setText(str(row_data[24]))
        self.bairroedt2.setText(str(row_data[25]))
        self.enderecoedt2.setText(str(row_data[26]))
        self.numeroedt2.setText(str(row_data[27]))
        self.complementedt2.setText(str(row_data[28]))
        self.foreign_state.setText(str(row_data[29]))
        self.foreign_state2.setText(str(row_data[30]))
        self.infoedt.setText(str(row_data[31]))
        self.pessoasedt.setText(str(row_data[32]))
        self.foneedt.setText(str(row_data[33]))
        self.faxedt.setText(str(row_data[34]))
        self.celedt.setText(str(row_data[35]))
        self.celedt2.setText(str(row_data[36]))
        self.emailedt.setText(str(row_data[37]))
        self.emailedtnfe.setText(str(row_data[38]))
        self.siteedt.setText(str(row_data[39]))
        self.celedt3.setText(str(row_data[40]))
        self.celedt4.setText(str(row_data[41]))
        self.cargaedt.setText(str(row_data[42]))
        self.contratoedt.setText(str(row_data[43]))
        self.situation_box.setCurrentText(str(row_data[44]))
        self.VendEdt.setText(str(row_data[45]))
        self.CondEdt.setText(str(row_data[46]))
        self.InscrEdt.setText(str(row_data[47]))
        """
        a lógica aqui é o seguinte: pegar o caminho descrito no db
        tratá-lo e passá-lo como argumento do pixmap
        fazendo asism, aparecer o pixmap no label no local correto para cada registro
        """
        self.teste = row_data[48]
        self.y = str(self.teste)
        self.z = self.y.split("b")
        imagem = ""
        imagem = str(self.z[1]) # tratamento caminho da imagem
        imagem = imagem.split("b") # forma uma lista
        imagex = ""
        imagex = imagem[0]
        imagex = imagex.replace("'", "") # caminho tratado
        if str(row_data[48]) != "None":
            self.pic_pixmap = QPixmap(imagex) # exibir imagem a parir do path tratado
            self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(80) # fixa tamanho imagem para 80 pixel
            self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
            self.piclbl2.resize(20, 20)
            print("1442 Entrou na funcao exibir imagem")
            
        else:
            print("none img")
        self.CredEdt.setText(str(row_data[49]))
        self.CondEdt.setText(str(row_data[50]))
        self.CategoryEdt.setText(str(row_data[51]))
        self.Comment.setText(str(row_data[52]))


#=========================================================== Buscar Imagem Pasta ===============================================================
    def Browse_Image(self):
        self.fname = QFileDialog.getOpenFileName(self, "Open File", "C\\", "Image Files (*.jpg *.png)")
        self.fnamepath = self.fname[0]
        print(self.fnamepath)

        self.pic_pixmap = QPixmap(self.fnamepath)
        self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(80)
        self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
        self.piclbl2.resize(20, 20)

#=========================================================== Cadastro de clientes e fornecedores ================================================

    def Cadastrar(self):
        self.NomeInput = self.nameedt.text()
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )
            query = f"SELECT Nome FROM knowhow.cadastro_clientes_fornecedores WHERE Nome='{self.NomeInput}'"
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            if self.NomeInput == "":
                pass
            elif self.NomeInput == (str(result[0][0])):
                print("já existe")
                msg = QMessageBox()
                msg.setText("Já existe um nome com esse valor!")
                msg.setWindowTitle("Duplicity Verifier")
                msg.exec()
                return
            con.close()

        except Exception as e:
            msg = QMessageBox()
            msg.setText(f"Pode proceder, esse valor de nome não existe")
            msg.setWindowTitle("Duplicity Verifier")
            msg.exec()
            print(e)
        
        self.CNPJInput  = self.cnpjedt.text()
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )
            query = f"SELECT CNPJ FROM knowhow.cadastro_clientes_fornecedores WHERE CNPJ='{self.CNPJInput}'"
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            if self.CNPJInput == "../-":
                pass
            elif self.CNPJInput == "":
                pass
            elif self.CNPJInput == (str(result[0][0])):
                print("já existe")
                msg = QMessageBox()
                msg.setText("Já existe um CNPJ com esse valor!")
                msg.setWindowTitle("Duplicity Verifier")
                msg.exec()
                return
            con.close()

        except Exception as e:
            msg = QMessageBox()
            msg.setText(f"Pode proceder, esse valor de cnpj não existe")
            msg.setWindowTitle("Duplicity Verifier")
            msg.exec()
            print(e)

        self.CPFInput = self.cpfedt.text()
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )
            query = f"SELECT CPF FROM knowhow.cadastro_clientes_fornecedores WHERE CPF='{self.CPFInput}'"
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            if self.CPFInput == "":
                pass
            elif self.CPFInput == "..-":
                pass
            elif self.CPFInput == (str(result[0][0])):
                print("já existe")
                msg = QMessageBox()
                msg.setText("Já existe um CPF com esse valor!")
                msg.setWindowTitle("Duplicity Verifier")
                msg.exec()
                return
            con.close()

        except Exception as e:
            msg = QMessageBox()
            msg.setText(f"Pode proceder, esse valor de CPF não existe")
            msg.setWindowTitle("Duplicity Verifier")
            msg.exec()
            print(e)

        self.NomeInput = self.nameedt.text()
        self.FantasyInput = self.fanedt.text()
        self.KindInput = str(self.personbox.currentText())
        self.CNPJInput = self.cnpjedt.text()
        self.CPFInput = self.cpfedt.text()
        self.RegimeInput = str(self.codebox.currentText())
        self.SinceInput = self.desdeedt.text()
        self.ContribInput = str(self.contribbox.currentText())
        self.IEInput = self.stateregedt.text()
        self.IMInput = self.cityregedt.text()
        if self.IEchck.isChecked():
            self.IEChkInput = "Sim"
        else:
            self.IEChkInput = "Não"
        self.RGInput = self.RGEdt.text()
        self.OrgaoInput = self.emissedt.text()
        self.CountryInput = self.countryedt.text()
        self.CEPInput = self.cepedt1.text()
        self.UFInput = str(self.statebox.currentText())
        self.CityInput = self.cityedt.text()
        self.HoodInput = self.bairroedt.text()
        self.StreetInput = self.enderecoedt1.text()
        self.NumInput = self.numeroedt.text()
        self.ComplInput = self.complementedt.text()
        self.CEPInput2 = self.cepedt2.text()
        self.UFInput2 = str(self.statebox2.currentText())
        self.CityInput2 = self.cityedt2.text()
        self.HoodInput2 = self.bairroedt2.text()
        self.StreetInput2 = self.enderecoedt2.text()
        self.NumInput2 = self.numeroedt2.text()
        self.ComplInput2 = self.complementedt2.text()
        self.EstrangeiroInput = self.foreign_state.text()
        self.EstrangeiroInput2 = self.foreign_state2.text()
        self.ContactInfoInput = self.infoedt.text()
        self.PeopleInput = self.pessoasedt.text()
        self.FoneInput = self.foneedt.text()
        self.FAXInput = self.faxedt.text()
        self.Cel1Input = self.celedt.text()
        self.Cel2Input = self.celedt2.text()
        self.EmailInput = self.emailedt.text()
        self.NFeInput = self.emailedtnfe.text()
        self.SiteInput = self.siteedt.text()
        self.Cel3Input = self.celedt3.text()
        self.Cel4Input = self.celedt4.text()
        self.CargaInput = self.cargaedt.text()
        self.ContrTypeInput = self.contratoedt.text()
        self.SituacaoInput = str(self.situation_box.currentText())
        self.SellerInput = self.VendEdt.text()
        self.CondInput = self.CondEdt.text()
        self.SuframaInput = self.InscrEdt.text()
        self.ImgInput = self.fnamepath
        self.LimitInput = self.CredEdt.text()
        self.CondInput = self.CondEdt.text()
        self.CategoryInput = self.CategoryEdt.text()
        self.OBSInput = self.Comment.toPlainText()
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )
            query = f"""
                    INSERT INTO knowhow.cadastro_clientes_fornecedores (
                    Nome, Fantasia, TipoPessoa, CNPJ, CPF, 
                    RegimeTributario, ClienteDesde, Contribuinte, InscricaoEstadual, InscricaoMunicipal,
                    IEIsento, RG, OrgaoEmissor, Pais, CEP,
                    UF, Cidade, Bairro, Endereco, Numero,
                    Complemento, CEP2, UF2, Cidade2, Bairro2,
                    Endereco2, Numero2, Complemento2, Estrangeiro, Estrangeiro2,
                    ContactInfo, PessoasDeContato, Fone, Fax, Celular,
                    Celular2, Email, EmailNfe, WebSite, Celular3,
                    Celular4, CargaMedia, TipoContrato, Situacao, Vendedor,
                    NaturezaOperacao, InscricaoSuframa, Image, LimiteCredito, CondicaoPagament,
                    Categoria, Observacoes
                    ) VALUES (
                    '{self.NomeInput}', '{self.FantasyInput}', '{self.KindInput}', '{self.CNPJInput}', '{self.CPFInput}', 
                    '{self.RegimeInput}', '{self.SinceInput}', '{self.ContribInput}', '{self.IEInput}', '{self.IMInput}',
                    '{self.IEChkInput}', '{self.RGInput}', '{self.OrgaoInput}', '{self.CountryInput}', '{self.CEPInput}',
                    '{self.UFInput}', '{self.CityInput}', '{self.HoodInput}', '{self.StreetInput}', '{self.NumInput}',
                    '{self.ComplInput}', '{self.CEPInput2}', '{self.UFInput2}', '{self.CityInput2}', '{self.HoodInput2}',
                    '{self.StreetInput2}', '{self.NumInput2}', '{self.ComplInput2}', '{self.EstrangeiroInput}', '{self.EstrangeiroInput2}',
                    '{self.ContactInfoInput}', '{self.PeopleInput}', '{self.FoneInput}', '{self.FAXInput}', '{self.Cel1Input}',
                    '{self.Cel2Input}', '{self.EmailInput}', '{self.NFeInput}', '{self.SiteInput}', '{self.Cel3Input}',
                    '{self.Cel4Input}', '{self.CargaInput}', '{self.ContrTypeInput}', '{self.SituacaoInput}', '{self.SellerInput}',
                    '{self.CondInput}', '{self.SuframaInput}','{self.ImgInput}', '{self.LimitInput}', '{self.CondInput}',
                    '{self.CategoryInput}', '{self.OBSInput}'
                    );
                """

            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            cursor.close()
            con.close()
            msg = QMessageBox()
            msg.setText("Cadastrado com sucesso!")
            msg.setWindowTitle("Cadastro")
            msg.exec()

        except mc.Error as e:
            msg = QMessageBox()
            msg.setText(f"Falha ao cadatrar: {e}")
            msg.setWindowTitle("Cadastro")
            msg.exec()

        except Exception as b:
            print(b)
            msg = QMessageBox()
            msg.setText(f"Falha: {b}\nErro de Usuário")
            msg.setWindowTitle("Fail")
            msg.exec()

#============================================================ Busca por CEP ==================================================================

    def BuscaCep1(self):
        self.CEPInput1 = self.cepedt1.text()
        print(self.CEPInput1)

        data = {}

        try:


            instance = viacep.ViaCep()

            data = instance.GetData(self.CEPInput1)

            bairro = data.get("bairro")
            cidade = data.get("localidade")
            rua = data.get("logradouro")
            estado = data.get("uf")
            complemento = data.get("complemento")

            self.enderecoedt1.setText(rua)
            self.bairroedt.setText(bairro)
            self.cityedt.setText(cidade)
            self.complementedt.setText(complemento)
            self.index = self.statebox.findText(estado)
            if self.index >= 0:
                self.statebox.setCurrentIndex(self.index)

        except Exception as n:
            print(n)
            msg = QMessageBox()
            msg.setText("API Fora do Ar\nTente novamente mais tarde")
            msg.setWindowTitle("Fail")
            msg.exec()
            pass


#===================================================== Uso dos checkboxes =============================================================


    def retrieve_checkbox_linha(self):
        for row_number in range(self.TableView.rowCount()):
            try:
                if self.TableView.item(row_number, 0).checkState() == Qt.CheckState.Checked:
                    dados = ([self.TableView.item(row_number, column_number).text() for column_number in range(self.TableView.columnCount())])
                    print(dados)
                    self.IDdel.setText(str(dados[0]))
                    self.nameedt.setText(str(dados[1]))
                    self.fanedt.setText(str(dados[2]))
                    self.personbox.setCurrentText(str(dados[3]))
                    self.cnpjedt.setText(str(dados[4]))
                    self.cpfedt.setText(str(dados[5]))
                    self.codebox.setCurrentText(str(dados[6]))
                    self.desdeedt.setText(str(dados[7]))
                    self.contribbox.setCurrentText(str(dados[8]))
                    self.stateregedt.setText(str(dados[9]))
                    self.cityregedt.setText(str(dados[10]))
                    if str(dados[11]) == "Sim":
                        self.IEchck.setChecked(True)
                    else:
                        self.IEchck.setChecked(False)
                    self.RGEdt.setText(str(dados[12]))
                    self.emissedt.setText(str(dados[13]))
                    self.countryedt.setText(str(dados[14]))
                    self.cepedt1.setText(str(dados[15]))
                    self.statebox.setCurrentText(str(dados[16]))
                    self.cityedt.setText(str(dados[17]))
                    self.bairroedt.setText(str(dados[18]))
                    self.enderecoedt1.setText(str(dados[19]))
                    self.numeroedt.setText(str(dados[20]))
                    self.complementedt.setText(str(dados[21]))
                    self.cepedt2.setText(str(dados[22]))
                    self.statebox2.setCurrentText(str(dados[23]))
                    self.cityedt2.setText(str(dados[24]))
                    self.bairroedt2.setText(str(dados[25]))
                    self.enderecoedt2.setText(str(dados[26]))
                    self.numeroedt2.setText(str(dados[27]))
                    self.complementedt2.setText(str(dados[28]))
                    self.foreign_state.setText(str(dados[29]))
                    self.foreign_state2.setText(str(dados[30]))
                    self.infoedt.setText(str(dados[31]))
                    self.pessoasedt.setText(str(dados[32]))
                    self.foneedt.setText(str(dados[33]))
                    self.faxedt.setText(str(dados[34]))
                    self.celedt.setText(str(dados[35]))
                    self.celedt2.setText(str(dados[36]))
                    self.emailedt.setText(str(dados[37]))
                    self.emailedtnfe.setText(str(dados[38]))
                    self.siteedt.setText(str(dados[39]))
                    self.celedt3.setText(str(dados[40]))
                    self.celedt4.setText(str(dados[41]))
                    self.cargaedt.setText(str(dados[42]))
                    self.contratoedt.setText(str(dados[43]))
                    self.situation_box.setCurrentText(str(dados[44]))
                    self.VendEdt.setText(str(dados[45]))
                    self.CondEdt.setText(str(dados[46]))
                    self.InscrEdt.setText(str(dados[47]))
                    """
                    a lógica aqui é o seguinte: pegar o caminho descrito no db
                    tratá-lo e passá-lo como argumento do pixmap
                    fazendo asism, aparecer o pixmap no label no local correto para cada registro
                    """
                    self.teste = dados[48]
                    self.y = str(self.teste)
                    self.z = self.y.split("b")
                    imagem = ""
                    imagem = str(self.z[1]) # tratamento caminho da imagem
                    imagem = imagem.split("b") # forma uma lista
                    imagex = ""
                    imagex = imagem[0]
                    imagex = imagex.replace("'", "") # caminho tratado
                    if str(dados[48]) != "None":
                        self.pic_pixmap = QPixmap(imagex) # exibir imagem a parir do path tratado
                        self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(80) # fixa tamanho imagem para 80 pixel
                        self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
                        self.piclbl2.resize(20, 20)
                        print("1883 Entrou na funcao exibir imagem")
                    else:
                        print("none img")
                    self.CredEdt.setText(str(dados[49]))
                    self.CondEdt.setText(str(dados[50]))
                    self.CategoryEdt.setText(str(dados[51]))
                    self.Comment.setText(str(dados[52]))
                    print("FOI SELECIONADO")
                    self.TableView.hide()
                    self.hidden = True
                else:
                    print("FOI PRETERIDO(DES-SELECIONADO)")
            except:
                msg = QMessageBox()
                msg.setText("Selecione Algo na Tabela")
                msg.setWindowTitle("Fail")
                msg.exec()
                pass

#=================================================== Front-end functions ===============================================================

    def IE_Check(self, int):                           # The function isChecked returns 1 or 0 that's why the int parameter var value 
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
        self.cnpjedt.setCursorPosition(0)
        self.cpfedt.setCursorPosition(0)
        self.foneedt.setCursorPosition(0)
        self.celedt.setCursorPosition(0)

#======================================================== Busca no db ==============================================================

    def RegSrchOne(self, event):
        try:
            service_id = 'xxxxxxxxxxxxx'
            keyring.set_password(service_id, None, 'xxxxxxxxxxxxx')
            password_key = keyring.get_password(service_id, None)

            con = mc.connect(
                    host="xxxxxxxxxxxxx",
                    user="xxxxxxxxxxxxx",
                    password=password_key,
                    database="xxxxxxxxxxxxx"
                )
            self.input1 = self.buscaedt.text()
            self.input2 = self.searchby.currentText()
            print(f"buscar:{self.input1}\npor:{self.input2}")
            if self.searchby.currentText() == "Nome":
                query = f"SELECT * FROM knowhow.cadastro_clientes_fornecedores WHERE Nome LIKE '%{self.input1}%'"
                cursor = con.cursor()
                cursor.execute(query)
                result = cursor.fetchall()

                self.TableView.setRowCount(0)

                for row_number, row_data in enumerate(result):
                    self.TableView.insertRow(row_number)
                    for column_number , data in enumerate(row_data):
                        if column_number == 0:
                            self.item = QTableWidgetItem(f"{row_data[0]}") # ID together with checkbox
                            self.item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                            self.item.setCheckState(Qt.CheckState.Unchecked)
                            self.TableView.setItem(row_number, column_number, self.item)                     
                        else:
                            self.TableView.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                self.TableView.resizeRowsToContents()
                self.TableView.resizeColumnsToContents()
                self.TableView.setColumnWidth(0, 70)
                self.TableView.show()
                self.hidden = False

            elif self.searchby.currentText() == "CNPJ":
                query = f"SELECT * FROM knowhow.cadastro_clientes_fornecedores WHERE CNPJ LIKE '%{self.input1}%'"
                cursor = con.cursor()
                cursor.execute(query)
                result = cursor.fetchall()

                self.TableView.setRowCount(0)

                for row_number, row_data in enumerate(result):
                    self.TableView.insertRow(row_number)
                    for column_number , data in enumerate(row_data):
                        if column_number == 0:
                            self.item = QTableWidgetItem(f"{row_data[0]}") # ID together with checkbox
                            self.item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                            self.item.setCheckState(Qt.CheckState.Unchecked)
                            self.TableView.setItem(row_number, column_number, self.item)                     
                        else:
                            self.TableView.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                self.TableView.resizeRowsToContents()
                self.TableView.resizeColumnsToContents()
                self.TableView.setColumnWidth(0, 70)
                self.TableView.show()
                self.hidden = False

            elif self.searchby.currentText() == "ID":
                query = f"SELECT * FROM knowhow.cadastro_clientes_fornecedores WHERE ID LIKE '{self.input1}'"
                cursor = con.cursor()
                cursor.execute(query)
                result = cursor.fetchall()

                self.TableView.setRowCount(0)

                for row_number, row_data in enumerate(result):
                    self.TableView.insertRow(row_number)
                    for column_number , data in enumerate(row_data):
                        if column_number == 0:
                            self.item = QTableWidgetItem(f"{row_data[0]}") # ID together with checkbox
                            self.item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                            self.item.setCheckState(Qt.CheckState.Unchecked)
                            self.TableView.setItem(row_number, column_number, self.item)                     
                        else:
                            self.TableView.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                self.TableView.resizeRowsToContents()
                self.TableView.resizeColumnsToContents()
                self.TableView.setColumnWidth(0, 70)
                self.TableView.show()
                self.hidden = False

            elif self.searchby.currentText() == "CPF":
                query = f"SELECT * FROM knowhow.cadastro_clientes_fornecedores WHERE CPF LIKE '{self.input1}'"
                cursor = con.cursor()
                cursor.execute(query)
                result = cursor.fetchall()

                self.TableView.setRowCount(0)

                for row_number, row_data in enumerate(result):
                    self.TableView.insertRow(row_number)
                    for column_number , data in enumerate(row_data):
                        if column_number == 0:
                            self.item = QTableWidgetItem(f"{row_data[0]}") # ID together with checkbox
                            self.item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                            self.item.setCheckState(Qt.CheckState.Unchecked)
                            self.TableView.setItem(row_number, column_number, self.item)                     
                        else:
                            self.TableView.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                self.TableView.resizeRowsToContents()
                self.TableView.resizeColumnsToContents()
                self.TableView.setColumnWidth(0, 70)
                self.TableView.show()
                self.hidden = False

        except mc.Error as e:
            msg = QMessageBox()
            msg.setText(f"Falha ao buscar: {e}")
            msg.setWindowTitle("Busca")
            msg.exec()
            pass

        except Exception as b:
            msg = QMessageBox()
            msg.setText(f"Falha: {b}")
            msg.setWindowTitle("Fail")
            msg.exec()
            pass

        self.TableView.resizeRowsToContents()
        self.TableView.resizeColumnsToContents()
        self.TableView.setColumnWidth(0, 70)
        self.TableView.show()

        #print(str(row_data))
        self.IDdel.setText(str(row_data[0]))
        self.nameedt.setText(str(row_data[1]))
        self.fanedt.setText(str(row_data[2]))
        self.personbox.setCurrentText(str(row_data[3]))
        self.cnpjedt.setText(str(row_data[4]))
        self.cpfedt.setText(str(row_data[5]))
        self.codebox.setCurrentText(str(row_data[6]))
        self.desdeedt.setText(str(row_data[7]))
        self.contribbox.setCurrentText(str(row_data[8]))
        self.stateregedt.setText(str(row_data[9]))
        self.cityregedt.setText(str(row_data[10]))
        if str(row_data[11]) == "Sim":
            self.IEchck.setChecked(True)
        else:
            self.IEchck.setChecked(False)
        self.RGEdt.setText(str(row_data[12]))
        self.emissedt.setText(str(row_data[13]))
        self.countryedt.setText(str(row_data[14]))
        self.cepedt1.setText(str(row_data[15]))
        self.statebox.setCurrentText(str(row_data[16]))
        self.cityedt.setText(str(row_data[17]))
        self.bairroedt.setText(str(row_data[18]))
        self.enderecoedt1.setText(str(row_data[19]))
        self.numeroedt.setText(str(row_data[20]))
        self.complementedt.setText(str(row_data[21]))
        self.cepedt2.setText(str(row_data[22]))
        self.statebox2.setCurrentText(str(row_data[23]))
        self.cityedt2.setText(str(row_data[24]))
        self.bairroedt2.setText(str(row_data[25]))
        self.enderecoedt2.setText(str(row_data[26]))
        self.numeroedt2.setText(str(row_data[27]))
        self.complementedt2.setText(str(row_data[28]))
        self.foreign_state.setText(str(row_data[29]))
        self.foreign_state2.setText(str(row_data[30]))
        self.infoedt.setText(str(row_data[31]))
        self.pessoasedt.setText(str(row_data[32]))
        self.foneedt.setText(str(row_data[33]))
        self.faxedt.setText(str(row_data[34]))
        self.celedt.setText(str(row_data[35]))
        self.celedt2.setText(str(row_data[36]))
        self.emailedt.setText(str(row_data[37]))
        self.emailedtnfe.setText(str(row_data[38]))
        self.siteedt.setText(str(row_data[39]))
        self.celedt3.setText(str(row_data[40]))
        self.celedt4.setText(str(row_data[41]))
        self.cargaedt.setText(str(row_data[42]))
        self.contratoedt.setText(str(row_data[43]))
        self.situation_box.setCurrentText(str(row_data[44]))
        self.VendEdt.setText(str(row_data[45]))
        self.CondEdt.setText(str(row_data[46]))
        self.InscrEdt.setText(str(row_data[47]))
        """
        a lógica aqui é o seguinte: pegar o caminho descrito no db
        tratá-lo e passá-lo como argumento do pixmap
        fazendo asism, aparecer o pixmap no label no local correto para cada registro
        """
        self.teste = row_data[48]
        self.y = str(self.teste)
        self.z = self.y.split("b")
        imagem = ""
        imagem = str(self.z[1]) # tratamento caminho da imagem
        imagem = imagem.split("b") # forma uma lista
        imagex = ""
        imagex = imagem[0]
        imagex = imagex.replace("'", "") # caminho tratado
        if str(row_data[48]) != "None":
            self.pic_pixmap = QPixmap(imagex) # exibir imagem a parir do path tratado
            self.pic_pixmap2 = self.pic_pixmap.scaledToWidth(80) # fixa tamanho imagem para 80 pixel
            self.piclbl2.setPixmap(QPixmap(self.pic_pixmap2))
            self.piclbl2.resize(20, 20)
            print("1442 Entrou na funcao exibir imagem")
            
        else:
            print("none img")
        self.CredEdt.setText(str(row_data[49]))
        self.CondEdt.setText(str(row_data[50]))
        self.CategoryEdt.setText(str(row_data[51]))
        self.Comment.setText(str(row_data[52]))

        self.buscaedt.setFont(QFont("Arial", 9, 4))
        self.buscaedt.setStyleSheet("border-radius: 7px; background-color: white; color: gray; padding: 7px 14px; border-width:1px; border-color: gray; border-style:solid;")
        self.buscaedt.setText("Selecionar método de busca e digitar:")   

        
    def ShowHideTable(self):
        if self.hidden:
            self.TableView.show()
            self.hidden = False
        else:
            self.TableView.hide()
            self.hidden = True
            
    def ClearBusca(self, event):
        self.buscaedt.clear()
        self.buscaedt.setFont(QFont("Arial", 12, 12))
        self.buscaedt.setStyleSheet("border-radius: 7px; background-color: white; color: black; padding: 7px 14px; border-width:1px; border-color: #44a665; border-style:solid;")
        if self.searchby.currentText() == "CNPJ":
            self.buscaedt.setInputMask("99.999.999/9999-99")
        elif self.searchby.currentText() == "CPF":
            self.buscaedt.setInputMask("999.999.999-99")
        elif self.searchby.currentText() == "ID":
            self.buscaedt.setInputMask("999999")
        else:
            pass

        
app = QApplication(sys.argv)

xxxxxxxxxxxxx = MainTree()
xxxxxxxxxxxxx.show()
app.exec()

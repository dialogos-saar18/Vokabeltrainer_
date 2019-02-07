# -*- coding: cp1252 -*-
from com.clt.dialog.client import Client
from javax.swing import JPanel, JFrame, JTable, JLabel, ImageIcon, JButton, BoxLayout, Box, JTextField, JTextArea, JScrollPane, JViewport
from javax.swing.table import DefaultTableModel
from java.awt import Color,Font
from java.awt import Dimension
from java.lang import Class
from java.sql import Connection
from java.sql import DriverManager 
from java.sql import Statement
import java.sql.SQLException as SQLError
from java.sql import PreparedStatement
from leoanfragetest import *
Class.forName("org.sqlite.JDBC")
url = "jdbc:sqlite:C:/Users/marc_/Desktop/Dialogsysteme/Vokabeltrainer/VokTrainer2/Vokabeltrainer2/jython-demo-client-master/Lektionen.db"
conn = DriverManager.getConnection(url)
stmt = conn.createStatement()
pfad = "C:/Users/marc_/Desktop/Dialogsysteme/Vokabeltrainer/VokTrainer2/Vokabeltrainer2/jython-demo-client-master/jython-demo-client-master_neueLektion/Lektionen/alleLektionen"
import random

#Feedback Frame für die Abfrage
# Wird später sichtbar gemacht
def close2(event):
    frame_feedback.setVisible(False)
frame_feedback = JFrame('Abfrage',defaultCloseOperation = JFrame.EXIT_ON_CLOSE, size=(1000,1000))
frame_feedback.setLayout(None) 
uebersichtLabel2 = JLabel()
uebersichtLabel2.setText("<html><font size=+1 color=#191970>vorhandene Lektionen:</font></html>")
uebersichtLabel2.setBounds(450,200,250,50)
uebersicht2 = JTextArea()
uebersicht2.editable = False
uebersicht_scroll2 = JScrollPane(uebersicht2)
uebersicht_scroll2.viewport.view = uebersicht2
uebersicht_scroll2.setBounds(450,250,250,410)
feld_feedback = JTextArea()
feld_feedback.editable = False
feld_feedback.setBounds(50,50,300,600)
button_close = JButton('close window', actionPerformed=close2)
button_close.setBounds(50,650,300,30)
hintergrund2 = ImageIcon("Hintergrund.jpg")
pnl2 = JPanel()
hintergrundlabel2 = JLabel(hintergrund2)
frame_feedback.setContentPane(hintergrundlabel2)
frame_feedback.add(button_close)
frame_feedback.add(uebersicht_scroll2)
frame_feedback.add(uebersichtLabel2)
frame_feedback.add(feld_feedback)
frame_feedback.setVisible(False)

class Main(Client):
    def __init__(self):
        pass

    def stateChanged(self, cs):
        print "new state: " + str(cs)

    def sessionStarted(self):
        print "session started"

            
    def reset(self):
        print "reset"
    
    def output(self, value):
        eingabe = value.getString()
        if eingabe == "Lexikon":
            # Falls "Lexikon" an den Clienten übergeben wird, wird die GUI geöffnet,
            # in der man deutsche Wörter eingeben kann, die einem dann auf Englisch
            # vorgelesen werden.
            def change_text(event):
                text = feld.getText()
                x = suche(text)
                self.send(x)
                frame.visible  = False
            frame = JFrame('Woerterbuch',defaultCloseOperation = JFrame.EXIT_ON_CLOSE,size = (380, 350), )
            frame.setLayout(None)
            frame.visible = True
            hintergrund = ImageIcon("Hintergrund.jpg")
            hintergrundlabel = JLabel(hintergrund)
            frame.setContentPane(hintergrundlabel)

            uebersetzerlabel = JLabel()
            uebersetzerlabel.setForeground(Color(025,025,112))
            uebersetzerlabel.setText("<html><font size=+1>Welches Wort soll ich uebersetzen?</font></html>")
            uebersetzerlabel.setBounds(10,20,500,50)
            frame.add(uebersetzerlabel)

            feld = JTextField()
            feld.setText("")
            feld.setBounds(20,80,300,25)
            frame.add(feld)

            button = JButton('Uebersetzen', actionPerformed=change_text,size=(10,20))
            button.setBounds(20,110,300,30)
            frame.add(button)

        if eingabe == "neue Lektion":
            # Falls dem Clienten "neue Lektion" übergeben wird, öffnet er er die
            # GUI für das Verwalten der Lektionen
            frame = JFrame('Lektion erstellen',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE,size = (1000, 1000))
            frame.setLayout(None)

            def auflisten_in(ort):
                font = Font("Verdana",Font.BOLD, 15)
                liste_mit_Lektionen = []
                with open(pfad,"r") as f:
                    for line in f:
                         liste_mit_Lektionen.append(line.strip())
                liste_mit_Lektionen.sort()
                text = ""
                for lektion in liste_mit_Lektionen:
                    text += lektion
                    text += "\n"
                ort.setText(text)
                ort.setFont(font)            
                frame.setLayout(None)
                uebersichtLabel = JLabel()  
            
            def uebersetzen(event):
                frage = feld_frage.getText()
                x = suche(frage)
                feld_frage.setText(x)
                liste = []
                with open(pfad,"r") as lektionen:
                    for lektion in lektionen:
                        if "nachgeschlagen" in lektion:
                            liste.append(lektion)
                if liste:
                    name = liste[-1]
                    words = []
                    sql = "SELECT deutsch, englisch, symbol FROM "+name
                    zeile = stmt.executeQuery(sql)
                    while zeile.next():
                        d = zeile.getString("deutsch")
                        e = zeile.getString("englisch")
                        symb = zeile.getString("symbol")
                        words.append((d,e,symb))
                    if len(words)<50:
                        sql = "INSERT INTO "+name+" (deutsch, englisch, symbol)  VALUES(?,?,?);"
                        pstmt = conn.prepareStatement(sql)
                        pstmt.setString(1,frage)
                        pstmt.setString(2,x)
                        pstmt.setString(3,"X")
                        pstmt.executeUpdate()
                    else:
                        namensteile = name.split("_")
                        nummer = int(namensteile[1].strip())+1
                        name = "nachgeschlagen_"+str(nummer)
                        test = ""
                        with open(pfad,"r") as f:
                            for line in f:
                                test += line
                        if not name in test:
                            with open(pfad,"a") as f:
                                f.write(name+"\n")
                        sql = "CREATE TABLE "+name+" (deutsch text, englisch text, symbol text);"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                        stmt.execute(sql)
                        sql = "INSERT INTO "+name+" (deutsch, englisch, symbol)  VALUES(?,?,?);"
                        pstmt = conn.prepareStatement(sql)
                        pstmt.setString(1,frage)
                        pstmt.setString(2,x)
                        pstmt.setString(3,"X")
                        pstmt.executeUpdate()       
                else:
                    name = "nachgeschlagen_1"
                    test = ""
                    with open(pfad,"r") as f:
                        for line in f:
                            test += line
                    if not name in test:
                        with open(pfad,"a") as f:
                            f.write(name+"\n")
                    sql = "CREATE TABLE "+name+" (deutsch text, englisch text, symbol text);"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                    stmt.execute(sql)
                    sql = "INSERT INTO "+name+" (deutsch, englisch, symbol)  VALUES(?,?,?);"
                    pstmt = conn.prepareStatement(sql)
                    pstmt.setString(1,frage)
                    pstmt.setString(2,x)
                    pstmt.setString(3,"X")
                    pstmt.executeUpdate()
                auflisten_in(uebersicht)

            def delete(event):
                name = feld.getText()
                print name
                print self.geladen
                if name == self.geladen:
                    count = 0
                    while tabelle.getValueAt(count,0)!= None:
                        tabelle.setValueAt(None,count,0)
                        tabelle.setValueAt(None,count,1) 
                        count += 1
                stmt.execute("DROP TABLE "+name+";")
                lektionen = []
                with open(pfad,"r") as f:
                    for line in f:
                        lektion = line.strip()
                        if not name == lektion:
                            lektionen.append(lektion)
                with open(pfad,"w") as f:
                    for lektion in lektionen:
                        f.write(lektion+"\n")
                auflisten_in(uebersicht)

            def laden(event):
                name = feld.getText()
                self.geladen = name
                sql = "SELECT deutsch, englisch FROM "+name
                results = stmt.executeQuery(sql)
                count = 0
                while results.next():
                    d = results.getString("deutsch")
                    e = results.getString("englisch")
                    tabelle.setValueAt(d,count,0) 
                    tabelle.setValueAt(e,count,1) 
                    count += 1
                while tabelle.getValueAt(count,0)!= None:
                    tabelle.setValueAt(None,count,0)
                    tabelle.setValueAt(None,count,1) 
                    count += 1

            def erstelle_Lektionstabelle(event):
                reihen = []
                for i in range(0,50):
                    deutsch = tabelle.getValueAt(i,0)
                    englisch = tabelle.getValueAt(i,1)
                    if deutsch != None:
                        symbol = "X"
                        reihen.append([deutsch,englisch,symbol])
                    else:
                        break
                z = 0
                name = feld.getText()
                sql = "CREATE TABLE "+name+" (deutsch text, englisch text, symbol text);"
                try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                    stmt.execute(sql)
                except SQLError:
                    stmt.execute("DROP TABLE "+name+";")
                    stmt.execute(sql)
                for reihe in reihen:
                    print(reihe)
                    deutsch = reihe[0]
                    englisch = reihe[1]
                    symbol = reihe[2]
                    sql = "INSERT INTO "+name+" (deutsch, englisch, symbol)  VALUES(?,?,?);"
                    pstmt = conn.prepareStatement(sql)
                    pstmt.setString(1,deutsch)
                    pstmt.setString(2,englisch)
                    pstmt.setString(3,symbol)
                    pstmt.executeUpdate()
                test = ""
                with open(pfad,"r") as f:
                    for line in f:
                        test += line
                if not name in test:
                    with open(pfad,"a") as f:
                        f.write(name+"\n")
                self.send(name)
                frame.setVisible(False)

            frame = JFrame('Vokabel Listen',defaultCloseOperation = JFrame.EXIT_ON_CLOSE, size=(1000,1000))
            frame.setLayout(None) 
            label_enter = JLabel()
            label_enter.setText("<html><font size=+0.5 color = 000000>Bitte vor dem Speichern<br>die Entertaste bedienen</font></html>")
            label_enter.setBounds(20,720,250,50)
            uebersichtLabel = JLabel()
            uebersichtLabel.setText("<html><font size=+1 color=#191970>Bereits vorhandene Lektionen:</font></html>")
            uebersichtLabel.setBounds(450,230,250,50)
            uebersicht = JTextArea()
            uebersicht.editable = False
            uebersicht_scroll = JScrollPane(uebersicht)
            uebersicht_scroll.viewport.view = uebersicht
            uebersicht_scroll.setBounds(450,300,250,380)
            auflisten_in(uebersicht)
            button = JButton('Lektion speichern/Lektion reseten', actionPerformed=erstelle_Lektionstabelle,size=(10,20))
            button.setBounds(20,700,300,30)
            button_laden = JButton('vorhandene Lektion laden', actionPerformed=laden,size=(10,20))
            button_laden.setBounds(20,110,210,30)
            button_delete = JButton("Lektion entfernen",actionPerformed=delete)
            button_delete.setBounds(20,140,210,30)
            hintergrund = ImageIcon("Hintergrund.jpg")
            pnl = JPanel()
            hintergrundlabel = JLabel(hintergrund)
            frame.setContentPane(hintergrundlabel)
            lektionsnamensLabel = JLabel()
            lektionsnamensLabel.setForeground(Color(025,025,112))
            lektionsnamensLabel.setText("<html><font size=+1>Hier bitte Namen der Lektion eingeben<br>(Nur ein Wort lang)</font></html>")
            lektionsnamensLabel.setBounds(10,20,500,50)
            frame.add(lektionsnamensLabel)
            feld = JTextField()
            feld.setText("")
            feld.setBounds(20,80,210,25)
            frame.add(feld)
            column_names = ["<html><font size=+1 color=#191970><b>Deutsch</b></font></html>","<html><font size=+1 color=#191970><b>Englisch</b></font></html>"]
            table_model = DefaultTableModel(column_names,50)
            tabelle = JTable(table_model)
            lektionsnamensLabel.setForeground(Color(025,025,112))
            scrollbar = JScrollPane(tabelle)
            scrollbar.viewport.view = tabelle
            scrollbar.setVerticalScrollBarPolicy(scrollbar.VERTICAL_SCROLLBAR_ALWAYS)
            scrollbar.setVisible(True)
            tabelle.setVisible(True)
            scrollbar.setBounds(20,190,300,490)
            feld_frage = JTextField()
            feld_frage.setText("")
            feld_frage.setBounds(450,30,300,50)
            uebersetzerlabel = JLabel()
            uebersetzerlabel.setForeground(Color(025,025,112))
            uebersetzerlabel.setText("<html><font size=+1>Hier kannst Du ein deutsches Wort eintragen,<br>dass ich fuer Dich nachschlage</font></html>")
            uebersetzerlabel.setBounds(450,80,500,50)
            button_uebersetzen = JButton('Uebersetzen', actionPerformed=uebersetzen,size=(10,20))
            button_uebersetzen.setBounds(450,130,300,30)
            frame.add(button_uebersetzen)
            frame.add(uebersetzerlabel)
            frame.add(feld_frage)
            frame.add(feld)
            frame.add(scrollbar)
            frame.add(button)
            frame.add(button_laden)
            frame.setVisible(True) 
            frame.add(uebersicht_scroll)
            frame.add(uebersichtLabel)
            frame.add(button_delete)
            frame.add(label_enter)
        elif eingabe == "alle Lektionen auflisten":
            # Hier erstellt der Client eine dynamische Grammatik
            # mit den vorhandenen Lektionen, die man sich abfragen lassen kann
            # und gibt diese wieder an DialogOS zurück.
            # Außerdem wird der Feedback Frame geöffnet.
            def auflisten_in2(ort):
                font = Font("Verdana",Font.BOLD, 15)
                liste_mit_Lektionen = []
                with open(pfad,"r") as f:
                    for line in f:
                        liste_mit_Lektionen.append(line.strip())
                        liste_mit_Lektionen.sort()
                text = ""
                for lektion in liste_mit_Lektionen:
                    text += lektion
                    text += "\n"
                ort.setText(text)
                ort.setFont(font)


            frame_feedback.setVisible(True)
            auflisten_in2(uebersicht2)
            grammatik = ""
            grammatik = "root $NamevonLektion;\n"
            grammatik += "$NamevonLektion = "
            with open(pfad,"r") as f:
                z = 0
                for line in f:
                    if z == 0:
                        if not "_" in line:
                            grammatik += line
                        else:
                            zeile = line.split("_")
                            grammatik += zeile[0]+" "
                            grammatik += zeile[1].strip()
                    else:
                        if not "_" in line:
                            grammatik += "|"+line
                        else:
                            zeile = line.split("_")
                            grammatik += "|"+zeile[0]+" "
                            grammatik += zeile[1].strip()
                    if line != "\n":
                        z += 1
            grammatik += ";"
            self.send(grammatik)
        elif "sende" in eingabe:
            # DialogOS sagt dem Clienten, welche Lektion der User abgefragt
            # werden möchte. Der Client ließt dann die entsprechende Lektion
            # aus der Datenbank aus und gibt eine Liste mit 2 Listen zurück.
            # In der ersten Liste befinden sich die deutschen Bedeutungen, der
            # noch nicht gewussten Wörter, in der 2. Liste die englsichen Bedeutungen.
            # Falls alle Wörter bereits gekonnt wurden, wird stattdessen eine entsprechende
            # Anmerkung an DialogOS geschickt und DialogOS informiert den User darüber.
            z = 0
            if "nachgeschlagen" in eingabe:
                bestandteile = eingabe.split()
                name = bestandteile[1]+"_"+bestandteile[2]
            else:
                name = eingabe.split()[1]
            sql = "SELECT deutsch, englisch, symbol FROM "+name
            vokabelliste = stmt.executeQuery(sql)
            deutsch = []
            englisch = []
            symbol = []
            while (vokabelliste.next()):
                deutsch.append(vokabelliste.getString("deutsch"))
                englisch.append(vokabelliste.getString("englisch"))
                symbol.append(vokabelliste.getString("symbol"))
                
            indices = range(0,len(deutsch))
            random.shuffle(indices)
            vokabeln = [[],[]]
            for index in indices:
                d = deutsch[index]    
                e = englisch[index]
                s = symbol[index]
                if s == "X":
                    vokabeln[0].append(d)
                    vokabeln[1].append(e)
            if vokabeln[0]:
                self.send(vokabeln)
            else:
                self.send(["Du kannst diese Lektion schon komplett. Wenn Du sie wieder abgefragt werden willst, resete sie bitte unter Wokabeln verwalten."])
        else:
            # Dieser Teil des Codes wird während der Abfrage ausgeführt.
            # Nach jeder neuen Vokabel wird dann in ein Feld im Feedback
            # Frame die deutsche, die englische Vokabel und ein Symbol angezeigt,
            # welches einen darüber informiert, ob man die Vokabel wusste, oder nicht.
            # (O für gewusst und X für nicht gewusst)
            nametext = eingabe.split(":")
            name = nametext[0]
            text = nametext[1]
            feld_feedback.setText(text)
            zeilen = text.split("\n")
            symb = zeilen[-2].split("\t")[-1]
            d = zeilen[-2].split("\t")[-3]
            print d
            sql = "UPDATE "+name+" SET symbol = ? WHERE deutsch = ?"
            pstmt = conn.prepareStatement(sql)
            pstmt.setString(1, symb)
            pstmt.setString(2, d)
            pstmt.executeUpdate()
            
    def getName(self):
        return "Jython demo client"

    def error(self, throwable):
        print "error"


m = Main()
m.open(8000)




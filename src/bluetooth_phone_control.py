import bluetooth
import os

host=''
port = 1		#le rasp utilise le port 1 pour le SPP

keyCommand = ""
valeurCommand = ""



server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Socket bluetooth on')
try:
	server.bind((host, port))
	print("Bind Bluetooth ok")
except:
	print("Bind Bluetooth echoue")
server.listen(1)		#1 seul client --> portable
client, adress = server.accept()
print("Connecte a : ", adress)
print("Client : ", client)


def end_connection():
	client.close()
	server.close()
	os.system("python $HOME/SoundBerry/src/bluetooth_phone_control.py")
	
	
def analyse_trame(donnee):
		global keyCommand
		global valeurCommand
		
		i = 0
		position_point = 0
		
		for i in range(len(donnee)):
			if donnee[i] == '.':
				position_point = i
				keyCommand = donnee[i-1]
				valeurCommand = donnee[position_point+1 : len(donnee)]
def case_keyCommand(key):
	if key == 'v':
		commande = "amixer set Master " + valeurCommand
		os.system(commande)
		
	if key == '0':
		commande = "amixer -D equal sset 00.\ 31\ Hz " + valeurCommand
		os.system(commande)
	if key == '1':
		commande = "amixer -D equal sset 01.\ 63\ Hz " + valeurCommand
		os.system(commande)
	if key == '2':
		commande = "amixer -D equal sset 02.\ 125\ Hz " + valeurCommand
		os.system(commande)
	if key == '3':
		commande = "amixer -D equal sset 03.\ 250\ Hz " + valeurCommand
		os.system(commande)
	if key == '4':
		commande = "amixer -D equal sset 04.\ 500\ Hz " + valeurCommand
		os.system(commande)
	if key == '5':
		commande = "amixer -D equal sset 05.\ 1\ kHz " + valeurCommand
		os.system(commande)
	if key == '6':
		commande = "amixer -D equal sset 06.\ 2\ kHz " + valeurCommand
		os.system(commande)
	if key == '7':
		commande = "amixer -D equal sset 07.\ 4\ kHz " + valeurCommand
		os.system(commande)
	if key == '8':
		commande = "amixer -D equal sset 08.\ 8\ kHz " + valeurCommand
		os.system(commande)
	if key == '9':
		commande = "amixer -D equal sset 09.\ 16\ kHz " + valeurCommand
		os.system(commande)
	if key == 'c':
		end_connection()
		
def reset_command():
	global keyCommand
	global valeurCommand
	
	keyCommand = 	""
	valeurCommand = ""


try:
	while True:
		donnee_bluez = client.recv(1024)
		
		analyse_trame(donnee_bluez)
		
		print(keyCommand)
		print(valeurCommand)
		case_keyCommand(keyCommand)
		reset_command()	

except:
	end_connection()

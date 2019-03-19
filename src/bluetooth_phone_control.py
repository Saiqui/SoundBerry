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

# On prend le nom de l'interface wifi pour la portabilite
wifiInterface = os.popen("ip -o a | grep \"wl\" | head -n1 | awk '{print $2}'").read()


def end_connection():
	client.close()
	server.close()
	os.system("python /home/pi/SoundBerry/src/bluetooth_phone_control.py")
	
	
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
				
				
def case_keyCommand(key, commandKey):
	if (key == 'v' and commandKey != 'u' and commandKey != 'm'):
		commande = "amixer set Master " + valeurCommand
		print(commande)
		os.system(commande)
	if(key == 'v' and commandKey == 'm'):
		commande = "amixer sset Master mute"
		os.system(commande)
	if(key == 'v' and commandKey == 'u'):
		commande = "amixer sset Master unmute"
		os.system(commande)
		
	if key == 'm':
		os.system("amixer sset Master toggle")
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
		
	if key == 'w':
		commande = "sudo iwlist " + wifiInterface.rstrip() + " scan | grep -i 'essid' >> wifi.txt"
		print(commande)
		os.system(commande)
		essid = open("wifi.txt", "r")
		data = []
		k=0
		while 1:
			line=essid.readline()
			if not line: break
			i=0
			while line[i] != '"':
				i += 1
			i += 1
			while line[i] != '"':
				data.append(line[i])
				i += 1
			data.append(":")
			k+=1

		data_send = "".join(data)
		print(data_send)

		client.send(data_send)

		essid.close()
		os.system("rm wifi.txt")

		
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
		case_keyCommand(keyCommand, valeurCommand)
		reset_command()	

except:
	end_connection()

import bluetooth
import os

host=''
port = 1		#le rasp utilise le port 1 pour le SPP

keyCommand = ""
valeurCommand = ""



# on créer leserver bluetooth en rfcomm pour la lisaison SPP
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


# On prend le nom de l'interface wifi pour la portabilite du script car le nom change selon les versions/devices
wifiInterface = os.popen("ip -o a | grep \"wl\" | head -n1 | awk '{print $2}'").read()


#fonction qui arrête la connection puis relance le script automatiquement
def end_connection():
	client.close()
	server.close()
	os.system("python /home/pi/SoundBerry/src/bluetooth_phone_control.py")
	

#fonction qui analyse la trame reçut par bluetooth :       keyCommand.valeurCommand
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


# reset de keyCommand et ValeurCommand pour eviter des problèmes
def reset_command():
	global keyCommand
	global valeurCommand
	
	keyCommand = 	""
	valeurCommand = ""


# fonction qui permet de recuperer la ssid et le pass du wifi reçu par trame :			ssid.password
def wifiPswdDecodage(trame):
	global wifiSSID
	global wifiPass
	
	for i in range(len(trame)):
				
		if trame[i] == '.':
			position_point = i
			wifiSSID = trame[0 : position_point]
			wifiPass = trame[position_point+1 : len(trame)]
			print(wifiPass)
			print(wifiSSID)
		
	
# fonction qui definit chaque action possible grâce a keyCommand et valeurCommand
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
		commande = "amixer -D equal sset 00.\ 31\ Hz " + valeurCommand + " && amixer -D equal sset 01.\ 63\ Hz " + valeurCommand + " && amixer -D equal sset 02.\ 125\ Hz " + valeurCommand
		os.system(commande)

	if key == '1':
		commande = "amixer -D equal sset 03.\ 250\ Hz " + valeurCommand + "&& amixer -D equal sset 04.\ 500\ Hz " + valeurCommand + " && amixer -D equal sset 05.\ 1\ kHz " + valeurCommand + " && amixer -D equal sset 06.\ 2\ kHz " + valeurCommand
		os.system(commande)

	if key == '2':
		commande = "amixer -D equal sset 07.\ 4\ kHz " + valeurCommand + " && amixer -D equal sset 08.\ 8\ kHz " + valeurCommand + " && amixer -D equal sset 09.\ 16\ kHz " + valeurCommand
		os.system(commande)

		
	if key == 'w' and commandKey == 'l':
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
	
	if key == 'w' and commandKey == 'c':
		print("debug debut ici")
		client.send("ok")
		print('ok envoyer')
		data = client.recv(1024)
		print('donnee recu')
		wifiPswdDecodage(data)
		commande = "sudo nmcli d wifi connect \"" + wifiSSID + "\" password \"" + wifiPass + "\""
		os.system(commande)
		
	if key == 'i':
		
		info_ssid = "nmcli connection show | grep -i 'wlan0' | awk '{print$1}'"
		os.system(info_ssid)
		info_ip = "hostname -I | awk '{print $1}'"
		os.system(info_ip)
		info = os.popen(info_ssid).read().rstrip() + ':' + os.popen(info_ip).read().rstrip() + ':'
		print(info)
		client.send(info)
		
	if key == 'c':
		end_connection()
		
# coeur du programme qui tourne en boucle jusqu'a la fin de la connexion bluetooth
try:
	while True:
		
		donnee_bluez = client.recv(1024)
		
		analyse_trame(donnee_bluez)

		print(keyCommand)
		print(valeurCommand)
		case_keyCommand(keyCommand, valeurCommand)
		reset_command()
		print('====================================================================\n')

except:
	end_connection()
	

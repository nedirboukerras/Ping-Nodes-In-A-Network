from os import posix_fadvise
from subprocess import run
import re
#fichier qui contiendra le resultat 
file=open('result_ping.txt','w')
#executer ifconfig pour recuperer l adresse IP et le masque et l adresse de diffusion
res=run(['ifconfig'],capture_output=True)
j=res.stdout.decode('utf-8')
#expression reguliere pour garder uniquement les adresses IP lors de l execution de ifconfig
ipAddress=re.findall('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',j)
#combien d adresses IP on a
size=len(ipAddress)
#recuperer uniquement l adresse IP qui nous interesse
i=0
for i in range(size):
    if(ipAddress[i]!='127.0.0.1' and ipAddress[i].find('255')==-1):
        #adresse IP
        ipAddressHost=ipAddress[i]
        #le masque
        mask=ipAddress[i+1]
        #adresse de diffusion
        broadcast=ipAddress[i+2]
#transformer l adresse IP et le masque en liste pour faire un ET binaire
tempHost=ipAddressHost.split('.')
tempMask=mask.split('.')
#liste qui va contenir l adreese du reseau
tempAddressNetwork=[]
for i,j in zip(tempHost,tempMask):
    #ip host and masque
    tempAddressNetwork.append(str(int(i) & int(j)))
#transformer le resultat (adresse reseau) en chaine de caracteres
ipAddressNetwork='.'.join(tempAddressNetwork)
#transformer l adresse reseau et l adresse de diffusion en liste
tempAddressNetwork=ipAddressNetwork.split('.')
tempBroadcast=broadcast.split('.')
#plage d adressage du premier hote au dernier hote
firstHost=int(tempAddressNetwork[3])+1
lastHost=int(tempBroadcast[3])-1
#enlever le dernier octets de l adresse du reseau pour concatiner
del tempAddressNetwork[3]
ipAddressNetwork='.'.join(tempAddressNetwork)
#pinguer tout le reseau
for i in range(firstHost,lastHost+1):
    res=run(['ping' , '-c' , '1',ipAddressNetwork+'.'+str(i)],capture_output=True)
    j=res.stdout.decode('utf-8')
    #si ping reussi ecrire le resultat dans le fichier result_ping.txt
    if(j.find('0 received')==-1):
        file.writelines(ipAddressNetwork+'.'+str(i)+'\n')
#fermer le fichier
file.close()

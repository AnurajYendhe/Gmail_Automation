######################################################################
# importing requried package
######################################################################
import os
import time
import psutil
import urllib.request
import smtplib
import schedule
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

######################################################################
# Function name :- is_connected
# Description :- to check the internet connection
# Input :- Nothing
# Output :- return True(internet connection) / False(No internet connection)
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def is_connected():
    try:
        urllib.request.urlopen('http://www.gmail.com',timeout=11)
        return True
    except urllib.request.URLError as err:
        return False

######################################################################
# Function name :- MailSender
# Description :- to send mail to specified address
# Input :- attachment file path,current time,mail address
# Output :- send mail to specified address
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def MailSender(filename,time,address):
    try:
        fromaddr = "abyendhe@gmail.com"
        toaddr = address

        msg = MIMEMultipart()

        msg['From'] = fromaddr

        msg['To'] = toaddr

        body = """ 
        Hello %s,
        Please find attached ducument which contains Log of Running process.
        Log file is created at : %s

        This is auto gennerated mail.

        Thanks & Regards,
        Anuraj Yendhe
        """%(toaddr,time)


        Subject = """
        Process log generated at : %s
        """%(time)

        msg['Subject'] = Subject

        msg.attach(MIMEText(body,'plain'))

        attachment = open(filename,"rb")

        p = MIMEBase('application','octet-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition',"attachment; filename= %s" % filename)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com',587)

        s.starttls()

        s.login(fromaddr,"ivyl yexa saze dpln")

        text = msg.as_string()

        s.sendmail(fromaddr,toaddr,text)

        s.quit()

        print("Log file successfully sent through Mail")
    
    except Exception as E:
        print("Unable to send mail",E)

######################################################################
# Function name :- CheckAbs
# Description :- check file path is related or absolute
# Input :- Path of directory
# Output :- True(file path is absolute) / False(file path is not absolute)
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def CheckAbs(DirName):
    result = os.path.isabs(DirName)
    return result

######################################################################
# Function name :- AbsolutePath
# Description :- create absolute path of directory
# Input :- Path of directory
# Output :- Absolute Path of directory
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def AbsolutePath(DirName):
    path = os.path.abspath(DirName)
    return path 

######################################################################
# Function name :- CheckDir
# Description :- check directory exists or not
# Input :- Absolute path of directory
# Output :- True(file path is exists) / False(file path is not exists)
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def CheckDir(DirName):
    result = os.path.exists(DirName)
    return result

######################################################################
# Function name :- CreateDir
# Description :- To create directory
# Input :- Absolute path of directory
# Output :- create specified directory
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def CreateDir(DirName):
    try:
        os.mkdir(DirName)
    except:
        pass

######################################################################
# Function name :- ProcessLog
# Description :- write the info about running process into the log file
# Input :- Path of directory,list of running process,mail address
# Output :- generate log file that contain info about running process
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def ProcessLog(DirName,listprocess,mailAddress):
    flag = CheckAbs(DirName)
    if flag == False:
        DirName = AbsolutePath(DirName)

    exist = CheckDir(DirName)
    if(exist == False):
        CreateDir(DirName)

    separator = "-"*150
    log_path = os.path.join(DirName,"Processinfo.log")
    f = open(log_path,'w')
    f.write(separator + "\n")
    f.write("Process Logger at : "+time.ctime()+"\n")
    f.write(separator + "\n")
    f.write("\n")

    for element in listprocess:
        f.write("%s\n"%element)

    f.write("\n") 
    f.write(separator + "\n")
    f.write("Total numbers of running process is %s"%len(listprocess) + "\n")
    f.write(separator + "\n")
    f.close()

    print("Log file successfully generated at location %s" %(log_path)) 

    connected = is_connected()
    if (connected == True):
        startTime = time.time()
        MailSender(log_path,time.ctime(),mailAddress)
        endTime = time.time()

        print('Took %s seconds to send mail' %(endTime - startTime))
    else:
        print("There is no internet connection")

######################################################################
# Function name :- ProcessDisplay
# Description :- create a list which contain info about running process
# Input :- Nothing
# Output :- generate list
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def ProcessDisplay():
    listprocess = []
    
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid','name','username'])
            listprocess.append(pinfo)
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return listprocess

######################################################################
# Function name :- main
# Description :- Main function from where execution starts
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def main():
    print("-------------- Process Automation using Python --------------")

    print("Application Name : ",argv[0])

    if(len(argv) ==  2):
        if(argv[1] == "-h" or argv[1] == "-H"):
            print("This automation script is ues send mail which contain log file in this log file information(name PID and Users) of running process")
            exit()

        elif(argv[1] == "-u" or argv[1] == "-U"):
            print("Usage : Name_of_script Absolute_path_of_Directory Mail_Address")
            print("Example : Assignment12_4.py Anuraj abyendhe@gmail.com")
            exit()    
        else:
            print("Error : Invalid Arguments.")
    
    elif(len(argv) == 3):    
        try:
            list1 = list()
            list1 = ProcessDisplay()
            ProcessLog(argv[1],list1,argv[2])
        except ValueError:
            print("Error : Invalid datatype of input")

        except Exception as E:
            print("Error : Invalid input",E)    

    else:
        print("Error :Invalid number of arguments")
        exit()

######################################################################
# Application stater
######################################################################
if __name__ == "__main__":
    main()

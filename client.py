import sys
import ftplib
from ftplib import FTP
import socket
import os
import configparser

logfile = '/logfile.txt'
ls = 'ls' # list all file under cwd
cd = 'cd' # change dir
ds = 'dw' # download file
upl = 'upl' # upload file
rm = 'rm' #remove a file
cmdlist = ['ls', 'cd', 'dw', 'upl', 'rm', 'mkdir', 'search','rmd', 'spawn', 'rename','logout']
funclist = ['list all file under pwd', 'change dir', 'download file', 'upload file', 'delete file', 'make dir',
            'search by file name', 'remove dir', 'list your local pwd so you can find file to upload','rename a file', 'disconnect']
cnt_list = 11

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(ftp, original_pwd, username, file):
    ftp.cwd('/')
    if(original_pwd == '/'):
        path = original_pwd + file
    else:
        path = original_pwd+'/'+file
    fp = open(logfile, 'a+')
    fwrite(path + '\n')
    fwrite(username + '\n')
    fp.close()
    ftp.cwd(original_pwd)


def downloadfile(downftp, remotepath,localpath):
    bufsize=1024
    fp = open(localpath,'wb')   
    downftp.set_debuglevel(2)
    try:
        downftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    except:
        print(bcolors.WARNING + 'download fail')
        print("chcek typo and do it again" + bcolors.ENDC)
        fp.close()
        return
    print(bcolors.OKCYAN + 'download success'+bcolors.ENDC)
    fp.close()  

def ftpconnect(host, username, password):
    ftp = FTP()
    ftp.connect(host, 21)
    try:
        ftp.login(username, password)
    except (ftplib.error_perm):
        print(bcolors.WARNING +'bad user or password'+bcolors.ENDC)
        return 
    return ftp

'''	
def ftpconnect(host,username,password):
    ftp = FTP()
    ftp.connect(host, 21)
    ftp.login(username, password)
    #ftp.dir()
    return ftp
'''
def uploadfile(ftp,remotepath, name, pwd, username):
    bufsize=1024
    if(pwd == '/'):
        path = pwd + name
    else:
        path = pwd + '/'+ name
    if os.path.isfile(path) == False:
        print(bcolors.WARNING +'file can not open' + bcolors.ENDC)
        return
    fp=open(path,'rb')
    ftp.set_debuglevel(0)
    ftp.cwd(remotepath)
    try:
        ftp.storbinary('STOR '+ name , fp , bufsize)
    except:
        print(bcolors.WARNING + 'upload fail')
        print("somehow do it again")
        fp.close()
        return
    print(bcolors.OKCYAN + 'upload success'+ bcolors.ENDC)
    fp.close()
    #log(ftp, pwd, username, name)




def cwd(ftp,pwd, pos):
    path = pwd
    if(pwd == '/' and pos != '..'):
        path = pwd + pos
    elif(pos != '..'):
        path = pwd + '/' + pos
    try:
        ftp.cwd(path)
    except:
        print(bcolors.WARNING + 'bad path' + bcolors.ENDC)
        return 0
    return 1
    
def remove(ftp, pwd, name, username):
    try:
        fp = open('log.txt','w+')
    except:
        print('open file fail')
        return
    stdout = os.dup(1)
    os.dup2(fp.fileno(), 1)
    fp.close()
    try:
        ftp.dir(name)
    except:
        print(bcolors.WARNING + 'check typo of file name or it can not be dir')
    os.dup2(stdout, 1)
    fp = open('log.txt','r')
    permission = False;
    line = fp.read()
    data = line.split()
    for i in range(len(data)):
        #print(data[i])
        if(data[i] == username):
            permission = True
            break
    os.unlink('log.txt')        
    fp.close()
    if(not permission):
        print(bcolors.WARNING + 'permission denied' + bcolors.ENDC)
        return 
    if(pwd == '/'):
        path = pwd + name
    else:
        path = pwd + '/' + name
    try:
        ftp.delete(path)
    except:
        print(bcolors.WARNING + 'remove fail')
        print("check typo and do it again or permission denied"+bcolors.ENDC)
        return
    print(bcolors.OKCYAN+'delete success'+bcolors.ENDC)
def Rename(ftp, pwd, name, new, username):
    try:
        fp = open('log.txt','w+')
    except:
        print('open file fail')
        return
    stdout = os.dup(1)
    os.dup2(fp.fileno(), 1)
    fp.close()
    try:
        ftp.dir(name)
    except:
        print(bcolors.WARNING + 'check typo of file name or it can not be dir')
    os.dup2(stdout, 1)
    fp = open('log.txt','r')
    permission = False;
    line = fp.read()
    data = line.split()
    for i in range(len(data)):
        #print(data[i])
        if(data[i] == username):
            permission = True
            break
    os.unlink('log.txt')        
    fp.close()
    if(not permission):
        print(bcolors.WARNING + 'permission denied'+bcolors.ENDC)
        return
    try:
        ftp.rename(name, new)
    except:
        print(bcolors.WARNING + 'rename fail')
        print("check conflict"+bcolors.ENDC)
        return
    '''
    print("start to download")
    downftp=ftpconnect('127.0.0.1', 'haha' , '12345')   
    downopsition = '/mnt/c/final_proj/downloadfile'      
    downloadfile(downftp, './txt.c', downopsition)  
    downftp.quit()        
    print("finsih download !")
    
    print("start to upload")
    
    ftp = ftpconnect('127.0.0.1', 'haha', '12345')    
    
    uploadfile(ftp, '/' , '/mnt/c/final_proj/upload.txt') 
    
    ftp.quit()
    print("finsih upload!")
    '''
ip = '127.0.0.1'
print('Welcome to our Server')
print(" ")
user_name = input('pls enter your username : ')
pass_word = input('pls enter your password : ')

cnt_login = 0
while(1): 
    ftp = ftpconnect(ip, user_name, pass_word)
    if(ftp):
        print(bcolors.OKCYAN +'login success')
        break;
    else:
        cnt_login = cnt_login + 1
        if(cnt_login == 3):
            print(bcolors.WARNING + 'fail too many time')
            exit(0)
        print(bcolors.WARNING + 'pls enter again')
        user_name = input(bcolors.ENDC + 'enter your username : ')
        pass_word = input(bcolors.ENDC + 'enter your password : ')

pwd = '/';
first_time_login = True
dir_path = os.path.dirname(os.path.realpath(__file__))
while(1):
    if(first_time_login == True):
        print(bcolors.OKCYAN + 'enter help to see command' + bcolors.ENDC)
        first_time_login = False
    print(bcolors.OKGREEN + user_name + '@' + bcolors.ENDC + ':' + bcolors.OKBLUE + pwd + bcolors.ENDC + '$',end='')
    cmd = input()
    if(cmd == 'ls'):
        try:
            ftp.dir()
        except:
            print(bcolors.WARNING+'permission denied'+ bcolors.ENDC)
    elif(cmd == 'cd'):
        pos = input(bcolors.WARNING + 'enter relative path : ' + bcolors.ENDC)
        if pos == '.':
            continue
        if(pos == '..'):
            i = len(pwd)
            while pwd[i - 1] != '/':
                i = i-1
            pwd = pwd[:i - 1]
            if len(pwd) == 0:
                pwd = '/'
        ok = cwd(ftp, pwd, pos)
        if(ok and pos != '..'):
            if(pwd == '/'):
                pwd = pwd + pos
            else:
                pwd = pwd + '/' + pos
    elif(cmd == 'help'):
        print(bcolors.WARNING + 'All command do not take arguments immediately' + bcolors.ENDC)
        for i in range(cnt_list):
            print('$'+cmdlist[i] + '  ' + funclist[i])
    elif(cmd == 'mkdir'):
        name = input('enter dir name : ')
        try:
            ftp.mkd(name)
        except:
            print(bcolors.WARNING + 'can not make dir'+bcolors.ENDC)
            continue
        #log(ftp, pwd, user_name, name)

    elif(cmd == 'dw'):
        print(bcolors.WARNING + 'enter the filename :'+ bcolors.ENDC,end='')
        name = input()
        downloadfile(ftp, pwd + '/' + name ,dir_path+'/'+name)
        ftp.quit()
        ftp = ftpconnect(ip, user_name, pass_word)
        ftp.cwd(pwd);
    elif(cmd == 'upl'):
        print(bcolors.WARNING + 'enter the filename and the file should in your working dir :' + bcolors.ENDC,end='')
        name = input()
        uploadfile(ftp, pwd, name, dir_path, user_name)
        ftp.quit()
        ftp = ftpconnect(ip, user_name, pass_word)
        ftp.cwd(pwd);
    elif(cmd == 'rm'):
        print(bcolors.WARNING + 'enter file name and this command can not work on dir :'+bcolors.ENDC,end='')
        name = input()
        remove(ftp, pwd, name, user_name)
    elif(cmd == 'search'):
        print(bcolors.WARNING + 'enter file name :' + bcolors.ENDC,end='')
        name = input()
        try:
            ftp.dir(name)
        except:
            print(bcolors.OKCYAN+'seems no such file exist here'+bcolors.ENDC)
    elif(cmd == 'rmd'):
        print(bcolors.WARNING +'enter dir name :'+ bcolors.ENDC,end='')
        name = input()
        try:
            ftp.rmd(name)
        except:
            print(bcolors.WARNING + 'permission denied'+bcolors.ENDC)
            continue
        print(bcolors.OKCYAN + 'remove success'+bcolors.ENDC)
    elif(cmd == 'spawn'):
        os.system('ls -l')
    elif(cmd == 'rename'):
        print(bcolors.WARNING +'enter old file name :',end='')
        old_name = input()
        print(bcolors.WARNING + 'enter new file name :', end='')
        new_name = input()
        print(bcolors.ENDC, end='')
        Rename(ftp, pwd, old_name, new_name, user_name)
    elif(cmd == 'logout'):
        ftp.quit()
        print(bcolors.OKCYAN+'Good Bye'+bcolors.ENDC)
        break;
    else:
        print(bcolors.WARNING + "can not tell the command " + cmd + bcolors.ENDC)    




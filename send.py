import colorama
import html
import smtplib, re, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from configparser import ConfigParser

def _sendEmail(_receiversEmail):
    _config = ConfigParser(interpolation=None)
    _config.read('settings/smtp.ini')
    _smtpHost = _config.get('smtp_server', 'HOST')
    _smtpPort = _config.get('smtp_server', 'PORT')
    _smtpUser = _config.get('smtp_server', 'USER')
    _smtpPass = _config.get('smtp_server', 'PASS')
    _smtpFrom = _config.get('smtp_server', 'FROM')

    ### Replace letter
    _fin = open('settings/letter.txt', 'rt')
    _data = _fin.read()
    _data = _data.replace('####HOST####', _smtpHost)
    _data = _data.replace('####USERNAME####', _smtpUser)
    _data = _data.replace('####FROM####', _smtpFrom)
    _data = _data.replace('####EMAIL_TO####', _receiversEmail)
    _fin.close()

    #_fin = open('settings/letter.txt.dup', 'wt')
    #_fin.write(_data)
    #_fin.close()
    ###
    #_msgHtml = open('settings/letter.txt.dup').read()
    _Letter = """Your Letter"""
    _msgRoot = MIMEMultipart('alternative')
    _hhhtml = MIMEText(_Letter,'html')
    _msgRoot.attach(_hhhtml)
    _msgRoot['From'] = Header(_smtpFrom)
    _msgRoot['To'] =  Header(_receiversEmail)
    _msgRoot['Subject'] = Header('Your Subject')
    
    try:
        _server = smtplib.SMTP(_smtpHost, _smtpPort, timeout=20)
        _server.ehlo()
        _server.starttls()
        _server.ehlo()
        _server.login(_smtpUser, _smtpPass)
        _server.sendmail(_smtpFrom, _receiversEmail, _msgRoot.as_string())
        _server.quit()
        print(' \033[1;36m[\033[31m+\033[36m] \033[32mMessage Sent \033[1;36m[\033[31m+\033[36m] \033[31m---> \033[1;37m: \033[1;37m' + _receiversEmail,'\033[1;37m')
    except smtplib.SMTPException as _errorRes:
        print(_errorRes)
        #_ = os.remove('settings/letter.txt.dup')
        exit()
    
def main(_receiversList):

    for _receiversEmail in _receiversList:
        _regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        if(re.fullmatch(_regexEmail, _receiversEmail)):
            _sendEmail(_receiversEmail)

        else:
            print(' [ - ] ' + _receiversEmail + 'is not email')


if os == 'nt':
    _ = os.system('cls')

else:
    _ = os.system('clear')

print(''' 

███████╗███╗   ███╗████████╗██████╗     ███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝████╗ ████║╚══██╔══╝██╔══██╗    ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
███████╗██╔████╔██║   ██║   ██████╔╝    ███████╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝
╚════██║██║╚██╔╝██║   ██║   ██╔═══╝     ╚════██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
███████║██║ ╚═╝ ██║   ██║   ██║         ███████║███████╗██║ ╚████║██████╔╝███████╗██║  ██║
╚══════╝╚═╝     ╚═╝   ╚═╝   ╚═╝         ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                                                                                                                                             
''')
if __name__ == '__main__':
    try:
        _receiversList = open('receivers/email.txt').read().split()
        main(_receiversList)
    except FileNotFoundError:
        print('[-] File receivers/email.txt not found!')
        print('[-] Please create file email.txt in folder receivers')
        exit()

    #_ = os.remove('settings/letter.txt.dup')

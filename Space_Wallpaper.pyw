from urllib.request import urlopen, urlretrieve
import re,logging,sys,ctypes,os,datetime
from bs4 import BeautifulSoup
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', filename = u'errors.txt')

def StopProgram(message):
    logging.error(message)
    ctypes.windll.user32.MessageBoxA(0, message, b'Error', 0)
    sys.exit()

url = "http://apod.nasa.gov/apod/"
to_find = "IMG SRC="
html = str(urlopen(url).read())
html = html.replace('\\n',' ')
soup = BeautifulSoup(html, 'html.parser')
try:
    image_url = soup.img.get('src')
except:
    StopProgram(b'Something\'s gone wrong! Couldn\'t find URL of the image o.O')
full_url = url + image_url
destination = 'wallpaper' + full_url[-4:]
if '.' not in destination:
    StopProgram(b'Something\'s gone wrong! Couldn\'t find \'.\' (full stop) in URL o.O')
image = urlopen(full_url).read()
fimage = open(destination, "wb")
fimage.write(image)
fimage.close()

full_date = datetime.datetime.now().strftime("%Y %B %d")
date = re.findall(' 0[1-9]',full_date)
if date != []:
    date = str(date[0])
    full_date = full_date.replace(date[1:],date[2:])
flag = 0
for string in soup.stripped_strings:
    if flag:
        break;
    if string == full_date:
        flag = 1;
image_name = string
file = open('explanation.txt',"w")
file.write(full_date+'\n\n')
file.write('\t'+image_name+'\n')
flag = 0
for string in soup.strings:
    if '\\\'' in string:
        string = string.replace('\\\'','\'')
    if 'Tomorrow\'s picture:' in string:
        break
    if 'Explanation:' in string:
        flag = 1
    if flag:
        file.write(string)
file.write('\n\n'+url) 
file.close()

fimage_path = os.getcwd() + '\\' + destination
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, fimage_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)

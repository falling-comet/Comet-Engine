import requests
import re
import os
import pickle
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)


mylist=[]

with open('link.list', 'wb') as f:
    pickle.dump(mylist, f)

def getFilename_fromCd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def direct_download_link(direct_download_link):
    direct_download_link=direct_download_link.split('?')[0]
    direct_download_link=direct_download_link.split('/')[-2]
    direct_download_link='https://docs.google.com/uc?export=download&id='+direct_download_link
    return direct_download_link

def enum_download(num):

    lklist=[]
    fnlist=[]
    fnum_counter=0

    while True:

        url = 'http://lms.ksa.hs.kr/NBoard/download.php?db=vod&idx=%d&fnum=%d'%(num,fnum_counter)
        r = requests.get(url, allow_redirects=True)
        filename = getFilename_fromCd(r.headers.get('content-disposition'))

        if filename==None:
            break
        else:
            open(os.path.join('tempfile',filename), 'wb').write(r.content)
            
            file1 = drive.CreateFile({'title': filename})
            file1.SetContentFile(os.path.join('tempfile',filename))
            file1.Upload()

            if os.path.exists(os.path.join('tempfile',filename)):
                os.remove(os.path.join('tempfile',filename))
            else:
                pass

            file1.InsertPermission({'type': 'anyone','value': 'anyone','role': 'reader'})

            link=file1['alternateLink']


            lklist.append([link,direct_download_link(link)])
            fnlist.append(filename)
        
            fnum_counter+=1
        
    with open('link.list', 'rb') as f:
        link_list = pickle.load(f)
    
    link_list.append([num,fnlist,lklist])

    with open('link.list', 'wb') as f:
        pickle.dump(link_list, f)
    
    print(link_list)



enum_download(10000)
# Comet-Engine
A search engine for our school's LMS  

## Workflow  

#### Downloading

python `requests` is used to download files and other metadata from http://lms.ksa.hs.kr/

```python
url = '***************'
r = requests.get(url, allow_redirects=True)
filename = getFilename_fromCd(r.headers.get('content-disposition'))

if filename==None:
    break
else:
    open(filename, 'wb').write(r.content)
```

#### Uploading

As heroku cannot maintain files, it uploads the files it downloaded to google drive.  

```python
file1 = drive.CreateFile({'title': filename})
file1.SetContentFile(filename)
file1.Upload()
```

#### Get direct download url  

To use in `html` or `css`, we need to get the direct download url of the google drive file.  

```python
def direct_download_link(direct_download_link):
    direct_download_link=direct_download_link.split('?')[0]
    direct_download_link=direct_download_link.split('/')[-2]
    direct_download_link='https://docs.google.com/uc?export=download&id='+direct_download_link
    return direct_download_link

file1.InsertPermission({'type': 'anyone','value': 'anyone','role': 'reader'})

link=file1['alternateLink']

link=direct_download_link(link)
```

#### Append to pickle for later searching  

Then, append to pickle to search later

```python
with open('link.list', 'rb') as f:
    link_list = pickle.load(f)

link_list.append(link+other metadata)

with open('link.list', 'wb') as f:
    pickle.dump(link_list, f)

print(link_list)
```


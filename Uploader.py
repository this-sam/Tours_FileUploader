#uploader.py by Sam Brown

global httplib, base64, hashlib, datetime, formatdate, mktime
from datetime import datetime
from email.utils import formatdate
from time import mktime
import httplib, base64, hashlib

class Uploader():
    
    def __init__(self):
        self.username = "sbrown2594@gmail.com"
        self.password = "bubbles"
        self.base_url = "http://www.eebsy.com"
        self.publickey = "TlTVIFYuzq9UgsSnjnJUUVFOQr1UbzTIwQFyWEaQ0P4xaZZ29wBp9jb18ofMG9rS"
        self.privatekey = "tP8Y798c0tDwVAlgi26ESrTePMFfKVPrkYfRckD6M2tvE5MIEn9w9qm2EZPRFTeF"
        self.date = self.date_rfc822()
        self.headers = {"Date":self.date, "Authorization":"", "accept":"Application/json"}
        #date format Sat, 22 Oct 2011 04:50:43 +0000
        #publickey:base64_encode(sha1(private_key+"\n"+Date)):base64_encode(userID):base64(password)
        
        self.auth_header = self.__build_auth_string(self.publickey, self.privatekey, self.date, self.username, self.password)
        
        
    def date_rfc822(self):
        #http://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python
        now = datetime.now()
        stamp = mktime(now.timetuple())
        return formatdate(
            timeval     = stamp,
            localtime   = False,
            usegmt      = False
        )
    
    def __build_auth_string(self, publickey, privatekey, date, username, password):
        return publickey + ":" + base64.b64encode(hashlib.sha1(privatekey + '\n' + date).hexdigest()) + ":" + base64.b64encode(username) + ":" + base64.b64encode(password)
        
#-------------------------------------------------------------------------------         
#-------------------------------------------------------------------------------    
#http://code.activestate.com/recipes/146306/
    def post_multipart(host, selector, fields, files):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        content_type, body = encode_multipart_formdata(fields, files)
        h = httplib.HTTPConnection(host)
        headers = {
            'User-Agent': 'INSERT USERAGENTNAME',
            'Content-Type': content_type
            }
        h.request('POST', selector, body, headers)
        res = h.getresponse()
        return res.status, res.reason, res.read()
    def encode_multipart_formdata(fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
    
    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
#http://code.activestate.com/recipes/146306/    
#-------------------------------------------------------------------------------    
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    U = Uploader()
    print 'curl -H "Authorization: ' + U.auth_header + '" -H "Date: ' + U.date + '" -H "Accept: application/json" https://www.eebsy.com/api/tour/1'
    
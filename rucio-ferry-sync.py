import pycurl
import io
import json
import yaml
import sys
import os

def main():
    print("I'm alive!")
    capath = "/etc/grid-security/certificates" # cert_path is location of CA certificates
    proxy = "/tmp/x509up_u%s" % (os.getuid()) # location to your proxy
    #url = "https://ferry.fnal.gov:8443" # Ferry url
    #action = "getGroupFile?resourcename=egp" # API call example
    #cmd = "%s/%s" % (url, action)
    #http = pycurl.Curl()
    #http.setopt(pycurl.CAPATH, capath)
    #http.setopt(pycurl.SSLCERT, proxy)
    #buffer = io.BytesIO()
    #http.setopt(pycurl.WRITEFUNCTION, buffer.write)
    #http.setopt(pycurl.URL, cmd)
    #try:
    #    http.perform()
    #except pycurl.error as err:
    #    print ("PyCurl error: {0}".format(err))
    #    sys.exit(1)
    #except pycurl.error as err:
    #    print ("PyCurl error: {0}".format(err))
    #    sys.exit(1)
    #except:
    #    print ("Unexpected error: %s"% (sys.exc_info()[0]))
    #    sys.exit(1)
    #data= buffer.getvalue().decode('UTF-8')
    #if "ferry_error" in data:
    #    print ("ferry_error %s - %s" % (cmd, data))
    #    sys.exit(1)
    #print json.loads(data)
    #sys.exit(0)

if __name__=="__main__":
    main()
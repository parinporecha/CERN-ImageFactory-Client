#!/usr/bin/env python

import argparse
import getpass
import requests
import sys
import json

# For HTTP requests, replace the 'https://' below with 'http://'
IMAGE_BUILDER_BASE_URL = 'https://lxbst0518.cern.ch:8075'
BASE_URL = IMAGE_BUILDER_BASE_URL + '/imagefactory'
PROVIDER_IMAGE_SUFFIX = '/provider_images'

REQUEST_SUCCESSFUL_MESSAGE = "Request Successful"
REQUEST_FAIL_MESSAGE = "Request failed"

UPLOAD_TARGET = 'openstack-kvm'
CERN_CERTIFICATE = '/etc/pki/tls/certs/CERN-bundle.pem'

def print_imagefactory_version():
    r = requests.get(BASE_URL, verify=CERN_CERTIFICATE)

    # For HTTP requests, comment the above line, and uncomment the below one
    #r = requests.get(BASE_URL)
    if (r.status_code == 200):
        print REQUEST_SUCCESSFUL_MESSAGE
    else:
        print REQUEST_FAIL_MESSAGE
    
    print r.text

def build_and_upload_image():
    if (len(sys.argv) < 4):
        print "Usage: ImageFactory_Client <path to provider definition file> <path to openrc credentials file> <path to tdl> <Optional: path to KickStart file>"
        return
    
    provider_definition = _get_file_contents (sys.argv[1])
    openrc_credentials = _get_file_contents (sys.argv[2])
    template = _get_file_contents (sys.argv[3])
    
    password = getpass.getpass(prompt='Please enter your OpenStack Password:\n')
    openrc_credentials = openrc_credentials.replace('export OS_PASSWORD=$OS_PASSWORD_INPUT', 'export OS_PASSWORD=' + password)

    kickstart_file = None
    if len(sys.argv) == 5:
        kickstart_file = _get_file_contents (sys.argv[4])
    
    parameters = json.dumps({'install_script' : kickstart_file})
    
    payload = {'target': UPLOAD_TARGET, 'provider': provider_definition, 'credentials': openrc_credentials, 'template': template, 'parameters': parameters}
    r = requests.post(BASE_URL + PROVIDER_IMAGE_SUFFIX, data = payload, verify=CERN_CERTIFICATE)
    
    # For HTTP requests, comment the above line, and uncomment the below one
    #r = requests.post(BASE_URL + PROVIDER_IMAGE_SUFFIX, data = payload)
    if (r.status_code == 202):
        print REQUEST_SUCCESSFUL_MESSAGE
    else:
        print REQUEST_FAIL_MESSAGE
    
    print r.text

def _get_file_contents (file_path):
    with open(file_path, "r") as file_object:
        contents = file_object.read()
    return contents

def main():
    print_imagefactory_version()
    build_and_upload_image()

main()

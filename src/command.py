
import argparse
import json
import sys
import os
sys.path.append("..")
import time
import reposca.commSca as commSca


def commn():
    '''
    Calls issuescanner
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--method", required=True,
                        choices=['local', 'lcsca'],
                        help="Select scan pr or repo")

    parser.add_argument("url", help="Specify the url/purl/http path to scan")

    parser.add_argument("--thread",default="3", required=False, help="Specify the thread num to scan")

    parser.add_argument("--token", default="" ,required=False, help="Specify the token,Optional input" )

    args = parser.parse_args()
    method = args.method

    if method == 'local':
        comSca = commSca.CommSca()
        result = comSca.locSca(args.url)
        jsonRe = json.dumps(result)
        print(jsonRe + "\n")
    else:   
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))   
        comSca = commSca.CommSca()
        result = comSca.scaResult(args.url, args.thread)
        jsonRe = json.dumps(result)
        print(jsonRe + "\n")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) 


if __name__ == '__main__':
    commn()
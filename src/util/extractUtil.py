import os
import sys
sys.path.append("..")
import shlex
import subprocess
import time
import traceback
import zipfile
import rarfile
import util.popUtil as popUtil
import util.catchUtil as catchUtil
import util.formateUtil as formateUtil

COMPRESSED_LIST = ['tar', 'tgz', 'zip', 'rar']

def extractCode(filePath):
    result = "inde"
    try:
        for deRoot,deDir,deFiles in os.walk(filePath):  
            for defile in deFiles:                        
                dePath = os.path.join(deRoot,defile)
                dePath = formateUtil.formateUrl(dePath)
                wrar = checkWrar(defile)
                if wrar in COMPRESSED_LIST:
                    result = "ref"
                    if wrar == 'tar' or wrar == 'tgz':
                        un_tar(dePath, filePath)
                    elif wrar == 'zip':
                        un_zip(dePath, filePath)
                    else:
                        un_rar(dePath, filePath)
                else:
                    continue
            break
    except Exception as e:
        result = "Except"
        traceback.print_exc()
        pass
    finally:
        return result

@catchUtil.catch_error
def checkWrar(fileName):
    if '.tar' in fileName:
        return 'tar'
    elif '.tgz' in fileName:
        return 'tgz'
    elif '.zip' in fileName:
        return 'zip'
    elif '.rar' in fileName:
        return 'rar'
    else:
        return 'fault'

def un_tar(filePath, tarPath):
    """ungz tar file"""
    try:
        command = shlex.split('tar xf %s -k' % (filePath))
        resultCode = subprocess.Popen(command, cwd=tarPath)
        while subprocess.Popen.poll(resultCode) == None:
            time.sleep(1)                
    except Exception as e:
        traceback.print_exc()
        pass
    finally:
        popUtil.popKill(resultCode) 

def un_zip(filePath, tarPath):
    """ungz zip file"""
    try:
        zip_file = zipfile.ZipFile(filePath)
        for file in zip_file.namelist():
            zip_file.extract(file, path=tarPath)    
    except Exception as e:
        traceback.print_exc()
        pass
    finally:
        zip_file.close()

def un_rar(filePath, tarPath):
    """ungz rar file"""
    try:
        rar = rarfile.RarFile(filePath)
        rar.extractall(path = tarPath)    
    except Exception as e:
        traceback.print_exc()
        pass
    finally:
        rar.close()

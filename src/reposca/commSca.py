
import logging
import os
import sys
sys.path.append("..")
import shlex
import stat
import subprocess
import time
import reposca.analyzeSca as analyzeSca
import reposca.sourceAnalyze as sourceAnalyze
import util.popUtil as popUtil 
import util.extractUtil as extractUtil 
import util.formateUtil as formateUtil
import util.catchUtil as catchUtil

SOURTH_PATH = '/home/repo/tempRepo'
class CommSca(object):
  
    @catchUtil.catch_error
    def locSca(self, path):
        try:
            temJsonSrc = SOURTH_PATH +'/tempJson'
            temJsonSrc = formateUtil.formateUrl(temJsonSrc)
            if os.path.exists(temJsonSrc) is False:
                os.makedirs(temJsonSrc)

            timestamp = int(time.time())
            localRepo = os.path.basename(path)
            tempJson = temJsonSrc + '/' + localRepo +str(timestamp)+'.txt'
            tempJson = formateUtil.formateUrl(tempJson)
            if os.path.exists(tempJson) is False:
                open(tempJson, 'w')

            self._type_ = "inde"
            reExt = extractUtil.extractCode(path)
            if reExt == "Except":
                logging.error("file extracCode error")
            elif reExt == "ref":
                self._type_ = "ref"          

            logging.info("==============START SCAN REPO==============")
            # Call scancode
            command = shlex.split(
                'scancode -l -c %s  --json %s -n 3 --timeout 10 --max-in-memory -1 --license-score 80' % (path, tempJson))
            resultCode = subprocess.Popen(command)
            while subprocess.Popen.poll(resultCode) == None:
                time.sleep(1)
            popUtil.popKill(resultCode)

            scaJson = ""
            # Get json
            with open(tempJson, 'r+') as f:
                list = f.readlines()
                scaJson = "".join(list)
            logging.info("===============END SCAN REPO===============")
            anlyzePath = os.path.dirname(path)
            analyze = analyzeSca.Analyze()
            scaResult = analyze.getScaAnalyze(scaJson, anlyzePath, self._type_, "None", [])
        except Exception as e:
            logger = logging.getLogger(__name__)
        finally:
            # Clear files
            os.chmod(tempJson, stat.S_IWUSR)
            os.remove(tempJson)
            return scaResult


    @catchUtil.catch_error
    def scaResult(self, path, threadNum):
        try:
            temJsonSrc = SOURTH_PATH +'/tempJson'
            temJsonSrc = formateUtil.formateUrl(temJsonSrc)
            if os.path.exists(temJsonSrc) is False:
                os.makedirs(temJsonSrc)

            timestamp = int(time.time())
            localRepo = os.path.basename(path)
            tempJson = temJsonSrc + '/' + localRepo +str(timestamp)+'.txt'
            tempJson = formateUtil.formateUrl(tempJson)
            if os.path.exists(tempJson) is False:
                open(tempJson, 'w')

            self._type_ = "inde"
            reExt = extractUtil.extractCode(path)
            if reExt == "Except":
                logging.error("file extracCode error")
            elif reExt == "ref":
                self._type_ = "ref"          

            logging.info("==============START SCAN REPO==============")
            # Call scancode
            command = shlex.split(
                'scancode -l -c %s  --json %s -n %s --timeout 10 --max-in-memory -1 --license-score 80' % (path, tempJson, threadNum))
            resultCode = subprocess.Popen(command)
            while subprocess.Popen.poll(resultCode) == None:
                time.sleep(1)
            popUtil.popKill(resultCode)

            scaJson = ''
            # Get json
            with open(tempJson, 'r+') as f:
                list = f.readlines()
                scaJson = "".join(list)

            logging.info("===============END SCAN REPO===============")
            scaResult = sourceAnalyze.getSourceData(scaJson, self._type_)
        except Exception as e:
            logger = logging.getLogger(__name__)
        finally:
            os.chmod(tempJson, stat.S_IWUSR)
            os.remove(tempJson)
            return scaResult
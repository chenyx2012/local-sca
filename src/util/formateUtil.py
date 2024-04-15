import os
import sys
sys.path.append("..")

import util.catchUtil as catchUtil


@catchUtil.catch_error
def formateUrl(urlData):
    return urlData.replace("\\", "/")
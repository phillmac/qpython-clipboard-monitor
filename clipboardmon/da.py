import requests
import json
import logging
import os
from pathlib import Path
from requests.auth import HTTPDigestAuth

logger = logging.getLogger(__name__)
config = None
da_address = None
user = None
passwd = None

try:
    conf_path = Path(__file__).parent / 'conf' / 'da.conf.json'
    with conf_path.open() as f:
        config = json.load(f)
        da_address = config.get('da_address')
        user = config.get('username', '')
        passwd = config.get('password','')
        
except:
    cwd = os.getcwd()
    logger.exception(f"Unable to load da handler. cwd: {cwd}")
        
def handleDA(_r, url):
    if not "deviantart.com" in url: return False
    r = requests.post(
        da_address,
        auth=HTTPDigestAuth(user, passwd) if user and passwd else None,
        data={
            "url": url
        }
    )
    r.raise_for_status()
    logger.info(r)
    return True




import requests
import json
import logging
import os
from pathlib import Path
from requests.auth import HTTPDigestAuth

logger = logging.getLogger(__name__)
config = None
tixati_address = None
user = None
passwd = None

try:
    conf_path = Path(__file__).parent / 'conf' / 'tixati.conf.json'
    with conf_path.open() as f:
        config = json.load(f)
        tixati_address = config.get('tixati_address')
        user = config.get('username', '')
        passwd = config.get('password','')
        
except:
    cwd = os.getcwd()
    logger.exception(f"Unable to load tixati handler. cwd: {cwd}")
        
def add_link(addlinktext):
    r = requests.post(
        tixati_address,
        auth=HTTPDigestAuth(user, passwd),
        data={
            "addlink":"Add",
            "addlinktext": addlinktext
        }
    )
    r.raise_for_status()
    logger.info(r)
    return True

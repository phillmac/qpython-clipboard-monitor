#-*-coding:utf8;-*-
#qpy:console

import sys
import logging
import validators
import requests

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

from androidhelper import Android
from time import sleep

from torrent import handleTorrent, handleMagnet 
from da import handleDA

handlers = dict()
handlers['url'] = [handleDA, handleTorrent]
handlers['default'] = [handleMagnet]

def main():
    logging.basicConfig(
	        format='%(asctime)s - %(levelname)s - %(message)s',
	        stream=sys.stdout,
	        level=logging.DEBUG
	    )

    logger = logging.getLogger(__name__)
    droid = Android()
    clipboard = droid.getClipboard().result
    logger.info('Monitoring clipboard')

    while True:
        sleep(.300)
        newclipboard = droid.getClipboard().result
        if newclipboard and clipboard == newclipboard: continue
        if validators.url(newclipboard):
            logger.debug(f"Handling url {newclipboard}")
            try:
                r = requests.get(newclipboard)
                r.raise_for_status()
                for h in handlers.get('url', []):
                    if h(r, newclipboard):
                        logger.debug("OK")
                        break
            except:
                logger.exception('Unhandled exception')
                continue
        else:       
            handled = False
            logger.debug(f"Handling default {newclipboard}")
            
            for h in handlers.get('default', []):
                if h(newclipboard):
                    handled = True
                    logger.debug("OK")
                    break
            if not handled:
                logger.info(f"Unknow clipboard contents {newclipboard}")
            

        clipboard = newclipboard
            
if __name__ == '__main__':
    main()

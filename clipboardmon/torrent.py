import os
import json
import logging
from importlib import import_module
from io import BytesIO

from pathlib import Path
from torf import Magnet, Torrent

logger = logging.getLogger(__name__)

config = None
handler = None

try:
    conf_path = Path(__file__).parent / 'conf' / 'torrent.conf.json'
    with conf_path.open() as f:
        config = json.load(f)
        handler_name = config.get('handler_name', None)
        handler_package = config.get('handler_package', None)
        if handler_name and handler_package:
            p = Path(__file__).parent / f"{handler_package}.py"
            if p.exists():
                handler_mod = import_module(handler_package)
                handler = getattr(handler_mod,handler_name)
            else:
                logger.error(f"Torrent handler {handler_package} is unavailable")
        else:
            logger.error(f"Torrent handler is unset")
              
    
except:
    cwd = os.getcwd()
    logger.exception(f"Unable to load torrent handler. cwd: {cwd}")


def handleMagnet(uri):
    magnet = None
    try:
        magnet = Magnet.from_string(uri)
    except:
        logger.debug(f"Invalid magnet {uri}", exc_info=1)
        return False
    try:
        return handler(uri)
    except:
        logger.exception(f"Torrent handler error")
        return False

def handleTorrent(r, uri):
    torrent = None
    try:
        torrent = Torrent.read_stream(BytesIO(r.content))
    except:
        logger.debug(f"Invalid torrent {uri}", exc_info=1)
        return False
    try:
        return handler(uri)
    except:
        logger.exception(f"Torrent handler error")
        return False

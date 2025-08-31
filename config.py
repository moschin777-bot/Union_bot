import os, json
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN','').strip()
ADMIN_ID=int(os.getenv('ADMIN_ID','0')) if os.getenv('ADMIN_ID') else None
DEFAULT_CHANNELS={"suppliers":None,"builders":None,"contractors":None,"tenders":None,"machines":None,"logistics":None,"rent":None}
CHANNELS=DEFAULT_CHANNELS.copy()
raw=os.getenv('CHANNELS_JSON','').strip()
if raw:
    try:
        CHANNELS.update(json.loads(raw))
    except:pass

import logging
import os
from datetime import datetime

file_name = f"{datetime.now().strftime('%d_%m_%Y')}.log"
log_path = os.path.join(os.getcwd(), "logs", file_name)
os.makedirs(log_path, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_path, file_name),
    level=logging.INFO,
    format="[%(filename)s - %(message)s - %(lineno)d ]",
)

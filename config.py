import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Params:
    temp_dir: str
    logs_path: str
    headers: dict
    pause_before_request: float
    time_start_script: str
    chrome_driver_path: str
    username: str
    password: str
    chrome_location_path: str


base_dir = Path(__file__).resolve().parent

temp_dir = os.path.join(base_dir, "Temp")
logs_path = os.path.join(base_dir, "logs")
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}
pause_before_request = 0.1
time_start_script = datetime.now().isoformat()
chrome_driver_path = os.path.join(base_dir, "Selenium_Driver\chromedriver.exe")

username = ''
password = ''
chrome_location_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'



params = Params(temp_dir, logs_path, headers, pause_before_request, time_start_script, chrome_driver_path,
                username, password, chrome_location_path)



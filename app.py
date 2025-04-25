from bs4 import BeautifulSoup
import re
import json
from requests import get
import time
from models import initialize_database, save_share_db

initialize_database()
BASE_URIS = [
    "https://www.google.com/finance/quote/{share}:NSE",
    "https://www.google.com/finance/quote/{share}:INDEXBOM",
    "https://www.google.com/finance/quote/{share}:INDEXNSE"
]

def frt_lzero(n:int) -> str:
     return f"{n:03}"

def get_json_data_parsed(share_name, serial):
     for base_uri in BASE_URIS:
          uri = base_uri.format(share=share_name)
          response = get(uri)
          if response.status_code == 200:     
               html_content = response.text
               soup = BeautifulSoup(html_content, "html.parser")
               script_tag = soup.find("script", class_="ds:2")

               if script_tag:
                    script_content = script_tag.string
                    match = re.search(r"AF_initDataCallback\((.*?)\);", script_content, re.DOTALL)
                    if match:
                         data_str = match.group(1)
                         fixed_json = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1"\2":', data_str)
                         fixed_json = fixed_json.replace("'", '"')
                         try:
                              data_json = json.loads(str(fixed_json))
                              try:
                                   share_value = data_json.get("data", [])[0][0][0][5][0]
                                   share_pts = data_json.get("data", [])[0][0][0][5][1]
                                   share_pts = round(share_pts, 2)
                                   G_N_L = "LOSS" if share_pts < 0 else "GAIN"
                                   G_N_L_ = "\033[37;42mGAIN\033[0m" if G_N_L == "GAIN" else "\033[37;41mLOSS\033[0m"
                                   save_share_db(share_name, share_value, share_pts, G_N_L)
                                   # print(f"\033[36m{share_name}\033[0m\t\t\033[33m{share_value}\t\t{share_pts}\t\t{G_N_L}\033[0m Status code: \033[32m{response.status_code}\033[0m")
                                   tabs = "\t\t\t" if len(share_name) <= 9 else "\t\t"
                                   tbn_ = "\t\t" if len(str(share_value)) >= 8 else "\t\t\t"
                                   print(f"[{serial}] \033[30;47m{share_name}\033[0m{tabs}{share_value}{tbn_}{share_pts}\t\t{G_N_L_} Status code: \033[37;44m{response.status_code}\033[0m")

                                   # print(f"Success to fetch data from {uri}\t\tStatus code: \033[32m{response.status_code}\033[0m")
                                   break
                              except (IndexError, TypeError):
                                   pass
                                   # print(f"Failed to extract the value.\t\t\t {data_json}")
                         except json.JSONDecodeError as e:
                              print("JSON Decode Error:", e)
                    else:
                         return "AF_initDataCallback function not found in the script content."
               else:
                    return "Script tag with class 'ds:2' not found."
          else:
               print(f"Failed to fetch data from {uri}\t\t Status code: \033[31m{response.status_code}\033[0m")
     
def data_extracted(data_json):
     try:
          share_value = data_json.get("data", [])[0][0][0][5][0]
          share_pts = data_json.get("data", [])[0][0][0][5][1]
          G_N_L = "LOSS" if share_pts < 0 else "GAIN"
          save_share_db(share_name, share_value, share_pts, G_N_L)
          print("Extracted value:", share_value, share_pts, G_N_L)
     except (IndexError, TypeError):
          print("Failed to extract the value.")

def convert_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"\033[33mTook {minutes} minutes {remaining_seconds:02d} seconds\033[0m"

if __name__=="__main__":
     share_names = ['RELIANCE', 'NIFTYBEES', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TATAELXSI', 'TATACHEM', 'TATACONSUM', 'M&M', 'UNITDSPR', 'BSE', 'COLPAL', 'RELAXO', 'ASALCBR', 'IRCTC', 'PIDILITIND', 'TITAN', 'EICHERMOT', 'HEROMOTOCO', 'BAJAJ-AUTO', 'SENSEX', 'NIFTY_IT', 'INFY', 'TCS', 'TEJASNET', 'WIPRO', 'HCLTECH', 'TECHM', 'KPITTECH', 'CAMS', 'TANLA', 'ANGELONE', 'LTIM', 'ROUTE', 'DIXON', 'LATENTVIEW', 'AFFLE', 'BOSCHLTD', 'MCX', 'BHARTIARTL', 'SONATSOFTW', 'NEWGEN', 'HAPPSTMNDS', 'DEEPAKNTR', 'DEEPAKFERT', 'SRF', 'CHAMBLFERT', 'ROSSARI', 'ALKYLAMINE', 'SUMICHEM', 'AARTIIND', 'VALIANTORG', 'CLEAN', 'SUNPHARMA', 'CIPLA', 'LAURUSLABS', 'IEX', 'MGL', 'HDFCBANK', 'HDFCAMC', 'ICICIBANK', 'SBIN', 'SBICARD', 'KOTAKBANK', 'MUTHOOTFIN', 'BAJAJFINSV', 'CDSL', 'LICHSGFIN', 'LICI', 'HINDALCO', 'BALRAMCHIN', 'ASTRAL', 'PRINCEPIPE', 'UNOMINDA', 'ENDURANCE', 'BERGEPAINT', 'ASIANPAINT', 'ARE&M', 'EXIDEIND', 'VEDL', 'SUPREMEIND', 'HINDUNILVR', 'JUBLFOOD', 'MRF', 'BRITANNIA', 'APOLLOTYRE', 'MARICO', 'HAVELLS', 'ORIENTELEC', 'POLYCAB', 'BAJAJELEC', 'ULTRACEMCO', 'LT', 'NYKAA', 'OLECTRA', 'KAJARIACER', 'NIFTY_50', 'BALKRISIND', 'ANURAS']
     e_ = time.time()
     print(len(share_names))
     serial:int = 1
     for share_name in share_names:
          # print(f"Processing share: {share_name}")
          a_ = get_json_data_parsed(share_name, frt_lzero(serial))
          serial += 1
     f_ = time.time()
     print(convert_seconds(int(f_-e_)))
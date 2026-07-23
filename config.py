import os

# Cấu hình Web
BASE_URL = "https://www.investing.com/news/latest-news"
MAX_PAGES = 3

# Cấu hình Delay (Random Sleep)
MIN_DELAY = 3.0
MAX_DELAY = 6.0

# Cấu hình Trình duyệt
CHROME_VERSION = 150
USER_DATA_DIR = r"D:\Projects\Social listening\SCRAPE DATA\investing_chrome_data"

# Đường dẫn lưu file
OUTPUT_DIR = r"D:\Projects\Social listening\SCRAPE DATA\articles_information"
CSV_FILE = os.path.join(OUTPUT_DIR, "investing_news.csv")
EXCEL_FILE = os.path.join(OUTPUT_DIR, "investing_news.xlsx")
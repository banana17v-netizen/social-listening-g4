import os
import pandas as pd
import config

def save_to_files(data):
    """Kiểm tra thư mục và lưu dữ liệu ra file"""
    if not data:
        print("-> Không có dữ liệu để lưu.")
        return

    # Tự động tạo thư mục nếu chưa có
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)

    df = pd.DataFrame(data)
    
    # Xuất file
    df.to_csv(config.CSV_FILE, index=False, encoding="utf-8-sig")
    df.to_excel(config.EXCEL_FILE, index=False)
    
    print(f"-> Đã lưu thành công {len(data)} bài viết vào:")
    print(f"   + CSV: {config.CSV_FILE}")
    print(f"   + Excel: {config.EXCEL_FILE}")
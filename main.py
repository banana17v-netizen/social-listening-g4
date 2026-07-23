import config
import browser_driver as bd
import parser
import storage

def run():
    driver = bd.init_driver()
    all_news = []

    try:
        # BƯỚC 1: CÀO DANH SÁCH BÀI VIẾT (LISTING)
        print("1. Đang mở trang tin tức Investing.com...")
        driver.get(config.BASE_URL)
        bd.random_sleep(4, 6)
        bd.handle_popups(driver)

        for page in range(1, config.MAX_PAGES + 1):
            print(f"\n--- Đang cào Trang danh mục {page}/{config.MAX_PAGES} ---")
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
            bd.random_sleep(2, 4)

            page_articles = parser.parse_articles_from_html(driver.page_source, page)
            all_news.extend(page_articles)
            print(f"-> Tìm thấy {len(page_articles)} bài từ trang {page}")

            if page < config.MAX_PAGES:
                if bd.click_next_page(driver):
                    print("-> Đã bấm chuyển trang danh mục...")
                    bd.random_sleep(4, 6)
                else:
                    print("-> Hết trang danh mục. Dừng lặp.")
                    break

        # BƯỚC 2: MỞ TỪNG LINK BÀI VIẾT ĐỂ CÀO NỘI DUNG CHI TIẾT (DETAIL)
        print(f"\n======== BẮT ĐẦU CÀO CHI TIẾT {len(all_news)} BÀI BÁO ========")
        
        for idx, item in enumerate(all_news, start=1):
            url = item['URL']
            print(f"[{idx}/{len(all_news)}] Đang cào nội dung: {item['Tiêu đề'][:50]}...")
            
            try:
                driver.get(url)
                # Random sleep để tránh bị Cloudflare phát hiện khi mở nhiều bài viết liên tục
                bd.random_sleep(3, 5) 
                bd.handle_popups(driver)

                # Bóc tách nội dung chi tiết
                full_content = parser.parse_article_detail(driver.page_source)
                item['Nội dung chi tiết'] = full_content
                
            except Exception as e:
                print(f"   Lỗi khi cào bài viết này: {e}")
                item['Nội dung chi tiết'] = "Lỗi khi tải trang bài viết"

        # BƯỚC 3: LƯU TOÀN BỘ DỮ LIỆU RA FILE
        storage.save_to_files(all_news)

    finally:
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == '__main__':
    run()
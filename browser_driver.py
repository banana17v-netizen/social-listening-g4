import time
import random
import undetected_chromedriver as uc
import config

def init_driver():
    """Khởi tạo Undetected Chromedriver"""
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={config.USER_DATA_DIR}")
    driver = uc.Chrome(options=options, version_main=config.CHROME_VERSION)
    return driver

def handle_popups(driver):
    """Tắt Cookie và Popup đăng nhập"""
    try:
        # Tắt Cookie
        driver.execute_script("var btn = document.getElementById('onetrust-accept-btn-handler'); if(btn) btn.click();")
        # Xóa Modal Đăng nhập
        driver.execute_script("""
            document.querySelectorAll('.fadeInOverlay, .modal-backdrop, .GenLightbox').forEach(el => el.remove());
            document.body.style.overflow = 'auto';
        """)
    except Exception:
        pass

def random_sleep(min_s=config.MIN_DELAY, max_s=config.MAX_DELAY):
    """Tạm dừng chương trình thời gian ngẫu nhiên"""
    time.sleep(random.uniform(min_s, max_s))

def click_next_page(driver):
    """Tìm và bấm nút Next Page"""
    return driver.execute_script("""
        var nextBtn = document.querySelector('[data-test="pagination-next-page"]') || 
                       document.querySelector('a[rel="next"]') ||
                       Array.from(document.querySelectorAll('a')).find(el => el.textContent.trim() === 'Next');
        if (nextBtn) {
            nextBtn.scrollIntoView();
            nextBtn.click();
            return true;
        }
        return false;
    """)
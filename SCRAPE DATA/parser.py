from bs4 import BeautifulSoup

def parse_articles_from_html(html_content, page_num):
    """Bóc tách bài viết từ mã nguồn HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article')
    extracted_data = []

    for article in articles:
        title_tag = article.find('a', {'data-test': 'article-title-link'}) or article.find('a', class_=lambda c: c and 'title' in c)
        
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get('href', '')
            if link.startswith('/'):
                link = 'https://www.investing.com' + link
            
            desc_tag = article.find('p')
            description = desc_tag.get_text(strip=True) if desc_tag else ''
            
            time_tag = article.find('time')
            time_str = time_tag.get_text(strip=True) if time_tag else 'N/A'

            extracted_data.append({
                'Trang': page_num,
                'Tiêu đề': title,
                'Mô tả': description,
                'Thời gian': time_str,
                'URL': link
            })

    return extracted_data

def parse_article_detail(html_content):
    """Bóc tách nội dung chi tiết bên trong một bài báo"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Tìm vùng chứa nội dung bài viết trên Investing.com
    # Thường là div chứa class articlePage, WYSIWYG, hoặc data-test="article-body"
    article_body = (
        soup.find('div', {'data-test': 'article-body'}) or 
        soup.find('div', class_=lambda c: c and ('articlePage' in c or 'WYSIWYG' in c or 'article-content' in c)) or
        soup.find('article')
    )
    
    if not article_body:
        return "Không cào được nội dung (Không tìm thấy khung bài viết)"

    # Lấy tất cả các thẻ <p> chứa đoạn văn bản
    paragraphs = article_body.find_all('p')
    
    # Nối các đoạn văn bản lại với nhau thành 1 bài hoàn chỉnh
    full_text_list = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        # Lọc bỏ các đoạn ngắn hoặc quảng cáo rác nếu có
        if text and not text.startswith("Read More:") and not text.startswith("Disclaimer:"):
            full_text_list.append(text)
            
    full_content = "\n\n".join(full_text_list)
    return full_content if full_content else "Không tìm thấy văn bản trong bài viết"
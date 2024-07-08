import fitz  # PyMuPDF
import re


def process_saved_pdf(file_dir):
    if file_dir.endswith(".pdf"):
        pdf_document = fitz.open(file_dir)
        username = extract_chinese_characters(file_dir)
        found_catering = False
        amount = None
        invoice_date = None
        buyer_id = None
        seller_id = None
        has_text = False
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            if page_text.strip():
                has_text = True
            if "餐饮" in page_text or "食品" in page_text:
                found_catering = True
            prices = re.findall(r'¥\s*(\d+\.?\d*)', page_text)
            if prices:
                max_amount = max(float(price) for price in prices)
                if amount is None or max_amount > amount:
                    amount = max_amount
            date = extract_date(page_text)
            if date and date is not None:
                invoice_date = date
            ids = re.findall(r'\b9\w{17}\b', page_text)
            for i, id_ in enumerate(ids):
                if i == 0:
                    buyer_id = id_
                else:
                    seller_id = id_
        if not has_text:
            amount = None
        if isinstance(amount, float) and amount < 5:
            amount = extract_amount_from_filename(file_dir)
        reimbursement_type = "餐饮" if found_catering else "非餐饮"
        return [username, reimbursement_type, amount, invoice_date, buyer_id, seller_id]
    else:
        return [None, None, None, None, None, None]


def extract_chinese_characters(filename):
    return ''.join(re.findall(r'[\u4e00-\u9fff]+', filename))


def extract_date(text):
    date_pattern = r'\d{4}年\d{2}月\d{2}日'
    matches = re.findall(date_pattern, text)
    if matches:
        date_str = matches[-1]
        # 转换为标准日期格式 "YYYY-MM-DD"
        year = date_str[:4]
        month = date_str[5:7]
        day = date_str[8:10]
        standard_date = f"{year}-{month}-{day}"
        return standard_date
    return None


def extract_amount_from_filename(filename):
    # 提取文件名中的数字部分作为金额替代值
    matches = re.findall(r'\d+', filename)
    if matches:
        return float(matches[0])
    return None

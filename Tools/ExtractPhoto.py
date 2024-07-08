import os
import pytesseract
from PIL import Image
import cv2
import re
import numpy as np
import uuid

pytesseract.pytesseract.tesseract_cmd = r"./Tesseract/tesseract.exe"


def process_saved_photo(image_path):
    processed_image = tpys(image_path)
    max_price = None
    is_catering = None
    invoice_date = None
    filtered_ids = None
    if processed_image is not None:
        preprocess_image_path = preprocess_image(processed_image)
        try:
            detected_text = detect_text(preprocess_image_path)
            is_catering, max_price, filtered_ids = extract_text_information(detected_text)
            invoice_date = extract_date(detected_text)
        finally:
            os.remove(preprocess_image_path)
    # ocr_text = detect_text(preprocess_image_path)
    img_filename = image_path[image_path.rfind('/'):]
    username = extract_chinese_characters(img_filename)
    if isinstance(max_price, float) and max_price < 5 or max_price is None:
        max_price = extract_amount_from_filename(img_filename)
    reimbursement_type = "餐饮" if is_catering else "非餐饮"
    if len(filtered_ids) >= 2:
        return [username, reimbursement_type, max_price, invoice_date, filtered_ids[0], filtered_ids[1]]
    elif len(filtered_ids) == 1:
        return [username, reimbursement_type, max_price, invoice_date, filtered_ids[0], None]
    else:
        return [username, reimbursement_type, max_price, invoice_date, None, None]


def tpys(image_path):
    image = read_image_with_chinese_path(image_path)
    gray = image[:, :, 2]
    edges = cv2.Canny(gray, 30, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea, default=None)
    if max_contour is None:
        return None
    (X, Y), radius = cv2.minEnclosingCircle(max_contour)
    corner = [[0, 0, 0]]
    corners = np.zeros((2000, 2))
    j = 0
    for point in max_contour:
        x, y = point[0]
        distance = abs(np.sqrt((x - X) ** 2 + (y - Y) ** 2) - radius)
        if distance <= 20:
            distance2 = 200
            corners[j] = [x, y]
            j += 1
            for i in range(len(corner)):
                x1, y1, distance1 = corner[i]
                distance2 = min(distance2, abs(x - x1) + abs(y - y1))

                if abs(x - x1) + abs(y - y1) < 100 and distance1 > distance:
                    corner[i] = [x, y, distance]
            if distance2 >= 100:
                corner.append([x, y, distance])
    corner = sorted(corner, key=lambda x_: x_[0] + x_[1])
    a, b = corner[2], corner[3]
    if b[0] < a[0]:
        corner[2], corner[3] = corner[3], corner[2]
    corner = sorted(corner, key=lambda x_: x_[0] + x_[1])
    dot = np.array(corner[1:5])
    points1 = np.float32(dot[:, :2])
    x1 = corner[1][0]
    y1 = corner[1][1]
    x2 = corner[2][0]
    y2 = corner[2][1]
    x3 = corner[3][0]
    y3 = corner[3][1]
    distance1 = int(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
    distance2 = int(np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2))
    points2 = np.float32([[x1, y1], [x1, y1 + distance1], [x1 + distance2, y1], [x1 + distance2, y1 + distance1]])
    mat_affine = cv2.getPerspectiveTransform(points1, points2)
    new_img = cv2.warpPerspective(image, mat_affine, (image.shape[1], image.shape[0]))
    return new_img


def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用双边滤波
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    # 应用自适应阈值
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
    unique_filename = f'temp_{uuid.uuid4().hex}.png'
    cv2.imwrite(unique_filename, gray)
    return unique_filename


def extract_chinese_characters(filename):
    return ''.join(re.findall(r'[\u4e00-\u9fff]+', filename))


def read_image_with_chinese_path(file_path):
    image = Image.open(file_path)
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    return image_cv


def extract_text_information(text):
    keyword = "餐饮"
    is_catering = "餐饮" if keyword in text else "非餐饮"
    prices = re.findall(r'¥?(\d+(?:,\d{3})*\.\d{2})', text)
    prices = [float(price.replace(',', '')) for price in prices]
    max_price = max(prices) if prices else None
    ids = re.findall(r'\b\d\w{17}\b', text)
    filtered_ids = [id_ for id_ in ids if id_ != '91310115671143758E']
    return is_catering, max_price, filtered_ids


def extract_amount_from_filename(filename):
    # 提取文件名中的数字部分作为金额替代值
    matches = re.findall(r'\d+', filename)
    if matches:
        return float(matches[0])
    return None


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


def detect_text(image_path):
    img = read_image_with_chinese_path(image_path)
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    return text

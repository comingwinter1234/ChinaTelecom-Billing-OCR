from fastapi import UploadFile
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import insert
from Database.Models import *
from Tools.ExtractPDF import *
from Tools.ExtractOFD import *
from Tools.ExtractPhoto import *
from Tools.DataBaseTools import *


async def save_file(file: UploadFile, user_id: str, save_dir: str) -> str:
    save_file_location = os.path.join(save_dir, user_id, file.filename)
    os.makedirs(os.path.dirname(save_file_location), exist_ok=True)
    with open(save_file_location, "wb") as buffer:
        buffer.write(await file.read())
    return save_file_location


async def process_file(file: UploadFile, user_id: str, conn: Session, temp_dir: str, save_dir: str) -> Dict:
    save_file_location = await save_file(file, user_id, save_dir)
    if file.filename.endswith('.pdf'):
        file_info = process_saved_pdf(file_dir=save_file_location)
    elif file.filename.endswith('.ofd'):
        file_info = process_saved_ofd(file_dir=save_file_location, temp_file_folder=temp_dir)
    elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_info = process_saved_photo(image_path=save_file_location)
    else:
        return {'msg': '上传文件格式不正确，请使用pdf、ofd或图片文件重试'}
    if None in file_info[0:3] or '' in file_info[0:3]:
        return {'msg': '文件识别信息不充分，请重试'}
    query = conn.query(Worker.worker_name).where(get_where_conditions([Worker.worker_name], file_info[0]))
    if len(query.all()) == 0:
        return {'msg': '扫描得到的员工姓名不存在，请重试'}
    query = conn.query(Service.service_name).where(get_where_conditions([Service.service_name], file_info[1]))
    if len(query.all()) == 0:
        return {'msg': '扫描得到的服务类型不存在，请重试'}
    query = conn.query(Service.service_id).where(
        get_where_conditions([Service.service_name], file_info[1]))
    service_info = query.first()
    query = conn.query(ServiceRecord.service_record_id)
    max_id = max([tup[0] for tup in query.all()]) if query.all() else 0
    new_record = {
        'service_record_id': max_id + 1,
        'service_id': service_info[0],
        'service_time': file_info[3],
        'buyer_company': file_info[5],
        'seller_company': file_info[4],
        'worker_id': user_id,
        'cost': file_info[2]
    }
    try:
        conn.execute(insert(ServiceRecord).values(new_record))
        conn.commit()
        return {'msg': '上传成功，数据已录入'}
    except Exception as e:
        return {'msg': f'数据库插入错误: {e}'}


async def upload_files(user_id: str, files: List[UploadFile], conn: Session, temp_dir: str, save_dir: str) -> List[Dict]:
    msg_list = []
    for file in files:
        msg = await process_file(file, user_id, conn, temp_dir, save_dir)
        msg_list.append({file.filename: msg})
    msg_list.append({'final_msg': '数据上传结束'})
    return msg_list

# **ChinaTelecom-Billing-OCR**

## 依赖配置(anaconda虚拟环境以及MySQL)

### Python环境
```
conda create -n fastapi python=3.10
conda activate fastapi
pip install -r requirements.txt
```
### Mysql安装

* 安装Mysql5.77.4.0， 下载地址：https://dev.mysql.com/downloads/installer/

## 项目启动

### 数据库搭建

* 打开Mysql运行createdb.sql

### 服务器启动

* 在项目目录`./Tools/DataBaseTools.py`中修改密码为你自己设置的Mysql本地服务访问密码

* 在项目根目录下打开终端，激活虚拟环境fastapi，输入：

```
uvicorn main:app --reload --port 8080 --host 0.0.0.0
```
* 本机在`http://127.0.0.1:8080/docs`测试后端已有的接口

### 安装Tesseract

* 安装tesseract v5.3.1.20230401到项目根目录，installer下载地址：https://digi.bib.uni-mannheim.de/tesseract/


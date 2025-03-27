from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import random
import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 和风天气API配置
WEATHER_API_KEY = ‘4da911dbf9534137838473f66fcbd2fd’
CITY_ID = os.getenv('CITY_ID', '101010100')  # 默认北京
CITY_NAME = os.getenv('CITY_NAME', '北京')  # 默认城市名称

# 情话列表
LOVE_MESSAGES = [
    "早安！今天也要元气满满哦！",
    "新的一天开始啦，要开开心心的！",
    "今天也要像Hello Kitty一样可爱呢！",
    "愿你的一天都充满粉色泡泡！",
    "今天也要做最可爱的自己！",
    "早安！今天也要保持好心情哦！",
    "新的一天，新的开始，要加油哦！",
    "今天也要像Hello Kitty一样温柔呢！",
    "愿你的一天都充满甜蜜！",
    "早安！今天也要保持微笑哦！"
]

# 获取城市名称
def get_city_name(city_id):
    """根据城市ID获取城市名称"""
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={city_id}&key={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['code'] == '200' and data['location'] and len(data['location']) > 0:
            return data['location'][0]['name']
    except Exception as e:
        print(f"获取城市名称失败: {e}")
    return CITY_NAME  # 返回默认城市名称

# 获取天气数据
def get_weather():
    """获取天气信息"""
    url = f"https://devapi.qweather.com/v7/weather/3d?location={CITY_ID}&key={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['code'] == '200':
            weather = data['daily'][0]
            city_name = get_city_name(CITY_ID)
            return {
                'city': city_name,
                'temp_max': weather['tempMax'],
                'temp_min': weather['tempMin'],
                'text_day': weather['textDay'],
                'text_night': weather['textNight'],
                'date': datetime.now().strftime("%Y年%m月%d日"),
                'love_message': random.choice(LOVE_MESSAGES)
            }
    except Exception as e:
        print(f"获取天气信息失败: {e}")
    return None

# 搜索城市
def search_city(city_name):
    """搜索城市"""
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['code'] == '200' and data['location']:
            return data['location']
    except Exception as e:
        print(f"搜索城市失败: {e}")
    return []

# 保存设置
def save_settings(api_key, city_id, city_name=""):
    """保存设置"""
    with open('.env', 'w') as f:
        f.write(f"WEATHER_API_KEY={api_key}\n")
        f.write(f"CITY_ID={city_id}\n")
        if city_name:
            f.write(f"CITY_NAME={city_name}\n")
    
    global WEATHER_API_KEY, CITY_ID, CITY_NAME
    WEATHER_API_KEY = api_key
    CITY_ID = city_id
    if city_name:
        CITY_NAME = city_name

# 首页路由
@app.route('/')
def index():
    weather_data = get_weather()
    return render_template('index.html', weather=weather_data)

# 设置页面路由
@app.route('/settings')
def settings():
    return render_template('settings.html', api_key=WEATHER_API_KEY, city_id=CITY_ID, city_name=CITY_NAME)

# 保存设置API
@app.route('/save_settings', methods=['POST'])
def save_settings_api():
    data = request.json
    api_key = data.get('api_key', '')
    city_id = data.get('city_id', '')
    city_name = data.get('city_name', '')
    save_settings(api_key, city_id, city_name)
    return jsonify({"status": "success"})

# 搜索城市API
@app.route('/search_city', methods=['POST'])
def search_city_api():
    data = request.json
    city_name = data.get('city_name', '')
    cities = search_city(city_name)
    return jsonify({"cities": cities})

# 更新天气API
@app.route('/update_weather')
def update_weather():
    weather_data = get_weather()
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 

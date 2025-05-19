from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建存储目录
os.makedirs("images", exist_ok=True)
os.makedirs("plans", exist_ok=True)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 启用CORS以允许前端访问

# 加载城市数据
def load_city_data():
    city_data = {}
    try:
        with open("induction.me", "r", encoding="utf-8") as f:
            content = f.read()
            
        current_city = None
        current_category = None
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是新城市
            if not line.startswith("人文景观") and not line.startswith("自然景观") and not line.startswith("饮食文化") and not any(c.isdigit() for c in line):
                current_city = line.replace("：", "").strip()
                if current_city not in city_data:
                    city_data[current_city] = {
                        "人文景观": [], 
                        "自然景观": [], 
                        "饮食文化": []
                    }
            
            # 检查是否是新分类
            elif line.startswith("人文景观"):
                current_category = "人文景观"
            elif line.startswith("自然景观"):
                current_category = "自然景观"
            elif line.startswith("饮食文化"):
                current_category = "饮食文化"
            
            # 处理分类内容
            elif current_city and current_category and "：" not in line:
                items = [item.strip() for item in line.replace("，", ",").split(",")]
                for item in items:
                    if item and not item.isdigit() and item not in city_data[current_city][current_category]:
                        if item.strip():  # 确保不添加空字符串
                            city_data[current_city][current_category].append(item.strip())
    
    except Exception as e:
        logger.error(f"加载城市数据出错: {e}")
        # 如果出错，使用默认数据
        city_data = {
            "北京": {
                "人文景观": ["故宫博物院", "八达岭长城", "颐和园"],
                "自然景观": ["百里画廊", "京东大峡谷", "八达岭国家森林公园"],
                "饮食文化": ["北京烤鸭", "稻香村糕点", "涮羊肉"]
            }
        }
    
    return city_data

# 全局数据
city_data = load_city_data()

# API路由
@app.route('/api/cities', methods=['GET'])
def get_cities():
    """获取所有城市列表"""
    cities = sorted(list(city_data.keys()))
    return jsonify(cities)

@app.route('/api/city/<city>/categories', methods=['GET'])
def get_categories(city):
    """获取指定城市的分类列表"""
    if city not in city_data:
        return jsonify({"error": "城市不存在"}), 404
    return jsonify(list(city_data[city].keys()))

@app.route('/api/city/<city>/category/<category>', methods=['GET'])
def get_subcategories(city, category):
    """获取指定城市和分类的子类别列表"""
    if city not in city_data or category not in city_data[city]:
        return jsonify({"error": "城市或分类不存在"}), 404
    return jsonify(city_data[city][category])

@app.route('/api/generate_plan', methods=['POST'])
def generate_plan():
    """生成旅游规划"""
    data = request.json
    city = data.get('city')
    category = data.get('category')
    subcategory = data.get('subcategory')
    
    if not city or not category or not subcategory:
        return jsonify({"error": "请提供城市、分类和子类别"}), 400
    
    try:
        # 调用AI生成旅游规划
        plan = call_deepseek_api(city, category, subcategory)
        
        # 保存规划
        filename = f"plans/{city}_{category}_{subcategory}规划.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(plan)
        
        return jsonify({"plan": plan, "filename": filename})
    
    except Exception as e:
        logger.error(f"生成规划时出错: {e}")
        return jsonify({"error": f"生成规划时出错: {e}"}), 500

def call_deepseek_api(city, category, subcategory):
    """调用DeepSeek API生成旅游规划"""
    try:
        # 从配置文件中读取API密钥
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        
        prompt = f"""
        请根据以下信息生成一个详细的三天旅游行程规划：
        城市：{city}
        选择的旅游类别：{category}
        特别兴趣点：{subcategory}
        
        请提供一个包含以下内容的旅游规划：
        1. 每天的行程安排（上午、下午、晚上）
        2. 推荐的景点和活动，包括游玩时间
        3. 餐饮推荐，包括当地特色美食
        4. 交通建议
        5. 住宿推荐
        
        格式要求：分三天详细规划，每天的行程清晰列出，内容要丰富实用，使用Markdown格式。
        """
        
        # 如果没有配置API密钥，返回模拟数据
        if not api_key:
            return generate_mock_plan(city, category, subcategory)
        
        # 实际API调用逻辑
        # 使用DeepSeek API生成旅游规划
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            logger.error(f"API调用失败: {response.status_code} - {response.text}")
            return generate_mock_plan(city, category, subcategory)
            
    except Exception as e:
        logger.error(f"生成旅游规划时出错: {e}")
        return generate_mock_plan(city, category, subcategory)

def generate_mock_plan(city, category, subcategory):
    """生成模拟的旅游规划数据"""
    subcategories = city_data.get(city, {}).get(category, [])
    
    return f"""
# {city}三日游 - {category}特色行程

## 第一天

### 上午
- 8:00-9:00 酒店早餐
- 9:30-12:00 游览{subcategory}，这是{city}最著名的{category}之一
  - 推荐在此处停留约2.5小时，可以深入了解当地文化特色

### 下午
- 12:30-13:30 在附近的"老字号餐厅"享用午餐
  - 推荐菜品：当地特色小吃
- 14:00-17:00 参观{city}博物馆
  - 了解{city}的历史文化发展

### 晚上
- 18:00-19:30 在"夜市美食街"品尝当地特色美食
- 20:00-21:30 欣赏{city}夜景
- 22:00 返回酒店休息

## 第二天

### 上午
- 8:00-9:00 酒店早餐
- 9:30-12:00 前往{subcategories[0] if len(subcategories) > 0 else "景点A"}
  - 建议请当地导游讲解，更好地了解当地文化

### 下午
- 12:30-13:30 在"人气餐厅"享用午餐
- 14:00-17:00 游览{subcategories[1] if len(subcategories) > 1 else "景点B"}
  - 这里是{city}的另一处著名{category}

### 晚上
- 18:00-20:00 参加当地文化体验活动
- 20:30 返回酒店休息

## 第三天

### 上午
- 8:00-9:00 酒店早餐
- 9:30-12:00 参观{subcategories[2] if len(subcategories) > 2 else "景点C"}

### 下午
- 12:30-13:30 享用午餐
- 14:00-16:00 购物时间，推荐前往当地特色商业街
- 16:30-18:00 自由活动，可以再次游览最喜欢的景点

### 晚上
- 18:30-20:00 告别晚餐，品尝尚未尝试过的当地美食
- 20:30 返回酒店，准备第二天离开

## 住宿推荐
- 豪华选择：{city}国际大酒店
- 中档选择：{city}舒适酒店
- 经济选择：{city}青年旅舍

## 交通建议
- 市内交通：建议使用地铁或出租车
- 景点间交通：可以使用公共交通或打车，部分景点可步行到达
- 特别提示：周末和节假日期间，部分景点人流量大，建议提前规划行程

## 实用提示
- 最佳旅游季节：春秋两季
- 推荐携带物品：舒适的鞋子、相机、水和零食
- 当地紧急电话：110（警察）、120（救护车）
    """

@app.route('/api/save_plan', methods=['POST'])
def save_plan():
    """保存旅游规划到文件"""
    data = request.json
    plan = data.get('plan')
    city = data.get('city')
    category = data.get('category')
    subcategory = data.get('subcategory')
    
    if not plan or not city or not category or not subcategory:
        return jsonify({"error": "请提供完整信息"}), 400
    
    try:
        # 创建保存目录
        os.makedirs("plans", exist_ok=True)
        
        # 生成文件名
        filename = f"plans/{city}_{category}_{subcategory}规划.md"
        
        # 保存规划
        with open(filename, "w", encoding="utf-8") as f:
            f.write(plan)
        
        return jsonify({"success": True, "filename": filename})
        
    except Exception as e:
        logger.error(f"保存规划时出错: {e}")
        return jsonify({"error": f"保存规划时出错: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000) 
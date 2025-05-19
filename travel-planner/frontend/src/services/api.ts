import axios from 'axios';

// API基础URL，根据环境配置
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001/api';

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 接口类型定义
export interface City {
  id: string;
  name: string;
  image?: string;
  description?: string;
  culturalAttractions?: string[];
  naturalAttractions?: string[];
  foodCulture?: string[];
}

export interface Category {
  id: string;
  name: string;
  icon?: string;
  description?: string;
}

export interface Subcategory {
  id: string;
  name: string;
  description?: string;
}

export interface PlanResponse {
  plan: string;
  filename: string;
}

// DeepSeek API配置
interface DeepSeekConfig {
  apiKey?: string;
  model: string;
  endpoint: string;
}

const deepseekConfig: DeepSeekConfig = {
  model: 'deepseek-chat',
  endpoint: 'https://api.deepseek.com/v1/chat/completions',
};

// 尝试从localStorage读取API密钥
try {
  const savedApiKey = localStorage.getItem('deepseek_api_key');
  if (savedApiKey) {
    deepseekConfig.apiKey = savedApiKey;
  }
} catch (error) {
  console.warn('无法从localStorage读取API密钥');
}

// 获取城市列表
export const getCities = async (): Promise<City[]> => {
  try {
    // 实际API实现
    // const response = await apiClient.get('/cities');
    // return response.data;
    
    // 清除缓存，确保总是获取最新的城市数据
    localStorage.removeItem('cached_cities');
    
    // 模拟数据
    const cities = mockCities();
    
    // 为了调试，输出城市列表
    console.log('模拟城市数据生成完成，共', cities.length, '个城市');
    
    // 缓存城市数据
    localStorage.setItem('cached_cities', JSON.stringify(cities));
    return cities;
  } catch (error) {
    console.error('获取城市列表失败:', error);
    throw error;
  }
};

// 获取城市的旅游类别
export const getCategories = async (cityId: string): Promise<Category[]> => {
  try {
    // 实际API实现
    // const response = await apiClient.get(`/cities/${cityId}/categories`);
    // return response.data;
    
    // 模拟数据
    return mockCategories();
  } catch (error) {
    console.error(`获取${cityId}的旅游类别失败:`, error);
    throw error;
  }
};

// 获取类别的子类别
export const getSubcategories = async (cityId: string, categoryId: string): Promise<Subcategory[]> => {
  try {
    // 实际API实现
    // const response = await apiClient.get(`/cities/${cityId}/categories/${categoryId}/subcategories`);
    // return response.data;
    
    // 模拟数据
    const cityData = await readInductionData();
    const city = cityData.find(c => c.id === cityId || c.name === cityId);
    
    if (city && categoryId === '人文景观') {
      return city.culturalAttractions.map((name, index) => ({
        id: `cultural-${index}`,
        name,
        description: `${city.name}的人文景观 - ${name}`
      }));
    } else if (city && categoryId === '自然景观') {
      return city.naturalAttractions.map((name, index) => ({
        id: `natural-${index}`,
        name,
        description: `${city.name}的自然景观 - ${name}`
      }));
    } else if (city && categoryId === '饮食文化') {
      return city.foodCulture.map((name, index) => ({
        id: `food-${index}`,
        name,
        description: `${city.name}的特色美食 - ${name}`
      }));
    }
    
    return mockSubcategories();
  } catch (error) {
    console.error(`获取${cityId}的${categoryId}子类别失败:`, error);
    throw error;
  }
};

// 生成旅游规划
export const generatePlan = async (
  city: string,
  category: string,
  subcategory: string
): Promise<PlanResponse> => {
  try {
    // 尝试从localStorage获取DeepSeek API密钥
    const apiKey = localStorage.getItem('deepseek_api_key') || '';
    
    // 如果有API密钥，调用DeepSeek API
    if (apiKey) {
      const plan = await callDeepSeekAPI(city, category, subcategory, apiKey);
      const filename = `${city}-${category}-${subcategory}-${Date.now()}.md`;
      return { plan, filename };
    }
    
    // 如果没有API密钥，显示设置提示并使用模拟数据
    console.warn('未设置DeepSeek API密钥，使用模拟数据');
    // 这里模拟API请求延迟
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const filename = `${city}-${category}-${subcategory}-${Date.now()}.md`;
    return {
      plan: mockPlan(city, category, subcategory),
      filename
    };
  } catch (error) {
    console.error('生成旅游规划失败:', error);
    throw error;
  }
};

// 保存DeepSeek API密钥
export const saveApiKey = (apiKey: string): void => {
  try {
    localStorage.setItem('deepseek_api_key', apiKey);
  } catch (error) {
    console.error('保存API密钥失败:', error);
    throw error;
  }
};

// 获取DeepSeek API密钥
export const getApiKey = (): string => {
  try {
    return localStorage.getItem('deepseek_api_key') || '';
  } catch (error) {
    console.error('获取API密钥失败:', error);
    return '';
  }
};

// 调用DeepSeek API生成旅游规划
const callDeepSeekAPI = async (
  city: string,
  category: string,
  subcategory: string,
  apiKey: string
): Promise<string> => {
  try {
    const prompt = `请为我生成一份详细的${city}${category}旅游规划，特别关注${subcategory}。
规划内容需要包括：
1. 行程概览（最佳旅游季节、交通建议等）
2. 三天的详细行程安排（上午、中午、下午、晚上），包括：
   - 推荐景点（包括地址、开放时间、门票信息）
   - 餐饮推荐（当地特色餐厅和招牌菜品）
   - 必做活动和体验
3. 住宿推荐（不同价位的选择）
4. 实用信息（紧急电话、天气提示、当地习俗等）
5. 额外建议和提示

请以Markdown格式输出，使用标题、列表和强调等格式，让规划清晰易读。`;

    const response = await axios.post(
      deepseekConfig.endpoint,
      {
        model: deepseekConfig.model,
        messages: [
          { role: 'system', content: '你是一个专业的旅游规划顾问，擅长生成详细、信息丰富的旅游规划。' },
          { role: 'user', content: prompt }
        ],
        max_tokens: 2000,
        temperature: 0.7,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`
        }
      }
    );

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('调用DeepSeek API失败:', error);
    // 如果API调用失败，返回模拟数据
    return mockPlan(city, category, subcategory);
  }
};

// 保存旅游规划
export const savePlan = async (filename: string, content: string): Promise<void> => {
  try {
    // 实际API实现
    // await apiClient.post('/save-plan', { filename, content });
    
    // 模拟API请求延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 保存到localStorage
    const savedPlans = JSON.parse(localStorage.getItem('saved_plans') || '[]');
    savedPlans.push({ filename, content, saveDate: new Date().toISOString() });
    localStorage.setItem('saved_plans', JSON.stringify(savedPlans));
    
    console.log('规划已保存:', filename);
  } catch (error) {
    console.error('保存旅游规划失败:', error);
    throw error;
  }
};

// 读取induction.me数据（模拟）
const readInductionData = async () => {
  // 这里应该是从文件读取，但前端无法直接读取文件，所以硬编码数据
  const cities = mockCities();
  
  // 为每个城市添加景点数据
  const cityData = cities.map(city => {
    // 默认数据
    const data = {
      ...city,
      culturalAttractions: [] as string[],
      naturalAttractions: [] as string[],
      foodCulture: [] as string[]
    };
    
    // 根据城市ID添加具体数据
    switch(city.id) {
      case 'xian':
        data.culturalAttractions = ['秦始皇兵马俑', '西安城墙', '大明宫国家遗址公园'];
        data.naturalAttractions = ['华山', '钟南山', '太白山'];
        data.foodCulture = ['肉夹馍', '凉皮', '冰峰'];
        break;
      case 'qingdao':
        data.culturalAttractions = ['栈桥', '八大关', '啤酒博物馆'];
        data.naturalAttractions = ['崂山风景区', '小麦岛', '金沙滩'];
        data.foodCulture = ['青岛脂渣', '青岛啤酒', '海肠捞饭'];
        break;
      case 'beijing':
        data.culturalAttractions = ['故宫博物院', '八达岭长城', '颐和园'];
        data.naturalAttractions = ['百里画廊', '京东大峡谷', '八达岭国家森林公园'];
        data.foodCulture = ['北京烤鸭', '稻香村糕点', '涮羊肉'];
        break;
      case 'nanjing':
        data.culturalAttractions = ['中山陵', '夫子庙', '南京博物院'];
        data.naturalAttractions = ['紫金山', '栖霞山', '玄武湖'];
        data.foodCulture = ['盐水鸭', '鸭血粉丝汤', '桂花糖芋苗'];
        break;
      case 'changsha':
        data.culturalAttractions = ['湖南省博物馆', '天心阁', '靖港古镇'];
        data.naturalAttractions = ['岳麓山', '橘子洲', '大围山国家森林公园'];
        data.foodCulture = ['口味虾', '糖油粑粑', '长沙米粉'];
        break;
      case 'chongqing':
        data.culturalAttractions = ['白公馆和渣滓洞', '洪崖洞', '大足石刻'];
        data.naturalAttractions = ['黑山谷', '长江三峡', '武隆喀斯特'];
        data.foodCulture = ['重庆火锅', '重庆烤鱼', '重庆小面'];
        break;
      case 'haerbin':
        data.culturalAttractions = ['圣索菲亚大教堂', '哈尔滨冰雪大世界', '中央大街'];
        data.naturalAttractions = ['太阳岛风景区', '凤凰山国家森林公园', '镜泊湖'];
        data.foodCulture = ['红肠', '马迭尔冰棍', '大列巴'];
        break;
      case 'hangzhou':
        data.culturalAttractions = ['灵隐寺', '南宋御街', '杭州宋城'];
        data.naturalAttractions = ['西湖', '九溪十八涧', '千岛湖'];
        data.foodCulture = ['龙井虾仁', '东坡肉', '叫化鸡'];
        break;
      case 'guizhou':
        data.culturalAttractions = ['青岩古镇', '西江千户苗寨', '肇兴侗寨'];
        data.naturalAttractions = ['黄果树瀑布', '荔波小七孔', '梵净山'];
        data.foodCulture = ['酸汤鱼', '丝娃娃', '花溪牛肉粉'];
        break;
      case 'chengdu':
        data.culturalAttractions = ['武侯祠', '杜甫草堂', '锦里古街'];
        data.naturalAttractions = ['都江堰', '青城山', '西岭雪山'];
        data.foodCulture = ['成都火锅', '担担面', '钟水饺'];
        break;
      case 'lhasa':
        data.culturalAttractions = ['布达拉宫', '大昭寺', '八廓街'];
        data.naturalAttractions = ['纳木错', '羊卓雍措', '念青唐古拉山'];
        data.foodCulture = ['酥油茶', '糌粑', '牦牛肉干'];
        break;
      case 'tianjin':
        data.culturalAttractions = ['古文化街', '五大道', '天津之眼'];
        data.naturalAttractions = ['盘山', '七里海湿地', '蓟州溶洞'];
        data.foodCulture = ['狗不理包子', '煎饼果子', '罾蹦鲤鱼'];
        break;
      case 'shanghai':
        data.culturalAttractions = ['外滩', '东方明珠广播电视', '豫园'];
        data.naturalAttractions = ['佘山国家森林公园', '东滩湿地公园', '辰山植物园'];
        data.foodCulture = ['虾子大乌参', '草头圈子', '南翔小笼包'];
        break;
      case 'guangzhou':
        data.culturalAttractions = ['广州塔', '陈家祠', '黄埔军校旧址'];
        data.naturalAttractions = ['白云山', '莲花山', '从化千泷沟大瀑布'];
        data.foodCulture = ['白切鸡', '烧鹅', '龙虎斗'];
        break;
      case 'huhehaote':
        data.culturalAttractions = ['昭君博物院', '大召寺', '塞上老街'];
        data.naturalAttractions = ['大青山', '哈素海', '敕勒川高山草原'];
        data.foodCulture = ['手把肉', '烤全羊', '烧麦'];
        break;
      case 'hainan':
        data.culturalAttractions = ['海口骑楼老街', '博鳌亚洲论坛永久会址', '东坡书院'];
        data.naturalAttractions = ['三亚亚龙湾', '呀诺达雨林', '五指山'];
        data.foodCulture = ['文昌鸡', '加积鸭', '东山羊'];
        break;
      default:
        break;
    }
    
    return data;
  });
  
  return cityData;
};

// 模拟数据 - 城市列表
const mockCities = (): City[] => {
  // 确保函数始终返回完整列表
  const allCities = [
    { 
      id: 'xian', 
      name: '西安', 
      description: '古都，兵马俑和古城墙的所在地',
      image: 'https://images.unsplash.com/photo-1607478900766-efe13248b125?w=640&q=80'
    },
    { 
      id: 'qingdao', 
      name: '青岛', 
      description: '海滨城市，著名的啤酒和海鲜',
      image: `${window.location.origin}/images/cities/qingdao.jpg`
    },
    { 
      id: 'beijing', 
      name: '北京', 
      description: '中国首都，拥有丰富的历史文化遗产',
      image: `${window.location.origin}/images/cities/beijing.jpg`
    },
    { 
      id: 'nanjing', 
      name: '南京', 
      description: '六朝古都，历史与现代交融的城市',
      image: `${window.location.origin}/images/cities/nanjing.jpg`
    },
    { 
      id: 'changsha', 
      name: '长沙', 
      description: '湖南省会，充满活力的文化名城',
      image: `${window.location.origin}/images/cities/changsha.jpg`
    },
    { 
      id: 'chongqing', 
      name: '重庆', 
      description: '山城、火锅之都，长江上游经济中心',
      image: `${window.location.origin}/images/cities/chongqing.jpg`
    },
    { 
      id: 'haerbin', 
      name: '哈尔滨', 
      description: '冰城，以冰雪文化和俄罗斯风情著称',
      image: `${window.location.origin}/images/cities/haerbin.jpg`
    },
    { 
      id: 'hangzhou', 
      name: '杭州', 
      description: '风景秀丽的城市，以西湖闻名',
      image: `${window.location.origin}/images/cities/hangzhou.jpg`
    },
    { 
      id: 'guizhou', 
      name: '贵州', 
      description: '多彩贵州，自然风光与民族文化的结合',
      image: `${window.location.origin}/images/cities/guizhou.jpg`
    },
    { 
      id: 'chengdu', 
      name: '成都', 
      description: '悠闲的天府之国，美食与大熊猫的家乡',
      image: `${window.location.origin}/images/cities/chengdu.jpg`
    },
    { 
      id: 'lhasa', 
      name: '拉萨', 
      description: '西藏首府，雪域高原上的圣城',
      image: `${window.location.origin}/images/cities/lhasa.jpg`
    },
    { 
      id: 'tianjin', 
      name: '天津', 
      description: '北方港口城市，中西文化交融的城市',
      image: `${window.location.origin}/images/cities/tianjin.jpg`
    },
    { 
      id: 'shanghai', 
      name: '上海', 
      description: '国际化大都市，东方明珠',
      image: `${window.location.origin}/images/cities/shanghai.jpg`
    },
    { 
      id: 'guangzhou', 
      name: '广州', 
      description: '华南地区的经济中心，粤菜美食之都',
      image: `${window.location.origin}/images/cities/guangzhou.jpg`
    },
    { 
      id: 'huhehaote', 
      name: '呼和浩特', 
      description: '内蒙古首府，草原文化与现代城市的融合',
      image: `${window.location.origin}/images/cities/huhehaote.jpg`
    },
    { 
      id: 'hainan', 
      name: '海南', 
      description: '热带海岛省份，阳光沙滩的度假胜地',
      image: `${window.location.origin}/images/cities/hainan.jpg`
    }
  ];
  
  console.log('生成城市列表，总数:', allCities.length);
  // 返回完整城市列表
  return allCities;
};

// 模拟数据 - 旅游类别
const mockCategories = (): Category[] => {
  return [
    { 
      id: 'culture', 
      name: '人文景观', 
      icon: '🏛️', 
      description: '探索历史文化遗迹、博物馆和传统建筑'
    },
    { 
      id: 'nature', 
      name: '自然景观', 
      icon: '🏞️', 
      description: '欣赏山水风光、公园、自然保护区'
    },
    { 
      id: 'food', 
      name: '饮食文化', 
      icon: '🍲', 
      description: '品尝当地特色美食、了解饮食传统'
    }
  ];
};

// 模拟数据 - 子类别
const mockSubcategories = (): Subcategory[] => {
  return [
    { 
      id: 'history', 
      name: '历史古迹', 
      description: '参观著名的历史遗迹和纪念地'
    },
    { 
      id: 'museum', 
      name: '博物馆', 
      description: '探索艺术和历史博物馆'
    },
    { 
      id: 'architecture', 
      name: '传统建筑', 
      description: '欣赏传统风格建筑和街区'
    },
    { 
      id: 'performance', 
      name: '传统表演', 
      description: '观看当地传统文化表演'
    }
  ];
};

// 模拟生成旅游规划
const mockPlan = (city: string, category: string, subcategory: string): string => {
  return `# ${city}${category}旅游规划 - ${subcategory}

## 行程概览

这是一份为期3天的${city}${subcategory}体验之旅。本规划结合了${city}最具特色的${subcategory}景点，为您提供深度的旅游体验。

### 最佳旅游季节
春季(3-5月)和秋季(9-11月)是游览${city}的最佳时节，天气宜人，景色优美。

### 交通建议
- 市内交通：地铁、公交车、出租车都很便捷
- 景点间交通：建议根据距离选择合适的交通方式，部分景点可步行到达

## 第一天

### 上午
- **参观点1**: 详细介绍，包括地址、开放时间、门票信息
- **参观点2**: 详细介绍，包括地址、开放时间、门票信息
- 休息与小吃推荐

### 中午
- **午餐推荐**: 当地特色餐厅，招牌菜品推荐

### 下午
- **参观点3**: 详细介绍，包括地址、开放时间、门票信息
- **参观点4**: 详细介绍，包括地址、开放时间、门票信息

### 晚上
- **晚餐推荐**: 当地特色餐厅，招牌菜品推荐
- **夜间活动**: 夜景观赏点或文化演出

## 第二天

### 上午
- **参观点5**: 详细介绍，包括地址、开放时间、门票信息
- **参观点6**: 详细介绍，包括地址、开放时间、门票信息

### 中午
- **午餐推荐**: 当地特色餐厅，招牌菜品推荐

### 下午
- **参观点7**: 详细介绍，包括地址、开放时间、门票信息
- **参观点8**: 详细介绍，包括地址、开放时间、门票信息

### 晚上
- **晚餐推荐**: 当地特色餐厅，招牌菜品推荐
- **夜间活动**: 夜景观赏点或文化演出

## 第三天

### 上午
- **参观点9**: 详细介绍，包括地址、开放时间、门票信息
- **参观点10**: 详细介绍，包括地址、开放时间、门票信息

### 中午
- **午餐推荐**: 当地特色餐厅，招牌菜品推荐

### 下午
- **参观点11**: 详细介绍，包括地址、开放时间、门票信息
- **纪念品购买建议**: 推荐购买的当地特色商品和购物地点

### 晚上
- **晚餐推荐**: 当地特色餐厅，招牌菜品推荐

## 住宿推荐

1. **豪华选择**: 酒店名称，位置优势，价格范围
2. **中档选择**: 酒店名称，位置优势，价格范围
3. **经济选择**: 酒店名称，位置优势，价格范围

## 实用信息

- **紧急电话**: 120(医疗急救)，110(报警)，119(火警)
- **旅游咨询**: 当地旅游咨询中心地址和电话
- **天气提示**: 季节性天气特点和应对建议
- **当地习俗**: 需要注意的当地习俗和禁忌

## 额外建议

- 建议提前预订热门景点门票和特色餐厅
- 带好防晒和雨具，做好天气变化的准备
- 尊重当地文化和习俗，做一个负责任的旅行者

---

希望这份旅游规划能为您的${city}之行带来愉快的体验！`;
};

// 导出API函数
const apiService = {
  getCities,
  getCategories,
  getSubcategories,
  generatePlan,
  savePlan,
  saveApiKey,
  getApiKey
};

export default apiService;
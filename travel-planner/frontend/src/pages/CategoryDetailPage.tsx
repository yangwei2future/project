import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Row, Col, Card, Typography, Spin, Alert, Empty, Button, List } from 'antd';
import { RightOutlined, AppstoreOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { useAtom } from 'jotai';
import {
  selectedCityAtom,
  selectedCategoryAtom,
  selectedSubcategoryAtom,
} from '../utils/store';
import { getSubcategories, Subcategory } from '../services/api';
import PathNavigation from '../components/PathNavigation';

const { Title, Paragraph } = Typography;
const { Meta } = Card;

const CategoryDetailPage: React.FC = () => {
  const { cityId, categoryId } = useParams<{ cityId: string; categoryId: string }>();
  const [subcategories, setSubcategories] = useState<Subcategory[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const [selectedCity] = useAtom(selectedCityAtom);
  const [selectedCategory] = useAtom(selectedCategoryAtom);
  const [, setSelectedSubcategory] = useAtom(selectedSubcategoryAtom);

  useEffect(() => {
    const fetchSubcategories = async () => {
      try {
        const data = await getSubcategories(cityId || '', categoryId || '');
        setSubcategories(data);
        setLoading(false);
      } catch (error) {
        console.error(`获取${cityId}的${categoryId}子类别列表失败:`, error);
        setError(`获取子类别列表失败，请稍后重试。`);
        setLoading(false);
      }
    };

    fetchSubcategories();
  }, [cityId, categoryId]);

  const handleSubcategorySelect = (subcategory: Subcategory) => {
    setSelectedSubcategory(subcategory.name);
    
    // 保存所有选择的数据，用于生成规划
    localStorage.setItem('planningData', JSON.stringify({
      city: cityId,
      category: categoryId,
      subcategory: subcategory.name
    }));
    
    navigate('/plan');
  };

  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
        <div className="loading-text">正在加载子类别列表...</div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="加载错误"
        description={error}
        type="error"
        showIcon
        style={{ maxWidth: '600px', margin: '0 auto' }}
      />
    );
  }

  return (
    <div className="category-detail-page">
      <PathNavigation
        paths={[
          { name: '首页', path: '/' },
          { name: cityId || '', path: `/city/${cityId}` },
          { name: categoryId || '', path: '' },
        ]}
      />

      <div className="page-title">
        <h1>{cityId} - {categoryId}</h1>
        <p className="subtitle">请选择您感兴趣的具体项目</p>
      </div>

      {subcategories.length === 0 ? (
        <Empty description="暂无子类别数据" />
      ) : (
        <List
          grid={{ gutter: 16, xs: 1, sm: 2, md: 3, lg: 3, xl: 4, xxl: 4 }}
          dataSource={subcategories}
          renderItem={(item) => (
            <List.Item>
              <Card
                hoverable
                className="subcategory-card"
                actions={[
                  <Button
                    type="primary"
                    icon={<ThunderboltOutlined />}
                    onClick={() => handleSubcategorySelect(item)}
                  >
                    生成旅游规划
                  </Button>,
                ]}
              >
                <Card.Meta
                  title={
                    <Typography.Title level={4} style={{ margin: 0 }}>
                      {item.name}
                    </Typography.Title>
                  }
                  description={item.description}
                />
              </Card>
            </List.Item>
          )}
        />
      )}

      <div style={{ marginTop: '40px', background: '#f5f5f5', padding: '20px', borderRadius: '8px' }}>
        <Typography.Title level={3}>选择后将会发生什么？</Typography.Title>
        <Typography.Paragraph>
          选择您感兴趣的子类别后，系统将为您生成一份详细的旅游规划，包括：
        </Typography.Paragraph>
        <ul>
          <li>行程概览（最佳旅游季节、交通建议等）</li>
          <li>三天的详细行程安排，包括景点、餐饮和活动推荐</li>
          <li>住宿推荐（不同价位的选择）</li>
          <li>实用信息（紧急电话、天气提示、当地习俗等）</li>
          <li>额外建议和提示</li>
        </ul>
        <Typography.Paragraph>
          您可以保存、下载或复制这份规划，以便在旅行中随时参考。
        </Typography.Paragraph>
      </div>
    </div>
  );
};

export default CategoryDetailPage; 
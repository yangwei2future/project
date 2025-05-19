import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Row, Col, Card, Typography, Spin, Alert, Empty } from 'antd';
import { EnvironmentOutlined, BankOutlined, ThunderboltOutlined, CoffeeOutlined } from '@ant-design/icons';
import { useAtom } from 'jotai';
import { selectedCityAtom, selectedCategoryAtom } from '../utils/store';
import { getCategories, Category } from '../services/api';
import PathNavigation from '../components/PathNavigation';

const { Title, Paragraph } = Typography;
const { Meta } = Card;

interface CategoryInfo {
  name: string;
  icon: React.ReactNode;
  description: string;
  color: string;
}

const CityDetailPage: React.FC = () => {
  const { cityId } = useParams<{ cityId: string }>();
  const navigate = useNavigate();
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [, setSelectedCity] = useAtom(selectedCityAtom);
  const [, setSelectedCategory] = useAtom(selectedCategoryAtom);

  useEffect(() => {
    if (cityId) {
      setSelectedCity(cityId);
      fetchCategories();
    }
  }, [cityId, setSelectedCity]);

  const fetchCategories = async () => {
    if (!cityId) return;
    
    setLoading(true);
    setError(null);
    try {
      const categoriesData = await getCategories(cityId);
      setCategories(categoriesData);
    } catch (err) {
      setError(`获取${cityId}的分类列表失败，请稍后重试`);
      console.error(`获取${cityId}的分类列表失败:`, err);
    } finally {
      setLoading(false);
    }
  };

  const handleCategorySelect = (category: string) => {
    setSelectedCategory(category);
    navigate(`/city/${cityId}/category/${category}`);
  };

  // 获取分类的信息（图标、描述等）
  const getCategoryInfo = (category: string): CategoryInfo => {
    switch (category) {
      case '人文景观':
        return {
          name: '人文景观',
          icon: <BankOutlined />,
          description: '探索历史文化遗迹和人文景点',
          color: '#3498db'
        };
      case '自然景观':
        return {
          name: '自然景观',
          icon: <EnvironmentOutlined />,
          description: '领略壮美自然风光和地理奇观',
          color: '#2ecc71'
        };
      case '饮食文化':
        return {
          name: '饮食文化',
          icon: <CoffeeOutlined />,
          description: '品尝当地特色美食和餐饮文化',
          color: '#e74c3c'
        };
      default:
        return {
          name: category,
          icon: <ThunderboltOutlined />,
          description: '探索更多城市特色',
          color: '#9b59b6'
        };
    }
  };

  return (
    <div className="city-detail-page">
      <PathNavigation
        paths={[
          { name: cityId || '城市', path: cityId ? `/city/${cityId}` : undefined }
        ]}
      />

      <div className="page-title">
        <Title level={1}>{cityId} · 旅游规划</Title>
        <Paragraph className="subtitle">请选择您在{cityId}感兴趣的旅游类别</Paragraph>
      </div>

      {loading ? (
        <div className="loading-container">
          <Spin size="large" />
          <div className="loading-text">正在加载{cityId}的旅游类别...</div>
        </div>
      ) : error ? (
        <Alert
          message="加载出错"
          description={error}
          type="error"
          showIcon
          style={{ maxWidth: '600px', margin: '20px auto' }}
        />
      ) : categories.length === 0 ? (
        <Empty
          description={`暂无${cityId}的旅游类别数据`}
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        />
      ) : (
        <Row gutter={[24, 24]} justify="center">
          {categories.map((category) => {
            const categoryInfo = getCategoryInfo(category.name);
            return (
              <Col xs={24} sm={24} md={8} key={category.id}>
                <Card
                  hoverable
                  className="category-card"
                  onClick={() => handleCategorySelect(category.name)}
                  style={{ textAlign: 'center', height: '100%' }}
                >
                  <div style={{
                    fontSize: '48px',
                    marginBottom: '20px',
                    color: categoryInfo.color
                  }}>
                    {categoryInfo.icon}
                  </div>
                  <Meta
                    title={<span style={{ fontSize: '18px' }}>{categoryInfo.name}</span>}
                    description={<span>{category.description || categoryInfo.description}</span>}
                  />
                </Card>
              </Col>
            );
          })}
        </Row>
      )}

      <div style={{
        margin: '40px 0',
        padding: '20px',
        background: '#f9f9f9',
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <Title level={4}>{cityId}旅游贴士</Title>
        <Paragraph>
          选择您最感兴趣的旅游类别，我们将为您提供更具体的景点推荐和旅游规划建议。
          根据您的选择，我们会生成包含行程安排、景点介绍、餐饮推荐等内容的详细旅游规划。
        </Paragraph>
      </div>
    </div>
  );
};

export default CityDetailPage; 
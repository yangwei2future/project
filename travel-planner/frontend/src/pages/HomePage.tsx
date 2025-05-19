import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Row, Col, Typography, Spin, Alert, Empty } from 'antd';
import { useAtom } from 'jotai';
import { selectedCityAtom } from '../utils/store';
import { getCities, City } from '../services/api';
import CityCard from '../components/CityCard';

const { Title, Paragraph } = Typography;

const HomePage: React.FC = () => {
  const [cities, setCities] = useState<City[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const [, setSelectedCity] = useAtom(selectedCityAtom);

  useEffect(() => {
    const fetchCities = async () => {
      try {
        const data = await getCities();
        console.log('获取到城市数量:', data.length, data);
        setCities(data);
        setLoading(false);
      } catch (error) {
        console.error('获取城市列表失败:', error);
        setError('获取城市列表失败，请稍后重试。');
        setLoading(false);
      }
    };

    fetchCities();
  }, []);

  const handleCitySelect = (city: City) => {
    setSelectedCity(city.id);
    navigate(`/city/${city.id}`);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
        <div className="loading-text">正在加载城市列表...</div>
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
    <div className="home-page">
      <div className="page-title" style={{ textAlign: 'center', marginBottom: '40px' }}>
        <Title level={1} style={{ color: '#3498db' }}>旅游规划生成器</Title>
        <Paragraph className="subtitle">
          选择一个城市开始您的旅程规划，我们将为您定制专属旅游方案
        </Paragraph>
        <Paragraph>
          显示城市数量: {cities.length}
        </Paragraph>
      </div>

      {cities.length === 0 ? (
        <Empty
          description="暂无可选城市数据"
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        />
      ) : (
        <Row gutter={[24, 24]} justify="center">
          {cities.map((city) => (
            <Col xs={24} sm={12} md={8} lg={6} key={city.id}>
              <CityCard city={city} onClick={handleCitySelect} />
            </Col>
          ))}
        </Row>
      )}

      <div style={{ 
        textAlign: 'center', 
        margin: '40px 0', 
        padding: '20px', 
        background: '#f9f9f9', 
        borderRadius: '8px' 
      }}>
        <Title level={4}>如何使用</Title>
        <Row gutter={[24, 24]} style={{ maxWidth: '900px', margin: '0 auto' }}>
          <Col xs={24} md={8}>
            <div style={{ padding: '16px' }}>
              <div style={{ fontSize: '24px', marginBottom: '12px' }}>1</div>
              <Paragraph>选择您想要旅游的城市</Paragraph>
            </div>
          </Col>
          <Col xs={24} md={8}>
            <div style={{ padding: '16px' }}>
              <div style={{ fontSize: '24px', marginBottom: '12px' }}>2</div>
              <Paragraph>选择感兴趣的旅游类别和特色景点</Paragraph>
            </div>
          </Col>
          <Col xs={24} md={8}>
            <div style={{ padding: '16px' }}>
              <div style={{ fontSize: '24px', marginBottom: '12px' }}>3</div>
              <Paragraph>获取AI生成的个性化旅游规划</Paragraph>
            </div>
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default HomePage; 
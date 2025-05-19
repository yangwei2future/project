import React, { useState } from 'react';
import { Card, Typography } from 'antd';
import { CompassOutlined } from '@ant-design/icons';
import { City } from '../services/api';

const { Meta } = Card;
const { Text } = Typography;

interface CityCardProps {
  city: City;
  onClick: (city: City) => void;
}

const CityCard: React.FC<CityCardProps> = ({ city, onClick }) => {
  const [imageError, setImageError] = useState(false);

  const handleImageError = () => {
    console.error(`图片加载失败: ${city.id}`);
    setImageError(true);
  };

  const getImageUrl = () => {
    if (city.image && city.image.startsWith('http')) {
      return city.image;
    }
    return `${window.location.origin}/images/cities/${city.id}.jpg`;
  };

  const renderImage = () => {
    if (imageError) {
      return (
        <div 
          style={{
            height: '180px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#e6f7ff',
            flexDirection: 'column',
          }}
        >
          <CompassOutlined style={{ color: '#3498db', fontSize: '60px' }} />
          <Text type="secondary" style={{ marginTop: '8px', fontSize: '14px' }}>
            {city.name}
          </Text>
        </div>
      );
    }

    return (
      <img
        alt={city.name}
        src={getImageUrl()}
        className="card-image"
        onError={handleImageError}
        style={{ height: '180px', objectFit: 'cover', width: '100%' }}
      />
    );
  };

  return (
    <Card
      hoverable
      className="city-card"
      cover={renderImage()}
      onClick={() => onClick(city)}
    >
      <Meta 
        title={city.name} 
        description={city.description || "点击探索这座城市"}
        style={{ textAlign: 'center' }} 
      />
    </Card>
  );
};

export default CityCard; 
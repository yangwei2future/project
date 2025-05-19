import React from 'react';
import { Layout, Typography, Button } from 'antd';
import { HomeFilled } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAtom } from 'jotai';
import { resetSelectionsAtom } from '../utils/store';

const { Header } = Layout;
const { Title } = Typography;

const AppHeader: React.FC = () => {
  const navigate = useNavigate();
  const [, resetAll] = useAtom(resetSelectionsAtom);

  const handleLogoClick = () => {
    resetAll();
    navigate('/');
  };

  return (
    <Header style={{ 
      background: '#fff', 
      padding: '0 24px',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)',
      height: '64px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <div 
        style={{ 
          display: 'flex', 
          alignItems: 'center',
          cursor: 'pointer'
        }}
        onClick={handleLogoClick}
      >
        <HomeFilled style={{ fontSize: '24px', color: '#3498db', marginRight: '12px' }} />
        <Title level={3} style={{ margin: 0, color: '#3498db' }}>
          旅游规划生成器
        </Title>
      </div>
      
      <Button 
        type="text" 
        size="large"
        onClick={handleLogoClick}
      >
        返回首页
      </Button>
    </Header>
  );
};

export default AppHeader; 
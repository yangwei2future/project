import React from 'react';
import { Layout, Typography } from 'antd';

const { Footer } = Layout;
const { Text } = Typography;

const AppFooter: React.FC = () => {
  return (
    <Footer style={{ 
      textAlign: 'center',
      background: '#f5f7fa',
      padding: '24px',
      borderTop: '1px solid #e8e8e8'
    }}>
      <Text style={{ color: 'rgba(0, 0, 0, 0.45)' }}>
        © {new Date().getFullYear()} 旅游规划生成器 - 使用AI技术定制您的旅行计划
      </Text>
    </Footer>
  );
};

export default AppFooter; 
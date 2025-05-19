import React from 'react';
import { Breadcrumb } from 'antd';
import { HomeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

interface PathNavigationProps {
  paths: {
    name: string;
    path?: string;
  }[];
}

const PathNavigation: React.FC<PathNavigationProps> = ({ paths }) => {
  const navigate = useNavigate();

  const handleClick = (path?: string) => {
    if (path) {
      navigate(path);
    }
  };

  return (
    <Breadcrumb
      className="path-navigation"
      items={[
        {
          title: (
            <span onClick={() => handleClick('/')} style={{ cursor: 'pointer' }}>
              <HomeOutlined /> 首页
            </span>
          ),
        },
        ...paths.map((item, index) => ({
          title: (
            <span
              onClick={() => item.path && handleClick(item.path)}
              style={{ cursor: item.path ? 'pointer' : 'default' }}
            >
              {item.name}
            </span>
          ),
        })),
      ]}
    />
  );
};

export default PathNavigation; 
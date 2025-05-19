import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, Button, Tooltip } from 'antd';
import { SettingOutlined } from '@ant-design/icons';
import { Provider } from 'jotai';
import './App.css';

// 导入组件
import AppHeader from './components/AppHeader';
import AppFooter from './components/AppFooter';
import HomePage from './pages/HomePage';
import CityDetailPage from './pages/CityDetailPage';
import CategoryDetailPage from './pages/CategoryDetailPage';
import PlanningPage from './pages/PlanningPage';
import ResultPage from './pages/ResultPage';
import ApiKeySetting from './components/ApiKeySetting';

const { Content } = Layout;

const App: React.FC = () => {
  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);

  return (
    <Provider>
      <Router>
        <Layout className="app-layout">
          <AppHeader />
          <Content className="app-content">
            <Tooltip title="设置API密钥">
              <Button
                type="text"
                icon={<SettingOutlined />}
                style={{ position: 'fixed', right: 20, top: 70, zIndex: 1000 }}
                onClick={() => setIsApiKeyModalOpen(true)}
              />
            </Tooltip>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/city/:cityId" element={<CityDetailPage />} />
              <Route path="/city/:cityId/category/:categoryId" element={<CategoryDetailPage />} />
              <Route path="/plan" element={<PlanningPage />} />
              <Route path="/result" element={<ResultPage />} />
            </Routes>
          </Content>
          <AppFooter />
          <ApiKeySetting 
            isOpen={isApiKeyModalOpen} 
            onClose={() => setIsApiKeyModalOpen(false)} 
          />
        </Layout>
      </Router>
    </Provider>
  );
};

export default App;

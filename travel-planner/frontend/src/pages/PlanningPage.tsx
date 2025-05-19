import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Button, Progress, Steps, Typography, Space, Alert, Card, Result } from 'antd';
import { LoadingOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { useAtom } from 'jotai';
import { selectedCityAtom, selectedCategoryAtom, selectedSubcategoryAtom, planResultAtom } from '../utils/store';
import { generatePlan, getApiKey } from '../services/api';

const { Title, Paragraph, Text } = Typography;
const { Step } = Steps;

const PlanningPage: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [planResult, setPlanResult] = useAtom(planResultAtom);
  const navigate = useNavigate();
  
  // 从localStorage获取规划数据
  const getPlanningData = () => {
    const planningDataStr = localStorage.getItem('planningData');
    if (!planningDataStr) {
      return { city: '', category: '', subcategory: '' };
    }
    try {
      return JSON.parse(planningDataStr);
    } catch (error) {
      console.error('解析planningData失败:', error);
      return { city: '', category: '', subcategory: '' };
    }
  };
  
  const planningData = getPlanningData();
  const city = planningData.city;
  const category = planningData.category;
  const subcategory = planningData.subcategory;

  // 检查是否设置了API密钥
  const hasApiKey = !!getApiKey();

  // 生成步骤
  const steps = [
    { title: '准备数据', description: '准备生成旅游规划所需的数据' },
    { title: '分析偏好', description: '分析您的旅游偏好' },
    { title: '生成规划', description: '生成个性化旅游规划' },
    { title: '完成', description: '旅游规划生成完成' },
  ];

  // 生成旅游规划
  const generateTravelPlan = async () => {
    if (!city || !category || !subcategory) {
      setError('缺少必要的规划数据，请返回重新选择');
      setLoading(false);
      return;
    }

    try {
      // 更新进度
      setCurrentStep(0);
      setProgress(10);
      await delay(1000);
      
      setCurrentStep(1);
      setProgress(30);
      await delay(1500);
      
      setCurrentStep(2);
      setProgress(60);
      
      // 调用API生成规划
      const response = await generatePlan(city, category, subcategory);
      
      // 保存规划结果
      setPlanResult({
        city,
        category,
        subcategory,
        plan: response.plan,
        filename: response.filename
      });
      
      setProgress(100);
      setCurrentStep(3);
      await delay(1000);
      
      // 导航到结果页面
      navigate('/result');
    } catch (error) {
      console.error('生成旅游规划失败:', error);
      setError('生成旅游规划失败，请稍后重试');
      setLoading(false);
    }
  };

  // 取消生成
  const handleCancel = () => {
    navigate(-1);
  };

  // 辅助函数：延迟
  const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

  useEffect(() => {
    // 生成规划
    generateTravelPlan();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (error) {
    return (
      <Result
        status="error"
        title="生成失败"
        subTitle={error}
        extra={[
          <Button type="primary" key="back" onClick={() => navigate(-1)}>
            返回
          </Button>,
          <Button key="retry" onClick={() => window.location.reload()}>
            重试
          </Button>,
        ]}
      />
    );
  }

  return (
    <div className="planning-page" style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <Title level={2} style={{ textAlign: 'center', marginBottom: '30px' }}>
        正在生成您的旅游规划
      </Title>

      {!hasApiKey && (
        <Alert
          message="未设置DeepSeek API密钥"
          description="您尚未设置DeepSeek API密钥，系统将使用模拟数据生成规划。如需使用真实数据，请点击右上角的设置按钮配置API密钥。"
          type="warning"
          showIcon
          style={{ marginBottom: '20px' }}
        />
      )}

      <Card style={{ marginBottom: '30px' }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
            <Text strong>城市:</Text>
            <Text>{city}</Text>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
            <Text strong>类别:</Text>
            <Text>{category}</Text>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <Text strong>子类别:</Text>
            <Text>{subcategory}</Text>
          </div>
        </Space>
      </Card>

      <Progress percent={progress} status="active" style={{ marginBottom: '30px' }} />

      <Steps
        current={currentStep}
        direction="vertical"
        className="progress-steps"
        style={{ marginBottom: '30px' }}
      >
        {steps.map((step, index) => {
          let icon = null;
          if (index === currentStep) {
            icon = <LoadingOutlined />;
          } else if (index < currentStep) {
            icon = <CheckCircleOutlined />;
          }
          return (
            <Step
              key={step.title}
              title={step.title}
              description={step.description}
              icon={icon}
            />
          );
        })}
      </Steps>

      <div style={{ textAlign: 'center' }}>
        <Button onClick={handleCancel} disabled={progress >= 100}>
          取消
        </Button>
      </div>
    </div>
  );
};

export default PlanningPage; 
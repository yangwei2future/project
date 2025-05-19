import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Typography, Button, Card, message, Divider, Space, Alert } from 'antd';
import { DownloadOutlined, CopyOutlined, SaveOutlined, HomeOutlined } from '@ant-design/icons';
import { useAtom } from 'jotai';
import { planResultAtom, resetSelectionsAtom } from '../utils/store';
import { savePlan } from '../services/api';
import ReactMarkdown from 'react-markdown';
import PathNavigation from '../components/PathNavigation';

const { Title, Paragraph } = Typography;

const ResultPage: React.FC = () => {
  const [planResult] = useAtom(planResultAtom);
  const [, resetSelections] = useAtom(resetSelectionsAtom);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const navigate = useNavigate();

  // 如果没有规划数据，跳转到首页
  if (!planResult) {
    return (
      <Alert
        message="未找到规划数据"
        description="未找到旅游规划数据，请重新开始规划"
        type="error"
        showIcon
        action={
          <Button type="primary" onClick={() => navigate('/')}>
            返回首页
          </Button>
        }
      />
    );
  }

  const { city, category, subcategory, plan, filename } = planResult;

  // 复制规划内容
  const handleCopy = () => {
    navigator.clipboard.writeText(plan).then(
      () => {
        message.success('规划内容已复制到剪贴板');
      },
      (err) => {
        console.error('复制失败:', err);
        message.error('复制失败，请手动复制');
      }
    );
  };

  // 下载规划文件
  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([plan], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    message.success('规划已下载');
  };

  // 保存规划
  const handleSave = async () => {
    setIsSaving(true);
    try {
      await savePlan(filename, plan);
      message.success('规划已保存');
    } catch (error) {
      console.error('保存规划失败:', error);
      message.error('保存规划失败');
    } finally {
      setIsSaving(false);
    }
  };

  // 返回首页
  const handleBackToHome = () => {
    resetSelections();
    navigate('/');
  };

  return (
    <div className="result-page">
      <PathNavigation
        paths={[
          { name: '首页', path: '/' },
          { name: city, path: `/city/${city}` },
          { name: category, path: `/city/${city}/category/${category}` },
          { name: '规划结果', path: '' },
        ]}
      />

      <div className="page-title">
        <Title level={2}>{city} {category} 旅游规划 - {subcategory}</Title>
        <Paragraph className="subtitle">
          您的个性化旅游规划已生成，您可以下载、复制或保存此规划
        </Paragraph>
      </div>

      <Space direction="vertical" style={{ width: '100%', marginBottom: '20px' }}>
        <Card>
          <div className="action-buttons" style={{ marginBottom: '20px' }}>
            <Space>
              <Button
                type="primary"
                icon={<DownloadOutlined />}
                onClick={handleDownload}
              >
                下载规划
              </Button>
              <Button icon={<CopyOutlined />} onClick={handleCopy}>
                复制内容
              </Button>
              <Button
                icon={<SaveOutlined />}
                onClick={handleSave}
                loading={isSaving}
              >
                保存规划
              </Button>
              <Button
                type="default"
                icon={<HomeOutlined />}
                onClick={handleBackToHome}
              >
                返回首页
              </Button>
            </Space>
          </div>

          <Divider />

          <div className="markdown-content">
            <ReactMarkdown>{plan}</ReactMarkdown>
          </div>
        </Card>
      </Space>
    </div>
  );
};

export default ResultPage;
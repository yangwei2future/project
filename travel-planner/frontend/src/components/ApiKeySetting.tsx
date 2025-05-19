import React, { useState, useEffect } from 'react';
import { Modal, Input, Button, message, Space, Typography } from 'antd';
import { KeyOutlined, SaveOutlined, CloseOutlined } from '@ant-design/icons';
import apiService from '../services/api';

const { Text, Title } = Typography;

interface ApiKeySettingProps {
  isOpen: boolean;
  onClose: () => void;
}

const ApiKeySetting: React.FC<ApiKeySettingProps> = ({ isOpen, onClose }) => {
  const [apiKey, setApiKey] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    // 获取已保存的API密钥
    const savedApiKey = apiService.getApiKey();
    setApiKey(savedApiKey);
  }, [isOpen]);

  const handleSave = () => {
    setIsLoading(true);
    try {
      apiService.saveApiKey(apiKey);
      message.success('API密钥已保存');
      setIsLoading(false);
      onClose();
    } catch (error) {
      console.error('保存API密钥失败:', error);
      message.error('保存API密钥失败');
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setApiKey('');
    apiService.saveApiKey('');
    message.info('API密钥已清除');
  };

  return (
    <Modal
      title={
        <Space>
          <KeyOutlined />
          <span>设置DeepSeek API密钥</span>
        </Space>
      }
      open={isOpen}
      onCancel={onClose}
      footer={[
        <Button key="clear" icon={<CloseOutlined />} onClick={handleClear}>
          清除密钥
        </Button>,
        <Button key="cancel" onClick={onClose}>
          取消
        </Button>,
        <Button
          key="save"
          type="primary"
          icon={<SaveOutlined />}
          loading={isLoading}
          onClick={handleSave}
        >
          保存
        </Button>,
      ]}
      width={600}
    >
      <div style={{ marginBottom: 20 }}>
        <Title level={5}>什么是DeepSeek API密钥？</Title>
        <Text>
          DeepSeek API密钥用于生成个性化的旅游规划。没有API密钥，系统将使用模拟数据。
        </Text>
      </div>

      <div style={{ marginBottom: 20 }}>
        <Title level={5}>如何获取API密钥</Title>
        <Text>
          1. 访问 <a href="https://deepseek.com" target="_blank" rel="noopener noreferrer">DeepSeek官网</a><br />
          2. 注册并登录您的账户<br />
          3. 在账户设置中找到API密钥选项<br />
          4. 创建新的API密钥并复制<br />
        </Text>
      </div>

      <div>
        <Title level={5}>输入您的API密钥</Title>
        <Input.Password
          placeholder="输入DeepSeek API密钥"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          style={{ marginBottom: 10 }}
        />
        <Text type="secondary">
          注意：API密钥将存储在浏览器的本地存储中，不会发送到其他服务器。
        </Text>
      </div>
    </Modal>
  );
};

export default ApiKeySetting; 
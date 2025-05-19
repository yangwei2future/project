/**
 * 简单的Markdown解析器
 * 用于在前端解析和显示旅游规划的Markdown文本
 */

interface MarkdownElement {
  type: 'h1' | 'h2' | 'h3' | 'paragraph' | 'list-item' | 'list-item-nested';
  content: string;
  level?: number;
}

/**
 * 解析Markdown文本为结构化数据
 * @param text Markdown格式的文本
 * @returns 解析后的结构化数据数组
 */
export const parseMarkdown = (text: string): MarkdownElement[] => {
  const lines = text.split('\n');
  const elements: MarkdownElement[] = [];

  for (const line of lines) {
    const trimmedLine = line.trim();
    
    if (!trimmedLine) continue; // 跳过空行
    
    if (trimmedLine.startsWith('# ')) {
      elements.push({
        type: 'h1',
        content: trimmedLine.substring(2).trim(),
      });
    } else if (trimmedLine.startsWith('## ')) {
      elements.push({
        type: 'h2',
        content: trimmedLine.substring(3).trim(),
      });
    } else if (trimmedLine.startsWith('### ')) {
      elements.push({
        type: 'h3',
        content: trimmedLine.substring(4).trim(),
      });
    } else if (trimmedLine.startsWith('- ')) {
      elements.push({
        type: 'list-item',
        content: trimmedLine.substring(2).trim(),
      });
    } else if (trimmedLine.startsWith('  - ')) {
      elements.push({
        type: 'list-item-nested',
        content: trimmedLine.substring(4).trim(),
      });
    } else {
      elements.push({
        type: 'paragraph',
        content: trimmedLine,
      });
    }
  }

  return elements;
};

/**
 * 将Markdown内容按照部分进行分组
 * 例如，将第一天、第二天、第三天的内容分组
 * @param elements 解析后的Markdown元素数组
 * @returns 分组后的数据，键为标题，值为该标题下的内容元素
 */
export const groupBySection = (elements: MarkdownElement[]): Record<string, MarkdownElement[]> => {
  const sections: Record<string, MarkdownElement[]> = {};
  let currentSection = '默认';
  
  for (const element of elements) {
    if (element.type === 'h2') {
      currentSection = element.content;
      if (!sections[currentSection]) {
        sections[currentSection] = [];
      }
      sections[currentSection].push(element);
    } else {
      if (!sections[currentSection]) {
        sections[currentSection] = [];
      }
      sections[currentSection].push(element);
    }
  }
  
  return sections;
};

export default {
  parseMarkdown,
  groupBySection,
}; 
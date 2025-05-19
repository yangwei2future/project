import { atom } from 'jotai';

// 用户选择的城市名称
export const selectedCityAtom = atom<string | null>(null);

// 用户选择的分类名称
export const selectedCategoryAtom = atom<string | null>(null);

// 用户选择的子类别名称
export const selectedSubcategoryAtom = atom<string | null>(null);

// 导航历史记录
export const navigationHistoryAtom = atom<string[]>([]);

// 规划结果
export interface PlanResultData {
  city: string;
  category: string;
  subcategory: string;
  plan: string;
  filename: string;
}

export const planResultAtom = atom<PlanResultData | null>(null);

// 加载状态
export const loadingAtom = atom<boolean>(false);

// 错误信息
export const errorMessageAtom = atom<string | null>(null);

// 生成的旅游规划文件名
export const planFilenameAtom = atom<string | null>(null);

// 重置所有状态
export const resetSelectionsAtom = atom(
  null, // 读取时不做任何事
  (_get: any, set: any) => {
    set(selectedCityAtom, null);
    set(selectedCategoryAtom, null);
    set(selectedSubcategoryAtom, null);
    set(planResultAtom, null);
    set(errorMessageAtom, null);
    set(navigationHistoryAtom, []);
    set(planFilenameAtom, null);
  }
);

// 添加导航历史
export const addNavigationHistoryAtom = atom(
  null,
  (get: any, set: any, newPath: string) => {
    const history = [...get(navigationHistoryAtom)];
    // 防止重复添加相同路径
    if (history[history.length - 1] !== newPath) {
      history.push(newPath);
      set(navigationHistoryAtom, history);
    }
  }
);

// 返回上一页
export const goBackAtom = atom(
  null,
  (get: any, set: any) => {
    const history = [...get(navigationHistoryAtom)];
    if (history.length > 1) {
      // 移除当前路径
      history.pop();
      set(navigationHistoryAtom, history);
      return history[history.length - 1]; // 返回新的当前路径
    }
    return null; // 如果没有历史记录可以回退，返回null
  }
); 
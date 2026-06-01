import { create } from 'zustand';

export interface ExpenseItem {
  id: string;
  title: string;
  amount: number;
  category: 'Food' | 'Shopping' | 'Transport' | 'Subscriptions' | 'Entertainment' | 'Other';
  date: string;
}

export interface BudgetCategory {
  name: 'Food' | 'Shopping' | 'Transport' | 'Subscriptions' | 'Entertainment' | 'Other';
  spent: number;
  budget: number;
  color: string;
}

export interface Goal {
  id: string;
  name: string;
  current: number;
  target: number;
  daysLeft: number;
  status: 'On track' | 'At risk' | 'Overspent';
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
}

interface DashboardState {
  // KPI Totals
  netWorth: number;
  netWorthTrend: string;
  saved: number;
  savedTarget: number;
  stressScore: number;
  stressLevel: string;
  
  // Lists
  expenses: ExpenseItem[];
  budgets: Record<string, BudgetCategory>;
  goals: Goal[];
  alerts: { id: string; type: 'danger' | 'warning' | 'success' | 'info'; text: string }[];
  chatMessages: ChatMessage[];
  chatInput: string;
  activeTab: 'Dashboard' | 'Expenses' | 'Goals' | 'Insights' | 'AI Coach';
  
  // Actions
  addExpense: (expense: Omit<ExpenseItem, 'id' | 'date'>) => void;
  deleteExpense: (id: string) => void;
  setChatInput: (text: string) => void;
  sendChatMessage: (text?: string) => void;
  setActiveTab: (tab: 'Dashboard' | 'Expenses' | 'Goals' | 'Insights' | 'AI Coach') => void;
  triggerAICoachQuestion: (question: string) => void;
  clearAllData: () => void;
}

const initialExpenses: ExpenseItem[] = [
  { id: 'exp-1', title: 'Weekly Groceries', amount: 2200, category: 'Food', date: '2026-06-01' },
  { id: 'exp-2', title: 'Zomato Delivery', amount: 2000, category: 'Food', date: '2026-05-31' },
  { id: 'exp-3', title: 'Zara Summer Collection', amount: 6100, category: 'Shopping', date: '2026-05-30' },
  { id: 'exp-4', title: 'Uber Taxi to Office', amount: 1800, category: 'Transport', date: '2026-05-29' },
  { id: 'exp-5', title: 'Auto Fare', amount: 1000, category: 'Transport', date: '2026-05-28' },
  { id: 'exp-6', title: 'Netflix Subscription', amount: 890, category: 'Subscriptions', date: '2026-05-27' },
];

const initialBudgets: Record<string, BudgetCategory> = {
  Food: { name: 'Food', spent: 4200, budget: 5000, color: 'hsl(var(--primary))' },
  Shopping: { name: 'Shopping', spent: 6100, budget: 5000, color: 'hsl(var(--danger))' },
  Transport: { name: 'Transport', spent: 2800, budget: 3000, color: 'hsl(var(--warning))' },
  Subscriptions: { name: 'Subscriptions', spent: 890, budget: 1000, color: 'hsl(var(--primary-light))' },
  Entertainment: { name: 'Entertainment', spent: 0, budget: 2000, color: 'hsl(var(--ai-purple))' },
};

const initialGoals: Goal[] = [
  { id: 'goal-1', name: 'Emergency Fund', current: 6200, target: 8000, daysLeft: 12, status: 'At risk' },
  { id: 'goal-2', name: 'New MacBook Pro', current: 45000, target: 150000, daysLeft: 90, status: 'On track' },
  { id: 'goal-3', name: 'Europe Summer Trip', current: 120000, target: 300000, daysLeft: 180, status: 'On track' },
];

const initialAlerts = [
  { id: 'alert-1', type: 'danger' as const, text: 'Shopping budget exceeded by ₹1,100' },
  { id: 'alert-2', type: 'warning' as const, text: 'Goal "Emergency Fund" at risk — 12 days left' },
  { id: 'alert-3', type: 'success' as const, text: 'Weekend spend spike detected (+42%)' },
];

const initialChatMessages: ChatMessage[] = [
  {
    id: 'msg-1',
    sender: 'ai',
    text: 'Hello Suraj! 👋 I am your MoneyMind X AI Coach. I have analyzed your transactions for June 2026. Your net worth has increased by 4.2%, but we have some spending spikes to address. How can I help you optimize your finances today?',
    timestamp: '18:23',
  },
];

export const usedashboardStore = create<DashboardState>((set, get) => {
  const recalculateKPIs = (expensesList: ExpenseItem[]) => {
    // 1. Calculate spent by category
    const categorySpent: Record<string, number> = {
      Food: 0,
      Shopping: 0,
      Transport: 0,
      Subscriptions: 0,
      Entertainment: 0,
      Other: 0,
    };
    
    expensesList.forEach(exp => {
      if (categorySpent[exp.category] !== undefined) {
        categorySpent[exp.category] += exp.amount;
      } else {
        categorySpent.Other = (categorySpent.Other || 0) + exp.amount;
      }
    });

    // Update budgets with new spent values
    const currentBudgets = get().budgets || initialBudgets;
    const updatedBudgets = { ...currentBudgets };
    Object.keys(updatedBudgets).forEach(cat => {
      updatedBudgets[cat] = {
        ...updatedBudgets[cat],
        spent: categorySpent[cat] || 0,
      };
    });

    // 2. Sum up total Spent
    const totalSpent = expensesList.reduce((sum, item) => sum + item.amount, 0);

    // 3. Saved & Net Worth
    const baseIncome = 45000; // Let's assume a mock salary
    const computedSaved = Math.max(0, baseIncome - totalSpent);
    
    // Net worth tracking (base ₹1,20,000 + saved)
    const baseNetWorth = 120000;
    const computedNetWorth = baseNetWorth + computedSaved;

    // 4. Stress score based on budgets exceeded
    let budgetOverCount = 0;
    let totalBudget = 0;
    Object.keys(updatedBudgets).forEach(cat => {
      totalBudget += updatedBudgets[cat].budget;
      if (updatedBudgets[cat].spent > updatedBudgets[cat].budget) {
        budgetOverCount += 1;
      }
    });

    const budgetUsageRatio = totalSpent / totalBudget;
    let calculatedStress = Math.min(100, Math.round(budgetUsageRatio * 40 + budgetOverCount * 15));
    if (calculatedStress < 10) calculatedStress = 10;
    
    let computedStressLevel = 'Low pressure';
    if (calculatedStress > 70) {
      computedStressLevel = 'High pressure';
    } else if (calculatedStress > 35) {
      computedStressLevel = 'Moderate pressure';
    }

    // 5. Update dynamic alerts
    const newAlerts = [];
    if (updatedBudgets.Shopping.spent > updatedBudgets.Shopping.budget) {
      newAlerts.push({
        id: 'alert-shop',
        type: 'danger' as const,
        text: `Shopping budget exceeded by ₹${(updatedBudgets.Shopping.spent - updatedBudgets.Shopping.budget).toLocaleString('en-IN')}`,
      });
    }
    
    if (updatedBudgets.Food.spent > updatedBudgets.Food.budget) {
      newAlerts.push({
        id: 'alert-food',
        type: 'danger' as const,
        text: `Food & Dining budget exceeded by ₹${(updatedBudgets.Food.spent - updatedBudgets.Food.budget).toLocaleString('en-IN')}`,
      });
    } else if (updatedBudgets.Food.spent > updatedBudgets.Food.budget * 0.85) {
      newAlerts.push({
        id: 'alert-food-warn',
        type: 'warning' as const,
        text: 'Food & Dining budget is close to limit (85% consumed)',
      });
    }

    // Emergency fund status
    const emergencyFundGoal = get().goals[0];
    if (emergencyFundGoal) {
      newAlerts.push({
        id: 'alert-goal-1',
        type: 'warning' as const,
        text: `Goal "Emergency Fund" at risk — ${emergencyFundGoal.daysLeft} days left`,
      });
    }

    if (totalSpent > totalBudget * 0.75) {
      newAlerts.push({
        id: 'alert-high-spend',
        type: 'warning' as const,
        text: `Total monthly budget spending is high at ${Math.round(budgetUsageRatio * 100)}%`,
      });
    }

    newAlerts.push({
      id: 'alert-spike',
      type: 'success' as const,
      text: 'Weekend spend spike detected (+42%)',
    });

    // Update emergency fund goal current amount dynamically
    const updatedGoals = get().goals.map(goal => {
      if (goal.id === 'goal-1') {
        return {
          ...goal,
          current: computedSaved,
          status: computedSaved < goal.target ? 'At risk' as const : 'On track' as const,
        };
      }
      return goal;
    });

    set({
      expenses: expensesList,
      budgets: updatedBudgets,
      netWorth: computedNetWorth,
      saved: computedSaved,
      stressScore: calculatedStress,
      stressLevel: computedStressLevel,
      alerts: newAlerts,
      goals: updatedGoals,
    });
  };

  return {
    netWorth: 124500,
    netWorthTrend: '↑ 4.2% this month',
    saved: 6200,
    savedTarget: 8000,
    stressScore: 42,
    stressLevel: 'Moderate pressure',
    expenses: initialExpenses,
    budgets: initialBudgets,
    goals: initialGoals,
    alerts: initialAlerts,
    chatMessages: initialChatMessages,
    chatInput: '',
    activeTab: 'Dashboard',

    addExpense: (expenseData) => {
      const newExpense: ExpenseItem = {
        ...expenseData,
        id: `exp-${Date.now()}`,
        date: new Date().toISOString().split('T')[0],
      };
      
      const newExpensesList = [newExpense, ...get().expenses];
      recalculateKPIs(newExpensesList);
    },

    deleteExpense: (id) => {
      const newExpensesList = get().expenses.filter(exp => exp.id !== id);
      recalculateKPIs(newExpensesList);
    },

    setChatInput: (text) => set({ chatInput: text }),

    sendChatMessage: (textOverride) => {
      const text = textOverride || get().chatInput;
      if (!text.trim()) return;

      const userMsg: ChatMessage = {
        id: `msg-user-${Date.now()}`,
        sender: 'user',
        text,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }),
      };

      const currentMessages = [...get().chatMessages, userMsg];
      set({ chatMessages: currentMessages, chatInput: '' });

      // Generate context-aware AI response in 1 second
      setTimeout(() => {
        let aiText = '';
        const currentSaved = get().saved;
        const currentShoppingSpent = get().budgets.Shopping.spent;
        const shoppingLimit = get().budgets.Shopping.budget;

        const lowercaseText = text.toLowerCase();

        if (lowercaseText.includes('shopping') || lowercaseText.includes('impulse') || lowercaseText.includes('over budget')) {
          aiText = `Based on your budget, your **Shopping** category is currently at **₹${currentShoppingSpent.toLocaleString('en-IN')}**, which is **₹${(currentShoppingSpent - shoppingLimit).toLocaleString('en-IN')} over** your ₹${shoppingLimit.toLocaleString('en-IN')} limit. 🛍️\n\nCutting weekend impulse purchases by **30%** over the next 4 weeks could save you approximately **₹3,960/year**. I recommend setting a weekend checkout delay rule (wait 24 hours before buying) to hit your savings goal!`;
        } else if (lowercaseText.includes('emergency') || lowercaseText.includes('save') || lowercaseText.includes('goal')) {
          aiText = `Your **Emergency Fund** savings goal stands at **₹${currentSaved.toLocaleString('en-IN')}** out of a **₹8,000** target, with **12 days left** in the month. 🎯\n\nYou need **₹${(8000 - currentSaved).toLocaleString('en-IN')}** more to hit your goal. To achieve this, try minimizing dining out this week (Food category is at 84% usage) which could easily free up the remaining ₹1,800.`;
        } else if (lowercaseText.includes('stress') || lowercaseText.includes('pressure')) {
          aiText = `Your financial **Stress Score is currently ${get().stressScore}/100** (${get().stressLevel}). This is driven by your overspent Shopping budget (+₹1,100 over) and Food budget close to limit. 🧘‍♂️\n\nTo lower the score, log a few no-spend days this week. If you can avoid shopping for 5 days, your stress score will fall back into the green zone (<35).`;
        } else {
          aiText = `Suraj, looking at your financial snapshot:\n\n- **Net Worth**: ₹${(get().netWorth).toLocaleString('en-IN')} (Up 4.2%)\n- **Spent**: ₹${get().expenses.reduce((sum, e) => sum + e.amount, 0).toLocaleString('en-IN')}\n- **Saved**: ₹${currentSaved.toLocaleString('en-IN')}\n\nYour biggest opportunity is to curve the Shopping overspend. What would you like to drill into? I can suggest a customized plan for food savings, shopping delays, or goals!`;
        }

        const aiMsg: ChatMessage = {
          id: `msg-ai-${Date.now()}`,
          sender: 'ai',
          text: aiText,
          timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }),
        };

        set({ chatMessages: [...get().chatMessages, aiMsg] });
      }, 1000);
    },

    setActiveTab: (tab) => set({ activeTab: tab }),

    triggerAICoachQuestion: (question) => {
      set({ activeTab: 'AI Coach' });
      get().sendChatMessage(question);
    },

    clearAllData: () => set({
      netWorth: 120000,
      netWorthTrend: '↑ 0.0% this month',
      saved: 45000,
      savedTarget: 8000,
      stressScore: 10,
      stressLevel: 'Low pressure',
      expenses: [],
      budgets: {
        Food: { name: 'Food', spent: 0, budget: 5000, color: 'hsl(var(--primary))' },
        Shopping: { name: 'Shopping', spent: 0, budget: 5000, color: 'hsl(var(--danger))' },
        Transport: { name: 'Transport', spent: 0, budget: 3000, color: 'hsl(var(--warning))' },
        Subscriptions: { name: 'Subscriptions', spent: 0, budget: 1000, color: 'hsl(var(--primary-light))' },
        Entertainment: { name: 'Entertainment', spent: 0, budget: 2000, color: 'hsl(var(--ai-purple))' },
      },
      goals: initialGoals.map(g => ({ ...g, current: 0 })),
      alerts: [],
      chatMessages: [
        {
          id: 'msg-clear',
          sender: 'ai',
          text: 'Data cleared! You are starting fresh. Enter your expenses in the Expenses tab, and I will track them in real-time.',
          timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }),
        }
      ]
    }),
  };
});

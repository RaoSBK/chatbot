'use client';

import React, { useEffect } from 'react';
import { 
  LayoutDashboard, 
  Receipt, 
  Target, 
  TrendingUp, 
  Sparkles, 
  RefreshCw
} from 'lucide-react';
import { usedashboardStore } from '../store/dashboardStore';

// Dynamic subviews
import DashboardView from './components/DashboardView';
import ExpensesView from './components/ExpensesView';
import GoalsView from './components/GoalsView';
import InsightsView from './components/InsightsView';
import AICoachView from './components/AICoachView';

export default function MainPage() {
  const { activeTab, setActiveTab, clearAllData } = usedashboardStore();

  // Scroll to top when active tab changes
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [activeTab]);

  const renderActiveView = () => {
    switch (activeTab) {
      case 'Dashboard':
        return <DashboardView />;
      case 'Expenses':
        return <ExpensesView />;
      case 'Goals':
        return <GoalsView />;
      case 'Insights':
        return <InsightsView />;
      case 'AI Coach':
        return <AICoachView />;
      default:
        return <DashboardView />;
    }
  };

  const navItems = [
    { id: 'Dashboard' as const, label: 'Dashboard', icon: LayoutDashboard },
    { id: 'Expenses' as const, label: 'Expenses', icon: Receipt },
    { id: 'Goals' as const, label: 'Goals', icon: Target },
    { id: 'Insights' as const, label: 'Insights', icon: TrendingUp },
    { id: 'AI Coach' as const, label: 'AI Coach', icon: Sparkles },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground pb-12 font-sans selection:bg-primary selection:text-white">
      {/* Premium Top Status Bar/NavBar */}
      <header className="border-b border-border bg-white/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 shadow-sm shadow-slate-100">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          {/* Logo Brand Title */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-primary to-primary-light flex items-center justify-center font-bold text-white text-lg">
              M
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-slate-900">MONEYMIND</span>
              <span className="font-black text-xl text-primary ml-0.5">X</span>
            </div>
          </div>

          {/* Navigation Bar matching second image but styled for light theme */}
          <nav className="flex flex-wrap items-center gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 border ${
                    isActive 
                      ? 'bg-slate-900 text-white border-transparent shadow-md' 
                      : 'bg-transparent text-slate-500 border-transparent hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-primary-light' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                  {item.id === 'AI Coach' && (
                    <span className="w-1.5 h-1.5 rounded-full bg-ai-purple animate-ping ml-0.5" />
                  )}
                </button>
              );
            })}
          </nav>

          {/* Extra utility actions */}
          <div className="flex items-center gap-3">
            <button 
              onClick={clearAllData}
              title="Reset data to empty state"
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-border bg-slate-50 text-xs font-semibold text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-all"
            >
              <RefreshCw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-6xl mx-auto px-6 mt-8">
        {/* Dynamic Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight mb-2">
            {activeTab}
          </h1>
          <p className="text-slate-500 font-medium">
            {activeTab === 'Dashboard' && (
              <>Good morning, Suraj 👋 — Here&apos;s your financial health for June 2026</>
            )}
            {activeTab === 'Expenses' && (
              <>Manage your transactions, filter by categories, and add new expenses below.</>
            )}
            {activeTab === 'Goals' && (
              <>Track your savings targets, emergency funds, and review timeline risks.</>
            )}
            {activeTab === 'Insights' && (
              <>Visual analytics, spending distribution, and comparative trends.</>
            )}
            {activeTab === 'AI Coach' && (
              <>Ask MoneyMind X AI for personalized optimization, insights, and recommendations.</>
            )}
          </p>
        </div>

        {/* View Layout Renderer */}
        <div className="transition-all duration-300">
          {renderActiveView()}
        </div>
      </main>
    </div>
  );
}

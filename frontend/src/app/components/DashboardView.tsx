import React from 'react';
import { 
  TrendingUp, 
  Wallet, 
  Receipt, 
  Target, 
  Activity, 
  Sparkles, 
  AlertTriangle, 
  Bell, 
  ArrowDownCircle,
  Plus
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Cell 
} from 'recharts';
import { usedashboardStore } from '../../store/dashboardStore';

export default function DashboardView() {
  const { 
    netWorth, 
    netWorthTrend, 
    saved, 
    savedTarget, 
    stressScore, 
    stressLevel,
    expenses,
    budgets,
    alerts,
    setActiveTab,
    triggerAICoachQuestion
  } = usedashboardStore();

  // Prepare chart data from budgets state
  const chartData = Object.values(budgets).map(b => ({
    name: b.name,
    amount: b.spent,
    budget: b.budget,
    color: b.color
  }));

  // Reformat currency to lakh abbreviation or standard format
  const formatLakh = (value: number) => {
    if (value >= 100000) {
      return `₹${(value / 100000).toFixed(2)}L`;
    }
    return `₹${value.toLocaleString('en-IN')}`;
  };

  const formatCurrency = (value: number) => {
    return `₹${value.toLocaleString('en-IN')}`;
  };

  return (
    <div className="space-y-6">
      
      {/* 1. KPI Cards Grid - Light Theme Styled */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Net Worth Card */}
        <div className="bg-card border border-border p-5 rounded-2xl relative overflow-hidden transition-all duration-200 hover:border-slate-300 hover:bg-slate-50/50 hover:shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-slate-500 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Wallet className="w-3.5 h-3.5 text-slate-400" />
              Net Worth
            </span>
          </div>
          <h3 className="text-3xl font-extrabold text-slate-900 tracking-tight mb-2">
            {formatLakh(netWorth)}
          </h3>
          <p className="text-primary font-bold text-xs flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5" />
            {netWorthTrend}
          </p>
        </div>

        {/* Spent Card */}
        <div className="bg-card border border-border p-5 rounded-2xl relative overflow-hidden transition-all duration-200 hover:border-slate-300 hover:bg-slate-50/50 hover:shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-slate-500 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Receipt className="w-3.5 h-3.5 text-slate-400" />
              Spent
            </span>
          </div>
          <h3 className="text-3xl font-extrabold text-slate-900 tracking-tight mb-2">
            {formatCurrency(expenses.reduce((sum, e) => sum + e.amount, 0))}
          </h3>
          <p className="text-warning font-bold text-xs">
            {Math.round((expenses.reduce((sum, e) => sum + e.amount, 0) / Object.values(budgets).reduce((sum, b) => sum + b.budget, 0)) * 100)}% of budget
          </p>
        </div>

        {/* Saved Card */}
        <div className="bg-card border border-border p-5 rounded-2xl relative overflow-hidden transition-all duration-200 hover:border-slate-300 hover:bg-slate-50/50 hover:shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-slate-500 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Target className="w-3.5 h-3.5 text-slate-400" />
              Saved
            </span>
          </div>
          <h3 className="text-3xl font-extrabold text-slate-900 tracking-tight mb-2">
            {formatCurrency(saved)}
          </h3>
          <p className="text-primary font-bold text-xs">
            Target {formatCurrency(savedTarget)}
          </p>
        </div>

        {/* Stress Score Card */}
        <div className="bg-card border border-border p-5 rounded-2xl relative overflow-hidden transition-all duration-200 hover:border-slate-300 hover:bg-slate-50/50 hover:shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-slate-500 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-slate-400" />
              Stress score
            </span>
          </div>
          <h3 className={`text-3xl font-extrabold tracking-tight mb-2 ${
            stressScore > 70 ? 'text-danger' : stressScore > 35 ? 'text-warning' : 'text-primary'
          }`}>
            {stressScore}/100
          </h3>
          <p className="text-slate-500 font-semibold text-xs">
            {stressLevel}
          </p>
        </div>

      </div>

      {/* 2. Middle Grid: Spending Chart & Budget Health */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Spending by Category Chart */}
        <div className="bg-card border border-border p-6 rounded-2xl lg:col-span-2 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-slate-900 tracking-tight">
              Spending by category
            </h3>
            <button 
              onClick={() => setActiveTab('Expenses')}
              className="text-xs font-bold text-primary hover:opacity-80 transition flex items-center gap-1"
            >
              <Plus className="w-3.5 h-3.5" />
              Add Expense
            </button>
          </div>

          <div className="h-64 w-full">
            {chartData.every(d => d.amount === 0) ? (
              <div className="h-full flex items-center justify-center text-slate-400 text-sm font-medium border border-dashed border-border rounded-xl bg-slate-50/50">
                No active spend recorded. Try adding an expense!
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                  <XAxis 
                    dataKey="name" 
                    stroke="#64748b" 
                    fontSize={11}
                    tickLine={false}
                    axisLine={false}
                  />
                  <YAxis 
                    stroke="#64748b" 
                    fontSize={11}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) => `₹${value}`}
                  />
                  <Tooltip 
                    cursor={{ fill: 'rgba(0,0,0,0.02)' }}
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="bg-white border border-slate-200 px-3 py-2 rounded-xl shadow-lg text-xs">
                            <p className="text-slate-900 font-extrabold mb-1">{data.name}</p>
                            <p className="text-primary font-bold">Spent: {formatCurrency(data.amount)}</p>
                            <p className="text-slate-500 font-semibold">Budget: {formatCurrency(data.budget)}</p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Bar dataKey="amount" radius={[8, 8, 0, 0]}>
                    {chartData.map((entry, index) => {
                      let color = 'hsl(var(--primary))';
                      if (entry.name === 'Shopping') color = 'hsl(var(--danger))';
                      else if (entry.name === 'Transport') color = 'hsl(var(--ai-purple))';
                      else if (entry.name === 'Subscriptions') color = 'hsl(var(--primary-light))';
                      else if (entry.name === 'Entertainment') color = 'hsl(var(--warning))';
                      
                      return <Cell key={`cell-${index}`} fill={color} />;
                    })}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Color Legend under chart */}
          <div className="flex flex-wrap items-center justify-center gap-4 mt-4 pt-4 border-t border-border/60">
            {Object.values(budgets).map((b) => {
              let dotColor = 'bg-primary';
              if (b.name === 'Shopping') dotColor = 'bg-danger';
              else if (b.name === 'Transport') dotColor = 'bg-ai-purple';
              else if (b.name === 'Subscriptions') dotColor = 'bg-primary-light';
              else if (b.name === 'Entertainment') dotColor = 'bg-warning';

              return (
                <div key={b.name} className="flex items-center gap-1.5 text-xs text-slate-500 font-semibold">
                  <span className={`w-2.5 h-2.5 rounded-full ${dotColor}`} />
                  <span>{b.name}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Budget Health Card */}
        <div className="bg-card border border-border p-6 rounded-2xl flex flex-col justify-between shadow-sm">
          <div>
            <h3 className="text-lg font-bold text-slate-900 tracking-tight mb-5">
              Budget health
            </h3>

            <div className="space-y-4">
              {Object.values(budgets).map((cat) => {
                const ratio = cat.budget > 0 ? cat.spent / cat.budget : 0;
                const percent = Math.min(100, Math.round(ratio * 100));
                
                let barColor = 'bg-primary';
                let textColor = 'text-slate-500';
                
                if (ratio > 1) {
                  barColor = 'bg-danger';
                  textColor = 'text-danger font-bold';
                } else if (ratio > 0.8) {
                  barColor = 'bg-warning';
                  textColor = 'text-warning font-semibold';
                } else {
                  barColor = 'bg-primary';
                }

                const formatShortVal = (val: number) => {
                  if (val >= 1000) {
                    return `₹${(val / 1000).toFixed(1)}K`;
                  }
                  return `₹${val}`;
                };

                return (
                  <div key={cat.name} className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-slate-800">{cat.name}</span>
                      <span className={textColor}>
                        {formatShortVal(cat.spent)} <span className="text-slate-400 font-normal">/ {formatShortVal(cat.budget)}</span>
                      </span>
                    </div>
                    <div className="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${barColor}`}
                        style={{ width: `${percent}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <button
            onClick={() => setActiveTab('Goals')}
            className="w-full text-center py-2.5 mt-4 rounded-xl border border-border text-xs font-bold text-slate-500 hover:text-slate-900 hover:bg-slate-50 transition-all bg-slate-50/50"
          >
            Manage Budgets
          </button>
        </div>

      </div>

      {/* 3. Bottom Grid: AI Coach Insight & Smart Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* AI Coach Insight Card - Light Lavender works perfectly on light background */}
        <div className="bg-ai-light text-[#2d277a] p-6 rounded-2xl relative overflow-hidden shadow-sm border border-[#dcdffd] flex flex-col justify-between group animate-glow-pulse">
          <div className="absolute right-0 top-0 w-36 h-36 bg-gradient-to-br from-indigo-200/50 to-purple-200/40 rounded-full blur-2xl -mr-8 -mt-8 pointer-events-none" />

          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="font-extrabold text-sm uppercase tracking-wider flex items-center gap-1.5 text-ai-purple">
                <Sparkles className="w-4 h-4 text-ai-purple fill-ai-purple/10" />
                AI coach insight
              </span>
              <span className="text-[10px] font-extrabold px-2.5 py-0.5 rounded-full border border-ai-purple/30 text-ai-purple bg-ai-purple/5">
                New
              </span>
            </div>

            <p className="text-base font-bold leading-relaxed mb-6 text-[#2d277a] pr-4">
              Your shopping spend is <span className="underline decoration-wavy decoration-[#ef4444] font-black">₹1,100 over budget</span>. Cutting weekend impulse purchases by 30% could save you <span className="font-black text-ai-purple">₹3,960/year</span>.
            </p>
          </div>

          <button 
            onClick={() => triggerAICoachQuestion("Your shopping spend is ₹1,100 over budget. Cutting weekend impulse purchases by 30% could save you ₹3,960/year. Detail a customized plan for me to accomplish this!")}
            className="flex items-center justify-center gap-1.5 w-max px-5 py-2.5 rounded-xl border-2 border-ai-purple text-xs font-black text-ai-purple bg-transparent transition-all duration-200 hover:bg-ai-purple hover:text-white active:scale-95 shadow-sm shadow-indigo-600/5"
          >
            <span>Ask AI coach</span>
            <span className="font-medium text-xs font-sans">↗</span>
          </button>
        </div>

        {/* Smart Alerts */}
        <div className="bg-card border border-border p-6 rounded-2xl flex flex-col justify-between shadow-sm">
          <div>
            <h3 className="text-lg font-bold text-slate-900 tracking-tight mb-5">
              Smart alerts
            </h3>

            <div className="space-y-3.5">
              {alerts.length === 0 ? (
                <p className="text-slate-400 text-sm font-semibold py-6 text-center">
                  No alerts active. Nice job keeping on track! 🎉
                </p>
              ) : (
                alerts.map((alert) => {
                  let Icon = Bell;
                  let iconColor = 'text-primary bg-primary/10';
                  
                  if (alert.type === 'danger') {
                    Icon = AlertTriangle;
                    iconColor = 'text-danger bg-danger/10';
                  } else if (alert.type === 'warning') {
                    Icon = Bell;
                    iconColor = 'text-warning bg-warning/10';
                  } else if (alert.type === 'success') {
                    Icon = TrendingUp;
                    iconColor = 'text-primary bg-primary/10';
                  }

                  return (
                    <div key={alert.id} className="flex items-start gap-3.5">
                      <div className={`p-2 rounded-xl flex items-center justify-center shrink-0 ${iconColor}`}>
                        <Icon className="w-4 h-4" />
                      </div>
                      <div className="text-xs font-semibold text-slate-600 mt-1 leading-relaxed">
                        {alert.text.includes('exceeded') ? (
                          <>
                            Shopping budget <span className="text-danger font-bold">exceeded</span> by{' '}
                            <span className="text-slate-900 font-extrabold">₹1,100</span>
                          </>
                        ) : alert.text.includes('Emergency Fund') ? (
                          <>
                            Goal <span className="text-slate-900 font-extrabold">&ldquo;Emergency Fund&rdquo;</span> at{' '}
                            <span className="text-warning font-bold">risk</span> &mdash; 12 days left
                          </>
                        ) : (
                          alert.text
                        )}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          <div className="flex items-center justify-center mt-6">
            <ArrowDownCircle className="w-5 h-5 text-slate-400 hover:text-slate-950 transition cursor-pointer animate-bounce" />
          </div>
        </div>

      </div>

    </div>
  );
}

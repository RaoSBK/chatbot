import React from 'react';
import { 
  Sparkles, 
  Lightbulb, 
  ArrowUpRight, 
  Zap, 
  Receipt,
  PiggyBank
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { usedashboardStore } from '../../store/dashboardStore';

export default function InsightsView() {
  const { budgets, saved, expenses } = usedashboardStore();

  // Mock trend data for area chart
  const savingsTrendData = [
    { month: 'Jan', savings: 4800, rate: 12 },
    { month: 'Feb', savings: 5200, rate: 13 },
    { month: 'Mar', savings: 7100, rate: 18 },
    { month: 'Apr', savings: 6800, rate: 17 },
    { month: 'May', savings: 7500, rate: 19 },
    { month: 'Jun', savings: saved, rate: Math.round((saved / 45000) * 100) },
  ];

  // Pie chart data for categories
  const pieData = Object.values(budgets).map(b => ({
    name: b.name,
    value: b.spent
  })).filter(d => d.value > 0);

  const colors = [
    'hsl(var(--primary))',
    'hsl(var(--danger))',
    'hsl(var(--ai-purple))',
    'hsl(var(--primary-light))',
    'hsl(var(--warning))',
    '#64748b'
  ];

  return (
    <div className="space-y-6">
      
      {/* 1. Large Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Savings Area Chart */}
        <div className="bg-card border border-border p-6 rounded-2xl lg:col-span-2 shadow-sm">
          <h3 className="text-base font-bold text-slate-900 mb-6 flex items-center gap-1.5">
            <PiggyBank className="w-5 h-5 text-primary" />
            Monthly Savings Trend (2026)
          </h3>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={savingsTrendData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorSavings" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.15}/>
                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis 
                  dataKey="month" 
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
                  tickFormatter={(val) => `₹${val}`}
                />
                <Tooltip 
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-white border border-slate-200 px-3 py-2 rounded-xl shadow-lg text-xs">
                          <p className="text-slate-900 font-bold mb-0.5">{data.month} 2026</p>
                          <p className="text-primary font-extrabold">Saved: ₹{data.savings.toLocaleString('en-IN')}</p>
                          <p className="text-slate-500 font-semibold">Savings Rate: {data.rate}%</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Area 
                  type="monotone" 
                  dataKey="savings" 
                  stroke="hsl(var(--primary))" 
                  strokeWidth={2.5}
                  fillOpacity={1} 
                  fill="url(#colorSavings)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Expense Category Distribution */}
        <div className="bg-card border border-border p-6 rounded-2xl flex flex-col justify-between shadow-sm">
          <div>
            <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-1.5">
              <Receipt className="w-5 h-5 text-ai-purple" />
              Expense Distribution
            </h3>

            <div className="h-44 w-full flex items-center justify-center relative">
              {pieData.length === 0 ? (
                <span className="text-slate-400 text-xs font-semibold">No active expenditures</span>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={48}
                      outerRadius={70}
                      paddingAngle={3}
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value: any) => `₹${value.toLocaleString('en-IN')}`}
                    />
                  </PieChart>
                </ResponsiveContainer>
              )}
              {pieData.length > 0 && (
                <div className="absolute flex flex-col items-center justify-center">
                  <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Total</span>
                  <span className="text-sm font-extrabold text-slate-950">
                    ₹{expenses.reduce((sum, e) => sum + e.amount, 0).toLocaleString('en-IN')}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Mini Legends List */}
          <div className="grid grid-cols-2 gap-2 mt-2 pt-3 border-t border-border/60">
            {pieData.map((d, index) => (
              <div key={d.name} className="flex items-center gap-1 text-[10px] font-semibold text-slate-500">
                <span 
                  className="w-2.5 h-2.5 rounded-full shrink-0" 
                  style={{ backgroundColor: colors[index % colors.length] }}
                />
                <span className="truncate">{d.name}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* 2. AI Intelligence Patterns Card */}
      <div className="bg-card border border-border p-6 rounded-2xl shadow-sm">
        <h3 className="text-base font-bold text-slate-900 mb-6 flex items-center gap-1.5">
          <Sparkles className="w-5 h-5 text-ai-purple" />
          AI Micro-Pattern Identifications
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          {/* Pattern 1 */}
          <div className="border border-border bg-slate-50/50 p-5 rounded-xl space-y-3 transition hover:border-primary/30 hover:bg-slate-100/20">
            <div className="w-9 h-9 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
              <Zap className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-slate-900">Weekend Shopping Spikes</h4>
            <p className="text-xs text-slate-600 font-medium leading-relaxed">
              We identified that <span className="text-slate-900 font-bold">68% of your shopping expenses</span> occur on Saturdays between 4 PM and 9 PM. Setting a checkout delay could curb this behavior.
            </p>
          </div>

          {/* Pattern 2 */}
          <div className="border border-border bg-slate-50/50 p-5 rounded-xl space-y-3 transition hover:border-ai-purple/30 hover:bg-slate-100/20">
            <div className="w-9 h-9 rounded-lg bg-ai-purple/10 border border-ai-purple/20 flex items-center justify-center text-ai-purple">
              <Lightbulb className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-slate-900">Subscription Consolidation</h4>
            <p className="text-xs text-slate-600 font-medium leading-relaxed">
              Your subscriptions category has increased by 15% due to Netflix adjustments. We recommend auditing unused streaming passes to save an estimated <span className="text-primary font-bold">₹1,800/year</span>.
            </p>
          </div>

          {/* Pattern 3 */}
          <div className="border border-border bg-slate-50/50 p-5 rounded-xl space-y-3 transition hover:border-warning/30 hover:bg-slate-100/20">
            <div className="w-9 h-9 rounded-lg bg-warning/10 border border-warning/20 flex items-center justify-center text-warning">
              <ArrowUpRight className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-slate-900">Food Optimization Potential</h4>
            <p className="text-xs text-slate-600 font-medium leading-relaxed">
              Food delivery spending spiked by <span className="text-slate-900 font-bold">22% this week</span> compared to the monthly average. Opting for meal prep on weekdays could save you ₹2,500/month.
            </p>
          </div>

        </div>
      </div>

    </div>
  );
}

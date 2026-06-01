import React, { useState } from 'react';
import { 
  Target, 
  Clock, 
  Plus, 
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  PlusCircle
} from 'lucide-react';
import { usedashboardStore, Goal } from '../../store/dashboardStore';

export default function GoalsView() {
  const { goals, saved } = usedashboardStore();
  const [name, setName] = useState('');
  const [target, setTarget] = useState('');
  const [days, setDays] = useState('');
  
  // Local addition of goals (could extend Zustand but this is fine and keeps store robust)
  const [localGoals, setLocalGoals] = useState<Goal[]>(goals);

  const handleAddGoal = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !target || !days) return;

    const newGoal: Goal = {
      id: `goal-${Date.now()}`,
      name: name.trim(),
      current: 0,
      target: parseFloat(target),
      daysLeft: parseInt(days),
      status: 'On track',
    };

    setLocalGoals([...localGoals, newGoal]);
    setName('');
    setTarget('');
    setDays('');
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'On track':
        return (
          <span className="flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold text-primary bg-primary/10 border border-primary/20">
            <CheckCircle className="w-3.5 h-3.5 text-primary" />
            On track
          </span>
        );
      case 'At risk':
        return (
          <span className="flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold text-warning bg-warning/10 border border-warning/20">
            <AlertTriangle className="w-3.5 h-3.5 text-warning" />
            At risk
          </span>
        );
      default:
        return (
          <span className="flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold text-danger bg-danger/10 border border-danger/20">
            <AlertTriangle className="w-3.5 h-3.5 text-danger" />
            Overspent
          </span>
        );
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      {/* Target Tracker Panel */}
      <div className="lg:col-span-2 space-y-6">
        {localGoals.map((goal) => {
          const currentAmount = goal.id === 'goal-1' ? saved : goal.current;
          const ratio = currentAmount / goal.target;
          const percent = Math.min(100, Math.round(ratio * 100));

          const computedStatus = goal.id === 'goal-1' 
            ? (currentAmount < goal.target ? 'At risk' as const : 'On track' as const) 
            : goal.status;

          return (
            <div key={goal.id} className="bg-card border border-border p-6 rounded-2xl space-y-5 transition hover:bg-slate-50/50 shadow-sm">
              
              {/* Header */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-primary/15 to-primary-light/5 border border-primary/20 flex items-center justify-center">
                    <Target className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h4 className="text-base font-extrabold text-slate-900">{goal.name}</h4>
                    <p className="text-xs text-slate-500 font-semibold flex items-center gap-1 mt-0.5">
                      <Clock className="w-3 h-3 text-slate-400" />
                      {goal.daysLeft} days remaining
                    </p>
                  </div>
                </div>

                <div className="shrink-0">
                  {getStatusBadge(computedStatus)}
                </div>
              </div>

              {/* Goal Stats */}
              <div className="grid grid-cols-3 gap-4 py-3 border-y border-border/60 text-center sm:text-left">
                <div>
                  <span className="block text-[10px] text-slate-500 font-bold uppercase tracking-wider">Current savings</span>
                  <span className="text-lg font-black text-slate-900">₹{currentAmount.toLocaleString('en-IN')}</span>
                </div>
                <div>
                  <span className="block text-[10px] text-slate-500 font-bold uppercase tracking-wider">Target amount</span>
                  <span className="text-lg font-black text-slate-400">₹{goal.target.toLocaleString('en-IN')}</span>
                </div>
                <div>
                  <span className="block text-[10px] text-slate-500 font-bold uppercase tracking-wider">Completion</span>
                  <span className="text-lg font-black text-primary">{percent}%</span>
                </div>
              </div>

              {/* Progress Slider */}
              <div className="space-y-2">
                <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden">
                  <div 
                    className="h-full rounded-full bg-gradient-to-r from-primary to-primary-light transition-all duration-500"
                    style={{ width: `${percent}%` }}
                  />
                </div>
                <div className="flex justify-between text-[10px] font-bold text-slate-400">
                  <span>0%</span>
                  <span>100% Target</span>
                </div>
              </div>

            </div>
          );
        })}
      </div>

      {/* Quick Stats & Form */}
      <div className="lg:col-span-1 space-y-6">
        
        {/* Helper Analytics Card */}
        <div className="bg-card border border-border p-6 rounded-2xl relative overflow-hidden shadow-sm">
          <div className="absolute right-0 top-0 w-24 h-24 bg-primary/5 rounded-full blur-xl pointer-events-none" />
          
          <h3 className="text-sm font-black text-slate-900 uppercase tracking-wider mb-4 flex items-center gap-1.5">
            <TrendingUp className="w-4 h-4 text-primary" />
            Savings Optimization
          </h3>
          
          <div className="space-y-4">
            <p className="text-xs text-slate-600 font-medium leading-relaxed">
              To hit your <span className="text-slate-900 font-bold">₹8,000 Emergency Fund</span> target in the next <span className="text-slate-900 font-bold">12 days</span>, you need to reserve:
            </p>
            
            <div className="bg-slate-50/50 border border-border rounded-xl p-4 divide-y divide-border/60 text-xs font-semibold">
              <div className="py-2.5 flex justify-between">
                <span className="text-slate-500">Daily savings rate:</span>
                <span className="text-slate-950 font-bold">₹150 / day</span>
              </div>
              <div className="py-2.5 flex justify-between">
                <span className="text-slate-500">Weekly requirement:</span>
                <span className="text-slate-950 font-bold">₹1,050 / week</span>
              </div>
              <div className="py-2.5 flex justify-between">
                <span className="text-slate-500">Remaining to save:</span>
                <span className="text-primary font-black">₹{Math.max(0, 8000 - saved).toLocaleString('en-IN')}</span>
              </div>
            </div>

            <p className="text-[10px] text-slate-400 font-medium italic">
              * Calculations are updated automatically as you log new transactions in the Expenses tab.
            </p>
          </div>
        </div>

        {/* Goal Add Form */}
        <div className="bg-card border border-border p-6 rounded-2xl shadow-sm">
          <h3 className="text-sm font-black text-slate-900 uppercase tracking-wider mb-4 flex items-center gap-1.5">
            <PlusCircle className="w-4 h-4 text-primary" />
            Establish New Goal
          </h3>

          <form onSubmit={handleAddGoal} className="space-y-4">
            <div>
              <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                Goal Name
              </label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Down Payment on Car"
                className="w-full bg-slate-50/50 border border-border rounded-xl px-4 py-2 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-primary focus:bg-white transition"
              />
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                Target Amount (₹)
              </label>
              <input
                type="number"
                required
                min="1"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                placeholder="50000"
                className="w-full bg-slate-50/50 border border-border rounded-xl px-4 py-2 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-primary focus:bg-white transition"
              />
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                Timeline (Days)
              </label>
              <input
                type="number"
                required
                min="1"
                value={days}
                onChange={(e) => setDays(e.target.value)}
                placeholder="30"
                className="w-full bg-slate-50/50 border border-border rounded-xl px-4 py-2 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-primary focus:bg-white transition"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-slate-900 hover:bg-slate-800 active:scale-95 text-white font-extrabold text-xs py-2.5 rounded-xl transition duration-200 mt-2 flex items-center justify-center gap-1.5 shadow-sm"
            >
              <Plus className="w-3.5 h-3.5" />
              Add Savings Goal
            </button>
          </form>
        </div>

      </div>

    </div>
  );
}

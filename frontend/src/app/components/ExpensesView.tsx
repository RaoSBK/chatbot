import React, { useState } from 'react';
import { 
  Plus, 
  Trash2, 
  Search, 
  Filter,
  Calendar,
  PlusCircle
} from 'lucide-react';
import { usedashboardStore } from '../../store/dashboardStore';

export default function ExpensesView() {
  const { expenses, addExpense, deleteExpense, budgets } = usedashboardStore();
  
  // Form State
  const [title, setTitle] = useState('');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState<'Food' | 'Shopping' | 'Transport' | 'Subscriptions' | 'Entertainment' | 'Other'>('Food');
  
  // Search & Filter State
  const [search, setSearch] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('All');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !amount) return;

    addExpense({
      title: title.trim(),
      amount: parseFloat(amount),
      category: category,
    });

    // Reset form
    setTitle('');
    setAmount('');
    setCategory('Food');
  };

  const filteredExpenses = expenses.filter(exp => {
    const matchesSearch = exp.title.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = filterCategory === 'All' || exp.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  const getCategoryColor = (cat: string) => {
    switch (cat) {
      case 'Food': return 'bg-primary/10 text-primary border-primary/20';
      case 'Shopping': return 'bg-danger/10 text-danger border-danger/20';
      case 'Transport': return 'bg-ai-purple/10 text-ai-purple border-ai-purple/20';
      case 'Subscriptions': return 'bg-primary-light/10 text-primary-light border-primary-light/20';
      case 'Entertainment': return 'bg-warning/10 text-warning border-warning/20';
      default: return 'bg-slate-500/10 text-slate-500 border-slate-500/20';
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 relative">
      
      {/* Slide-over Form Panel or Left Panel */}
      <div className="lg:col-span-1">
        <div className="bg-card border border-border p-6 rounded-2xl sticky top-24 shadow-sm">
          <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <PlusCircle className="w-5 h-5 text-primary" />
            Quick Add Expense
          </h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                Expense Title
              </label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Starbucks Coffee"
                className="w-full bg-slate-50/50 border border-border rounded-xl px-4 py-2.5 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-primary focus:bg-white transition"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                Amount (₹)
              </label>
              <div className="relative">
                <span className="absolute left-4 top-2.5 text-slate-400 text-sm font-bold">₹</span>
                <input
                  type="number"
                  required
                  min="1"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  placeholder="250"
                  className="w-full bg-slate-50/50 border border-border rounded-xl pl-8 pr-4 py-2.5 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-primary focus:bg-white transition"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value as any)}
                className="w-full bg-slate-50/50 border border-border rounded-xl px-4 py-2.5 text-sm text-slate-900 focus:outline-none focus:border-primary focus:bg-white transition"
              >
                <option value="Food">Food & Dining</option>
                <option value="Shopping">Shopping</option>
                <option value="Transport">Transport</option>
                <option value="Subscriptions">Subscriptions</option>
                <option value="Entertainment">Entertainment</option>
                <option value="Other">Other / Misc</option>
              </select>
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-primary to-primary-light hover:opacity-90 active:scale-95 text-white font-extrabold text-sm py-3 rounded-xl shadow-md shadow-primary/10 transition duration-200 mt-2 flex items-center justify-center gap-1.5"
            >
              <Plus className="w-4 h-4 text-white stroke-[3px]" />
              Add Expense
            </button>
          </form>
        </div>
      </div>

      {/* Expenses List Panel */}
      <div className="lg:col-span-2 space-y-4">
        
        {/* Search & Filter Toolbar */}
        <div className="bg-card border border-border p-4 rounded-2xl flex flex-col sm:flex-row gap-3 shadow-sm">
          <div className="relative flex-grow">
            <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search expenses..."
              className="w-full bg-slate-50/50 border border-border rounded-xl pl-10 pr-4 py-2 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-primary focus:bg-white transition"
            />
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="bg-slate-50/50 border border-border rounded-xl px-3 py-2 text-xs font-bold text-slate-600 focus:outline-none focus:border-primary focus:bg-white transition"
            >
              <option value="All">All Categories</option>
              {Object.keys(budgets).map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        {/* Expenses List Card */}
        <div className="bg-card border border-border rounded-2xl overflow-hidden shadow-sm">
          <div className="px-6 py-4 border-b border-border bg-slate-50/50">
            <h4 className="text-sm font-bold text-slate-700">Transaction Ledger</h4>
          </div>

          <div className="divide-y divide-border">
            {filteredExpenses.length === 0 ? (
              <div className="px-6 py-12 text-center text-slate-400 font-semibold text-sm">
                No matching transactions found.
              </div>
            ) : (
              filteredExpenses.map((exp) => (
                <div 
                  key={exp.id} 
                  className="px-6 py-4 flex items-center justify-between hover:bg-slate-50/50 transition-all group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-slate-50 border border-border flex items-center justify-center text-slate-600 font-bold">
                      {exp.title.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <h5 className="text-sm font-bold text-slate-900">{exp.title}</h5>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-[10px] text-slate-400 font-bold flex items-center gap-0.5">
                          <Calendar className="w-2.5 h-2.5" />
                          {exp.date}
                        </span>
                        <span className={`text-[9px] font-extrabold px-2 py-0.5 rounded border uppercase tracking-wider ${getCategoryColor(exp.category)}`}>
                          {exp.category}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <span className="text-sm font-extrabold text-slate-900">
                      -₹{exp.amount.toLocaleString('en-IN')}
                    </span>
                    <button
                      onClick={() => deleteExpense(exp.id)}
                      className="p-2 rounded-lg text-slate-400 hover:text-danger hover:bg-danger/10 transition opacity-0 group-hover:opacity-100 focus:opacity-100"
                      title="Delete transaction"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>

    </div>
  );
}

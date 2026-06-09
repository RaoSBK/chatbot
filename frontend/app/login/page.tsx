'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useauthStore } from '../../src/store/authStore';
import { Mail, Lock, User, ArrowRight, Eye, EyeOff, Loader2 } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const { login, register, isAuthenticated, error: storeError, initialize } = useauthStore();

  const [isLoginTab, setIsLoginTab] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'error' | 'success'; message: string } | null>(null);

  // Initialize store and check if already authenticated
  useEffect(() => {
    initialize();
  }, [initialize]);

  useEffect(() => {
    if (isAuthenticated) {
      // If already logged in, show success and wait briefly before redirect
      setFeedback({ type: 'success', message: 'Already authenticated! Redirecting...' });
      const timer = setTimeout(() => {
        router.push('/');
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [isAuthenticated, router]);

  const validateForm = () => {
    if (!email || !email.includes('@')) {
      setFeedback({ type: 'error', message: 'Please enter a valid email address.' });
      return false;
    }
    if (!password || password.length < 6) {
      setFeedback({ type: 'error', message: 'Password must be at least 6 characters long.' });
      return false;
    }
    if (!isLoginTab && !fullName) {
      setFeedback({ type: 'error', message: 'Full name is required for registration.' });
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFeedback(null);

    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      if (isLoginTab) {
        const result = await login({ email, password });
        if (result.success) {
          setFeedback({ type: 'success', message: 'Successfully logged in! Redirecting...' });
          setTimeout(() => {
            router.push('/');
          }, 1500);
        } else {
          setFeedback({ type: 'error', message: result.error || 'Authentication failed.' });
        }
      } else {
        const result = await register({ full_name: fullName, email, password });
        if (result.success) {
          setFeedback({ type: 'success', message: 'Account created successfully! You can now log in.' });
          // Switch to login tab and clear fields
          setIsLoginTab(true);
          setPassword('');
        } else {
          setFeedback({ type: 'error', message: result.error || 'Registration failed.' });
        }
      }
    } catch (err: any) {
      setFeedback({ type: 'error', message: 'An unexpected error occurred. Please try again.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden px-4">
      {/* Dynamic Background Gradients */}
      <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 translate-x-1/2 translate-y-1/2 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />

      {/* Grid Pattern */}
      <div 
        className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: 'radial-gradient(circle, #8b5cf6 1px, transparent 1px)',
          backgroundSize: '24px 24px'
        }}
      />

      <div className="w-full max-w-md z-10">
        {/* Brand / Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center p-3 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 shadow-lg shadow-purple-900/40 mb-4 animate-pulse">
            <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-200 via-slate-100 to-indigo-200">
            MoneyMindX
          </h1>
          <p className="text-sm text-slate-400 mt-2">
            AI-Powered Personal Finance & Wealth Simulator
          </p>
        </div>

        {/* Auth Box Container */}
        <div className="relative rounded-3xl bg-slate-900/65 backdrop-blur-xl border border-slate-800 shadow-2xl p-8 overflow-hidden">
          {/* Glowing Top Border */}
          <div className="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-purple-500 to-transparent" />

          {/* Custom Tabs */}
          <div className="flex border-b border-slate-800/80 mb-6">
            <button
              type="button"
              onClick={() => {
                setIsLoginTab(true);
                setFeedback(null);
              }}
              className={`flex-1 pb-3 text-sm font-semibold transition-all duration-300 relative ${
                isLoginTab ? 'text-purple-400' : 'text-slate-500 hover:text-slate-300'
              }`}
            >
              Sign In
              {isLoginTab && (
                <span className="absolute bottom-0 left-0 right-0 h-[2px] bg-purple-500 rounded-full" />
              )}
            </button>
            <button
              type="button"
              onClick={() => {
                setIsLoginTab(false);
                setFeedback(null);
              }}
              className={`flex-1 pb-3 text-sm font-semibold transition-all duration-300 relative ${
                !isLoginTab ? 'text-purple-400' : 'text-slate-500 hover:text-slate-300'
              }`}
            >
              Create Account
              {!isLoginTab && (
                <span className="absolute bottom-0 left-0 right-0 h-[2px] bg-purple-500 rounded-full" />
              )}
            </button>
          </div>

          {/* Feedback Alerts */}
          {feedback && (
            <div
              className={`p-3.5 rounded-xl text-sm mb-5 border transition-all duration-300 animate-fadeIn ${
                feedback.type === 'error'
                  ? 'bg-rose-500/10 border-rose-500/20 text-rose-300'
                  : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-300'
              }`}
            >
              {feedback.message}
            </div>
          )}

          {/* Authentication Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Full Name field (Only visible in Register) */}
            {!isLoginTab && (
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Full Name
                </label>
                <div className="relative group">
                  <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500 transition-colors group-focus-within:text-purple-400">
                    <User className="w-5 h-5" />
                  </span>
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="John Doe"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-purple-500/60 focus:ring-2 focus:ring-purple-500/20 transition-all duration-200"
                  />
                </div>
              </div>
            )}

            {/* Email Address */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Email Address
              </label>
              <div className="relative group">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500 transition-colors group-focus-within:text-purple-400">
                  <Mail className="w-5 h-5" />
                </span>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-purple-500/60 focus:ring-2 focus:ring-purple-500/20 transition-all duration-200"
                />
              </div>
            </div>

            {/* Password */}
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Password
                </label>
                {isLoginTab && (
                  <a href="#" className="text-xs text-purple-400 hover:text-purple-300 transition-colors">
                    Forgot password?
                  </a>
                )}
              </div>
              <div className="relative group">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500 transition-colors group-focus-within:text-purple-400">
                  <Lock className="w-5 h-5" />
                </span>
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-12 py-2.5 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-purple-500/60 focus:ring-2 focus:ring-purple-500/20 transition-all duration-200"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-500 hover:text-slate-300 transition-colors focus:outline-none"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full flex items-center justify-center gap-2 mt-6 py-3 px-4 rounded-xl text-white font-semibold bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-slate-900 transition-all duration-150 shadow-lg shadow-purple-900/30 disabled:opacity-50 disabled:pointer-events-none"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  {isLoginTab ? 'Sign In' : 'Create Account'}
                  <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Footer info */}
        <p className="text-center text-xs text-slate-500 mt-6">
          Secured by JWT Authentication. MoneyMindX v1.0.0
        </p>
      </div>
    </div>
  );
}

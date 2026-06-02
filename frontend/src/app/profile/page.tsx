'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  User, Mail, Calendar, Shield, LogOut, ChevronLeft,
  Sparkles, Edit2, Check, X, Loader2, KeyRound, Clock
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { useAuthStore } from '../../store/authStore';

function InfoRow({
  icon: Icon,
  label,
  value,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-start gap-4 p-4 rounded-xl bg-white/5 border border-white/10 hover:border-white/15 transition-all">
      <div className="mt-0.5 w-8 h-8 rounded-lg bg-emerald-500/15 flex items-center justify-center flex-shrink-0">
        <Icon className="w-4 h-4 text-emerald-400" />
      </div>
      <div className="min-w-0">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-0.5">{label}</p>
        <p className="text-sm text-white font-medium break-all">{value}</p>
      </div>
    </div>
  );
}

function Avatar({ name, email }: { name: string | null; email: string }) {
  const initials = name
    ? name.split(' ').map((n) => n[0]).join('').slice(0, 2).toUpperCase()
    : email.slice(0, 2).toUpperCase();

  return (
    <div className="relative mx-auto w-24 h-24">
      <div className="w-24 h-24 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-white text-3xl font-bold shadow-xl shadow-emerald-500/30">
        {initials}
      </div>
      <div className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-emerald-500 border-2 border-slate-900 flex items-center justify-center">
        <div className="w-2 h-2 rounded-full bg-white animate-pulse" />
      </div>
    </div>
  );
}

export default function ProfilePage() {
  const { user, isLoading, logout } = useAuth({ requireAuth: true });
  const accessToken = useAuthStore((s) => s.accessToken);
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);
    await logout();
  };

  if (isLoading || !user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-10 h-10 text-emerald-400 animate-spin" />
          <p className="text-slate-400 text-sm">Loading your profile…</p>
        </div>
      </div>
    );
  }

  const memberSince = new Date(user.created_at).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  });
  const lastUpdated = new Date(user.updated_at).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4 md:p-8">
      {/* Ambient glows */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full bg-emerald-500/8 blur-3xl" />
        <div className="absolute bottom-1/4 right-0 w-72 h-72 rounded-full bg-violet-600/8 blur-3xl" />
      </div>

      <div className="relative max-w-2xl mx-auto">
        {/* Back nav */}
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-slate-400 hover:text-white mb-6 transition-colors group"
        >
          <ChevronLeft className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" />
          Back to Dashboard
        </Link>

        {/* Header card */}
        <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl overflow-hidden mb-4">
          <div className="h-1 w-full bg-gradient-to-r from-emerald-400 via-teal-400 to-violet-500" />

          {/* Cover banner */}
          <div className="h-28 bg-gradient-to-br from-emerald-900/40 via-teal-900/30 to-slate-900/40 relative">
            <div className="absolute inset-0 opacity-20"
              style={{ backgroundImage: 'radial-gradient(circle at 20% 50%, #10b981 0%, transparent 50%), radial-gradient(circle at 80% 20%, #6366f1 0%, transparent 50%)' }}
            />
            <div className="absolute top-3 right-3 flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/30">
              <Sparkles className="w-3 h-3 text-emerald-400" />
              <span className="text-emerald-400 text-xs font-semibold">Active</span>
            </div>
          </div>

          <div className="px-6 pb-6 -mt-12">
            <Avatar name={user.full_name} email={user.email} />
            <div className="mt-4 text-center">
              <h1 className="text-xl font-bold text-white">
                {user.full_name ?? 'Anonymous User'}
              </h1>
              <p className="text-slate-400 text-sm mt-0.5">{user.email}</p>
            </div>

            {/* Stat pills */}
            <div className="flex items-center justify-center gap-3 mt-4 flex-wrap">
              <div className="px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-slate-400">
                <span className="text-white font-semibold">Member</span> since {new Date(user.created_at).getFullYear()}
              </div>
              <div className="px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-400 font-medium">
                Verified Account
              </div>
            </div>
          </div>
        </div>

        {/* Info grid */}
        <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6 mb-4">
          <h2 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2">
            <User className="w-4 h-4 text-emerald-400" />
            Account Details
          </h2>
          <div className="space-y-3">
            <InfoRow icon={User}     label="Full Name"     value={user.full_name ?? '—'} />
            <InfoRow icon={Mail}     label="Email Address" value={user.email} />
            <InfoRow icon={Calendar} label="Member Since"  value={memberSince} />
            <InfoRow icon={Clock}    label="Last Updated"  value={lastUpdated} />
            <InfoRow icon={Shield}   label="Account ID"    value={user.id.slice(0, 8) + '…' + user.id.slice(-4)} />
          </div>
        </div>

        {/* Session info */}
        <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6 mb-4">
          <h2 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2">
            <KeyRound className="w-4 h-4 text-violet-400" />
            Current Session
          </h2>
          <div className="space-y-3">
            <div className="p-4 rounded-xl bg-violet-500/10 border border-violet-500/20">
              <p className="text-xs text-slate-500 mb-1">Access Token (preview)</p>
              <p className="text-xs text-violet-300 font-mono break-all">
                {accessToken
                  ? accessToken.slice(0, 40) + '…'
                  : 'Not available'}
              </p>
            </div>
            <div className="flex items-center gap-3 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-sm text-emerald-400 font-medium">Session Active · Refresh token in HttpOnly cookie</span>
            </div>
          </div>
        </div>

        {/* Danger zone */}
        <div className="rounded-2xl border border-red-500/20 bg-red-500/5 backdrop-blur-xl p-6">
          <h2 className="text-sm font-bold text-red-400 uppercase tracking-wider mb-4 flex items-center gap-2">
            <LogOut className="w-4 h-4" />
            Session Management
          </h2>
          <p className="text-slate-400 text-sm mb-4">
            Signing out will clear your session and remove the refresh-token cookie from this device.
          </p>
          <button
            id="profile-logout"
            onClick={handleLogout}
            disabled={loggingOut}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-red-500/15 border border-red-500/30 text-red-400 hover:bg-red-500/25 hover:text-red-300 text-sm font-semibold transition-all disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loggingOut ? (
              <><Loader2 className="w-4 h-4 animate-spin" /><span>Signing out…</span></>
            ) : (
              <><LogOut className="w-4 h-4" /><span>Sign Out</span></>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

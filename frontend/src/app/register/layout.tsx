import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Create Account — MoneyMind X',
  description: 'Register a free MoneyMind X account and take control of your personal finances with AI-powered insights.',
};

export default function RegisterLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}

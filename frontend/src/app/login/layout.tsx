import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Sign In — MoneyMind X',
  description: 'Sign in to your MoneyMind X account to access your personal finance dashboard.',
};

export default function LoginLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}

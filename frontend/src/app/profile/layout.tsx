import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My Profile — MoneyMind X',
  description: 'View and manage your MoneyMind X account profile and session.',
};

export default function ProfileLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}

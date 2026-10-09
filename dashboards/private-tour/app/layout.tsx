import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Private Tour 看板',
  description: 'Private Tour 广告 → SQL → 成交,以及销售跟进表现',
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}

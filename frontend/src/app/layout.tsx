import './globals.css';
import type { Metadata, Viewport } from 'next';

export const metadata: Metadata = {
  title: 'KALKI AI — Master Intelligence Operating System',
  description: 'Unified enterprise AI platform combining LLMs, VLMs, autonomous multi-agent orchestration, hybrid RAG, and defensive cybersecurity.',
  icons: {
    icon: '/favicon.png',
    shortcut: '/favicon.ico',
    apple: '/kalki_symbol.jpg',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  themeColor: '#07090E',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased min-h-screen bg-[#07090E] text-gray-100">
        {children}
      </body>
    </html>
  );
}

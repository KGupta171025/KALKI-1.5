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
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                var targetHost = 'kalki.hg497kg.workers.dev';
                var currentHost = window.location.hostname.toLowerCase();
                if (currentHost === 'kgupta171025.github.io' || (currentHost !== targetHost && currentHost !== 'localhost' && currentHost !== '127.0.0.1' && !currentHost.endsWith('.local'))) {
                  var cleanPath = window.location.pathname.replace(/^\\/KALKI-1.5\\/?/, '/');
                  var targetUrl = 'https://' + targetHost + (cleanPath.startsWith('/') ? cleanPath : '/' + cleanPath) + window.location.search + window.location.hash;
                  window.location.replace(targetUrl);
                }
              })();
            `,
          }}
        />
      </head>
      <body className="antialiased min-h-screen bg-[#07090E] text-gray-100">
        {children}
      </body>
    </html>
  );
}

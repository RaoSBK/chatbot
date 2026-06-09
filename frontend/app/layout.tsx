import '../src/styles/globals.css';

export const metadata = {
  title: 'MoneyMindX',
  description: 'Personal Finance and Wealth Simulator',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#0a0a0c] text-slate-100 font-sans antialiased selection:bg-purple-600 selection:text-white">
        {children}
      </body>
    </html>
  )
}

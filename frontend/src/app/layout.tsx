import type { Metadata } from 'next'
import { Providers } from '@/app/providers'
import '@/styles/globals.css'

export const metadata: Metadata = {
  title: 'ACNC Malaysia Donor Platform',
  description: 'Multi-currency donation platform for missionary support',
  icons: {
    icon: '/favicon.ico',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}

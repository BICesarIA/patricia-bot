import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { ThemeProvider } from "@/components/theme-provider"
import { LanguageProvider } from "@/context/language-context"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "CESARIA.NET - Smart Solutions",
  description: "Business Intelligence and AI Bot solutions for modern businesses",
  keywords: "CRM, automatic collections, WhatsApp bots, dashboards, Power BI, intelligence Artificial",
  openGraph: {
    type: "website",
    locale: "es_ES",
    url: "https://cesaria.net",
    siteName: "CESARIA.NET",
    title: "CESARIA.NET - Smart Solutions",
    description: "Business Intelligence and AI Bot solutions for modern businesses",
    images: [
      {
        url: "/images/logo.png",
        width: 800,
        height: 600,
        alt: "CESARIA.NET",
      },
    ],
  },
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <head>
        {/* Space for Google Analytics */}
        {/* 
        <script
          async
          src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
            `,
          }}
        />
        */}
      </head>
      <body className={`${inter.className} bg-black min-h-screen flex flex-col`}>
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
          <LanguageProvider defaultLanguage="es">{children}</LanguageProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}

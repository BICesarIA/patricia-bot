"use client"

import Link from "next/link"
import Image from "next/image"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { useTheme } from "next-themes"
import { useLanguage } from "@/context/language-context"
import { Sun, Moon, Menu, X, Globe } from "lucide-react"

interface HeaderProps {
  userName?: string
}

export default function Header({ userName }: HeaderProps) {
  const pathname = usePathname()
  const isLoggedIn = pathname.includes("/bi/") || pathname.includes("/bot/")
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { theme, setTheme } = useTheme()
  const { language, setLanguage, t } = useLanguage()

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark")
  }

  const toggleLanguage = () => {
    setLanguage(language === "es" ? "en" : "es")
  }

  return (
    <header className="container mx-auto px-4 py-6 flex justify-between items-center">
      <Link href="/" className="flex items-center">
        <Image src="/images/logo.png" alt="CESARIA.NET" width={150} height={80} priority />
      </Link>

      {isLoggedIn ? (
        <div className="flex items-center gap-4">
          <span className="hidden md:inline-block">
            {t("welcome")}, {userName || "User"}
          </span>
          <Link href="/" className="btn-gold text-sm">
            {t("logout")}
          </Link>
        </div>
      ) : (
        <>
          <nav className="hidden md:flex space-x-8">
            <Link href="/" className="text-white hover:text-gold transition-colors">
              {t("home")}
            </Link>
            <Link href="/login" className="text-white hover:text-gold transition-colors">
              {t("login")}
            </Link>
            <Link href="/plans" className="text-white hover:text-gold transition-colors">
              {t("plans")}
            </Link>
          </nav>

          <div className="hidden md:flex items-center space-x-4">
            <button
              onClick={toggleLanguage}
              className="p-2 rounded-full hover:bg-gray-800 transition-colors"
              aria-label={language === "es" ? "Switch to English" : "Cambiar a Español"}
            >
              <Globe size={20} />
              <span className="sr-only">{language === "es" ? "EN" : "ES"}</span>
            </button>
            <button
              onClick={toggleTheme}
              className="p-2 rounded-full hover:bg-gray-800 transition-colors"
              aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            >
              {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
            </button>
          </div>
        </>
      )}

      <div className="md:hidden flex items-center space-x-2">
        <button
          onClick={toggleLanguage}
          className="p-2 rounded-full hover:bg-gray-800 transition-colors"
          aria-label={language === "es" ? "Switch to English" : "Cambiar a Español"}
        >
          <Globe size={20} />
        </button>
        <button
          onClick={toggleTheme}
          className="p-2 rounded-full hover:bg-gray-800 transition-colors"
          aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
        >
          {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
        </button>
        <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="p-2 text-white" aria-label="Toggle menu">
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-black bg-opacity-90 flex flex-col items-center justify-center">
          <button
            onClick={() => setMobileMenuOpen(false)}
            className="absolute top-6 right-6 text-white"
            aria-label="Close menu"
          >
            <X size={24} />
          </button>
          <nav className="flex flex-col items-center space-y-8 text-xl">
            <Link
              href="/"
              className="text-white hover:text-gold transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("home")}
            </Link>
            <Link
              href="/login"
              className="text-white hover:text-gold transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("login")}
            </Link>
            <Link
              href="/plans"
              className="text-white hover:text-gold transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("plans")}
            </Link>
          </nav>
        </div>
      )}
    </header>
  )
}

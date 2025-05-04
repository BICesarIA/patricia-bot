"use client"

import type React from "react"
import { createContext, useState, useContext, useEffect } from "react"

type Language = "es" | "en"

type Translations = {
  [key: string]: {
    es: string
    en: string
  }
}

// Common translations used across the app
const translations: Translations = {
  // Header
  home: {
    es: "Inicio",
    en: "Home",
  },
  login: {
    es: "Iniciar Sesión",
    en: "Login",
  },
  plans: {
    es: "Planes y Precios",
    en: "Plans & Pricing",
  },
  about: {
    es: "Sobre Mí",
    en: "About Me",
  },
  // Landing page
  welcomeTitle: {
    es: "CESARIA.NET – Soluciones Inteligentes",
    en: "CESARIA.NET – Smart Solutions",
  },
  biTitle: {
    es: "CesarIA BI",
    en: "CesarIA BI",
  },
  biDescription: {
    es: "Consultoría KPI, Power BI, Excel. Soluciones de Inteligencia de Negocios para su empresa.",
    en: "KPI Consulting, Power BI, Excel. Business Intelligence solutions for your company.",
  },
  botTitle: {
    es: "CesarIA BOT Suite CRM",
    en: "CesarIA BOT Suite CRM",
  },
  botDescription: {
    es: "Bots para mensajes y llamadas enfocados en cobranzas y ventas.",
    en: "Bots for messages and calls focused on collections and sales.",
  },
  cesariaSubtext: {
    es: "Especialistas en automatización de cobranzas mediante llamadas con IA",
    en: "Specialists in collections automation through AI calls",
  },
  patriciaSubtext: {
    es: "Expertos en soporte automatizado para ventas y recuperación de pagos",
    en: "Experts in automated support for sales and payment recovery",
  },
  exploreBi: {
    es: "Explorar BI",
    en: "Explore BI",
  },
  exploreBots: {
    es: "Explorar Bots",
    en: "Explore Bots",
  },
  // Footer
  copyright: {
    es: "© 2025 CESARIA.NET | Todos los derechos reservados.",
    en: "© 2025 CESARIA.NET | All rights reserved.",
  },
  // Login
  loginTitle: {
    es: "Iniciar Sesión",
    en: "Sign In",
  },
  email: {
    es: "Correo Electrónico",
    en: "Email Address",
  },
  password: {
    es: "Contraseña",
    en: "Password",
  },
  rememberMe: {
    es: "Recordarme",
    en: "Remember me",
  },
  forgotPassword: {
    es: "¿Olvidó su contraseña?",
    en: "Forgot password?",
  },
  loginButton: {
    es: "Iniciar Sesión",
    en: "Login",
  },
  accessTo: {
    es: "Acceder a",
    en: "Access to",
  },
  // Plans
  plansTitle: {
    es: "Planes y Precios",
    en: "Plans and Pricing",
  },
  biPlans: {
    es: "Planes BI",
    en: "BI Plans",
  },
  botPlans: {
    es: "Planes BOT",
    en: "BOT Plans",
  },
  getQuote: {
    es: "Solicitar Cotización",
    en: "Get a Quote",
  },
  // Dashboard
  dashboard: {
    es: "Panel de Control",
    en: "Dashboard",
  },
  roles: {
    es: "Roles",
    en: "Roles",
  },
  users: {
    es: "Usuarios",
    en: "Users",
  },
}

type LanguageContextType = {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: string) => string
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export const LanguageProvider: React.FC<{
  children: React.ReactNode
  defaultLanguage?: Language
}> = ({ children, defaultLanguage = "es" }) => {
  const [language, setLanguage] = useState<Language>(defaultLanguage)

  // Load language preference from localStorage on client side
  useEffect(() => {
    const savedLanguage = localStorage.getItem("language") as Language
    if (savedLanguage && (savedLanguage === "es" || savedLanguage === "en")) {
      setLanguage(savedLanguage)
    }
  }, [])

  // Save language preference to localStorage
  useEffect(() => {
    localStorage.setItem("language", language)
  }, [language])

  // Translation function
  const t = (key: string): string => {
    if (!translations[key]) {
      console.warn(`Translation key not found: ${key}`)
      return key
    }
    return translations[key][language]
  }

  return <LanguageContext.Provider value={{ language, setLanguage, t }}>{children}</LanguageContext.Provider>
}

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error("useLanguage must be used within a LanguageProvider")
  }
  return context
}

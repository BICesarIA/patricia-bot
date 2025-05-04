"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Image from "next/image"
import { useLanguage } from "@/context/language-context"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts"

export default function Login() {
  const { t, language } = useLanguage()
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [accessType, setAccessType] = useState<"bi" | "bot" | "both">("both")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, you would authenticate the user here
    console.log("Login attempted with:", { email, accessType })

    // Redirect based on access type
    if (accessType === "bi") {
      router.push("/bi/dashboard")
    } else if (accessType === "bot") {
      router.push("/bot/dashboard")
    } else {
      // For "both" access type, default to BOT dashboard
      router.push("/bot/dashboard")
    }
  }

  // Sample data for the pie chart
  const data = [
    { name: "Sales", value: 35 },
    { name: "Marketing", value: 25 },
    { name: "Operations", value: 20 },
    { name: "Finance", value: 20 },
  ]

  const COLORS = ["#FFB84C", "#FFFFFF", "#FFD700", "#E5E5E5"]

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center text-gold">{t("loginTitle")}</h1>

          <div className="flex flex-col md:flex-row gap-12 items-center md:items-start">
            <div className="w-full md:w-1/2">
              <div className="bg-gray-900 p-8 rounded-lg border border-gray-800 shadow-xl">
                <h2 className="text-2xl font-semibold mb-6">{t("loginTitle")}</h2>

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium mb-2">
                      {t("email")}
                    </label>
                    <input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="form-input"
                      placeholder="your@email.com"
                    />
                  </div>

                  <div>
                    <label htmlFor="password" className="block text-sm font-medium mb-2">
                      {t("password")}
                    </label>
                    <input
                      id="password"
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      className="form-input"
                      placeholder="••••••••"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">{t("accessTo")}:</label>
                    <div className="flex space-x-4">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="accessType"
                          value="bi"
                          checked={accessType === "bi"}
                          onChange={() => setAccessType("bi")}
                          className="mr-2"
                        />
                        BI
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="accessType"
                          value="bot"
                          checked={accessType === "bot"}
                          onChange={() => setAccessType("bot")}
                          className="mr-2"
                        />
                        BOT
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="accessType"
                          value="both"
                          checked={accessType === "both"}
                          onChange={() => setAccessType("both")}
                          className="mr-2"
                        />
                        {language === "es" ? "Ambos" : "Both"}
                      </label>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <input
                        id="remember-me"
                        type="checkbox"
                        className="h-4 w-4 rounded border-gray-700 text-gold focus:ring-gold"
                      />
                      <label htmlFor="remember-me" className="ml-2 block text-sm">
                        {t("rememberMe")}
                      </label>
                    </div>

                    <a href="#" className="text-sm text-gold hover:underline">
                      {t("forgotPassword")}
                    </a>
                  </div>

                  <button
                    type="submit"
                    className="w-full py-3 px-4 rounded-md font-medium transition-colors bg-gold text-black hover:bg-gold/90"
                  >
                    {t("loginButton")}
                  </button>
                </form>
              </div>
            </div>

            <div className="w-full md:w-1/2">
              <div className="bg-gray-900 p-8 rounded-lg border border-gray-800 shadow-xl h-full">
                <div className="flex justify-center mb-6">
                  <Image
                    src="/images/cesaria-patricia.png"
                    alt="CESARIA.NET Bots"
                    width={200}
                    height={200}
                    className="object-contain"
                  />
                </div>

                <h2 className="text-2xl font-semibold mb-6">
                  {language === "es" ? "Beneficios de CESARIA.NET" : "CESARIA.NET Benefits"}
                </h2>

                <ul className="space-y-4 mb-8">
                  <li className="flex items-start">
                    <span className="text-2xl mr-3">📊</span>
                    <span>{language === "es" ? "Dashboards KPI interactivos" : "Interactive KPI dashboards"}</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-2xl mr-3">🤖</span>
                    <span>{language === "es" ? "Automatización de cobranzas" : "Collections automation"}</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-2xl mr-3">📱</span>
                    <span>{language === "es" ? "Integración con WhatsApp" : "WhatsApp integration"}</span>
                  </li>
                </ul>

                <div className="mt-8">
                  <h3 className="text-lg font-medium mb-4">
                    {language === "es" ? "Uso por Departamento" : "Usage by Department"}
                  </h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={data}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        >
                          {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

"use client"

import { useState } from "react"
import { useLanguage } from "@/context/language-context"
import Header from "@/components/Header"
import Footer from "@/components/Footer"

export default function Plans() {
  const { t, language } = useLanguage()
  const [activeTab, setActiveTab] = useState<"bi" | "bot">("bot")
  const [showQuoteForm, setShowQuoteForm] = useState(false)

  const botPlans = [
    {
      name: "Starter",
      whatsappMessages: 50,
      whatsappCost: 1.75,
      calls: 10,
      callsCost: 0.9,
      price: language === "es" ? "USD 50/mes" : "USD 50/month",
    },
    {
      name: "Pro",
      whatsappMessages: 150,
      whatsappCost: 5.25,
      calls: 20,
      callsCost: 1.8,
      price: language === "es" ? "USD 100/mes" : "USD 100/month",
    },
    {
      name: "Enterprise",
      whatsappMessages: 400,
      whatsappCost: 14,
      calls: 50,
      callsCost: 4.5,
      price: language === "es" ? "USD 200/mes" : "USD 200/month",
    },
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-12">
        <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center text-gold">{t("plansTitle")}</h1>

        <div className="max-w-5xl mx-auto">
          {/* Tabs */}
          <div className="flex border-b border-gray-700 mb-8">
            <button
              className={`py-2 px-4 font-medium ${
                activeTab === "bot" ? "text-gold border-b-2 border-gold" : "text-gray-400"
              }`}
              onClick={() => setActiveTab("bot")}
            >
              {t("botPlans")}
            </button>
            <button
              className={`py-2 px-4 font-medium ${
                activeTab === "bi" ? "text-gold border-b-2 border-gold" : "text-gray-400"
              }`}
              onClick={() => setActiveTab("bi")}
            >
              {t("biPlans")}
            </button>
          </div>

          {/* BOT Plans */}
          {activeTab === "bot" && (
            <div className="grid md:grid-cols-3 gap-6">
              {botPlans.map((plan) => (
                <div key={plan.name} className="card">
                  <h2 className="text-xl font-bold mb-4">{plan.name}</h2>
                  <div className="text-3xl font-bold mb-6 text-gold">{plan.price}</div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex justify-between">
                      <span>{language === "es" ? "Mensajes WhatsApp" : "WhatsApp Messages"}</span>
                      <span className="font-semibold">{plan.whatsappMessages}</span>
                    </li>
                    <li className="flex justify-between">
                      <span>{language === "es" ? "Costo WhatsApp (USD)" : "WhatsApp Cost (USD)"}</span>
                      <span className="font-semibold">${plan.whatsappCost}</span>
                    </li>
                    <li className="flex justify-between">
                      <span>{language === "es" ? "Llamadas (1.5min)" : "Calls (1.5min)"}</span>
                      <span className="font-semibold">{plan.calls}</span>
                    </li>
                    <li className="flex justify-between">
                      <span>{language === "es" ? "Costo Llamadas (USD)" : "Calls Cost (USD)"}</span>
                      <span className="font-semibold">${plan.callsCost}</span>
                    </li>
                  </ul>
                  <button className="w-full btn-gold">{language === "es" ? "Seleccionar" : "Select"}</button>
                </div>
              ))}
            </div>
          )}

          {/* BI Plans */}
          {activeTab === "bi" && (
            <div className="bg-gray-900 p-8 rounded-lg border border-gray-800 shadow-xl">
              <h2 className="text-2xl font-bold mb-6 text-center">
                {language === "es" ? "Soluciones BI Personalizadas" : "Custom BI Solutions"}
              </h2>
              <p className="text-gray-300 mb-6 text-center">
                {language === "es"
                  ? "Nuestras soluciones de Business Intelligence se adaptan a las necesidades específicas de su empresa."
                  : "Our Business Intelligence solutions are tailored to your company's specific needs."}
              </p>
              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div className="bg-gray-800 p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-4">
                    {language === "es" ? "Dashboards Power BI" : "Power BI Dashboards"}
                  </h3>
                  <ul className="space-y-2 mb-4">
                    <li>• {language === "es" ? "Visualizaciones interactivas" : "Interactive visualizations"}</li>
                    <li>
                      •{" "}
                      {language === "es"
                        ? "Conexión a múltiples fuentes de datos"
                        : "Connection to multiple data sources"}
                    </li>
                    <li>• {language === "es" ? "Actualizaciones automáticas" : "Automatic updates"}</li>
                  </ul>
                </div>
                <div className="bg-gray-800 p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-4">
                    {language === "es" ? "Consultoría Excel" : "Excel Consulting"}
                  </h3>
                  <ul className="space-y-2 mb-4">
                    <li>• {language === "es" ? "Automatización de reportes" : "Report automation"}</li>
                    <li>• {language === "es" ? "Fórmulas avanzadas" : "Advanced formulas"}</li>
                    <li>• {language === "es" ? "Macros y VBA" : "Macros and VBA"}</li>
                  </ul>
                </div>
              </div>
              <div className="text-center">
                <button onClick={() => setShowQuoteForm(true)} className="btn-gold">
                  {t("getQuote")}
                </button>
              </div>
            </div>
          )}

          {/* Quote Form Modal */}
          {showQuoteForm && (
            <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
              <div className="bg-gray-900 p-6 rounded-lg max-w-md w-full">
                <h3 className="text-xl font-bold mb-4">
                  {language === "es" ? "Solicitar Cotización" : "Request a Quote"}
                </h3>
                <form className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">{language === "es" ? "Nombre" : "Name"}</label>
                    <input type="text" className="form-input" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">
                      {language === "es" ? "Correo Electrónico" : "Email"}
                    </label>
                    <input type="email" className="form-input" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">{language === "es" ? "Teléfono" : "Phone"}</label>
                    <input type="tel" className="form-input" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">
                      {language === "es" ? "Empresa" : "Company"}
                    </label>
                    <input type="text" className="form-input" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">
                      {language === "es" ? "Mensaje" : "Message"}
                    </label>
                    <textarea className="form-input" rows={3}></textarea>
                  </div>
                  <div className="flex justify-end space-x-3 pt-2">
                    <button
                      type="button"
                      onClick={() => setShowQuoteForm(false)}
                      className="px-4 py-2 bg-gray-700 rounded-md"
                    >
                      {language === "es" ? "Cancelar" : "Cancel"}
                    </button>
                    <button type="submit" className="btn-gold">
                      {language === "es" ? "Enviar" : "Submit"}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}

"use client"

import { useLanguage } from "@/context/language-context"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Sidebar from "@/components/Sidebar"
import MobileSidebar from "@/components/MobileSidebar"
import DashboardCard from "@/components/DashboardCard"
import { Phone, MessageSquare, UserCheck, Clock, Users } from "lucide-react"

export default function BOTDashboard() {
  const { language } = useLanguage()

  // Mock data for the dashboard
  const kpiData = [
    {
      title: language === "es" ? "Total de Llamadas" : "Total Calls",
      value: "1,248",
      icon: <Phone size={24} className="text-gold" />,
      trend: { value: 12, isPositive: true },
    },
    {
      title: language === "es" ? "Llamadas Positivas" : "Positive Calls",
      value: "856",
      icon: <UserCheck size={24} className="text-green-500" />,
      trend: { value: 8, isPositive: true },
    },
    {
      title: language === "es" ? "Mensajes Enviados" : "Messages Sent",
      value: "3,429",
      icon: <MessageSquare size={24} className="text-blue-500" />,
      trend: { value: 15, isPositive: true },
    },
    {
      title: language === "es" ? "Duración Promedio" : "Avg. Call Duration",
      value: "2m 34s",
      icon: <Clock size={24} className="text-purple-500" />,
      trend: { value: 3, isPositive: false },
    },
    {
      title: language === "es" ? "Nuevos Clientes" : "New Customers",
      value: "27",
      icon: <Users size={24} className="text-blue-500" />,
      trend: { value: 10, isPositive: true },
    },
  ]

  const monthlyData = [
    {
      month: language === "es" ? "Abril 2025" : "April 2025",
      calls: 428,
      messages: 1245,
      successRate: "68%",
      revenue: "$12,450",
    },
    {
      month: language === "es" ? "Marzo 2025" : "March 2025",
      calls: 385,
      messages: 1102,
      successRate: "65%",
      revenue: "$10,820",
    },
    {
      month: language === "es" ? "Febrero 2025" : "February 2025",
      calls: 312,
      messages: 956,
      successRate: "62%",
      revenue: "$9,340",
    },
    {
      month: language === "es" ? "Enero 2025" : "January 2025",
      calls: 123,
      messages: 126,
      successRate: "58%",
      revenue: "$5,890",
    },
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <Header userName="Admin User" />

      <div className="flex flex-1">
        <Sidebar type="bot" />
        <MobileSidebar type="bot" />

        <main className="flex-1 p-6 bg-black overflow-y-auto">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-white">
              {language === "es" ? "Panel de Control BOT" : "BOT Dashboard"}
            </h1>
            <p className="text-gray-400">
              {language === "es"
                ? "Monitorea el rendimiento de tus bots y gestiona usuarios"
                : "Monitor your bot performance and manage users"}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mb-8">
            {kpiData.map((card, index) => (
              <DashboardCard key={index} title={card.title} value={card.value} icon={card.icon} trend={card.trend} />
            ))}
          </div>

          <div className="bg-gray-900 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">
              {language === "es" ? "Desglose Mensual" : "Monthly Breakdown"}
            </h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-800">
                <thead className="bg-gray-900">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      {language === "es" ? "Mes" : "Month"}
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      {language === "es" ? "Llamadas" : "Calls"}
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider hidden md:table-cell">
                      {language === "es" ? "Mensajes" : "Messages"}
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider hidden md:table-cell">
                      {language === "es" ? "Tasa de Éxito" : "Success Rate"}
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      {language === "es" ? "Ingresos" : "Revenue"}
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-gray-800 divide-y divide-gray-700">
                  {monthlyData.map((row, index) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">{row.month}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">{row.calls}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm hidden md:table-cell">{row.messages}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm hidden md:table-cell">{row.successRate}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">{row.revenue}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* External BI Report Placeholder */}
          <div className="bg-gray-900 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">
              {language === "es" ? "Informe BI Externo" : "External BI Report"}
            </h2>
            <div className="bg-gray-800 p-4 rounded-lg border border-gray-700 h-96 flex items-center justify-center">
              <div className="text-center">
                <p className="text-gray-400 mb-4">
                  {language === "es"
                    ? "Espacio reservado para el informe de Power BI"
                    : "Placeholder for Power BI report"}
                </p>
                <button className="btn-gold text-sm">
                  {language === "es" ? "Conectar Power BI" : "Connect Power BI"}
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>

      <Footer />
    </div>
  )
}

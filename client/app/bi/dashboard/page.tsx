"use client"

import { useLanguage } from "@/context/language-context"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Sidebar from "@/components/Sidebar"
import MobileSidebar from "@/components/MobileSidebar"
import UserTable from "@/components/UserTable"

// Mock data for the table
const users = [
  {
    id: "1",
    name: "John Doe",
    email: "john@example.com",
    role: "Admin",
    status: "active" as const,
    lastLogin: "2025-04-26 14:22",
  },
  {
    id: "2",
    name: "Jane Smith",
    email: "jane@example.com",
    role: "User",
    status: "active" as const,
    lastLogin: "2025-04-25 09:15",
  },
  {
    id: "3",
    name: "Bob Johnson",
    email: "bob@example.com",
    role: "User",
    status: "inactive" as const,
    lastLogin: "2025-04-20 11:30",
  },
  {
    id: "4",
    name: "Alice Brown",
    email: "alice@example.com",
    role: "Manager",
    status: "active" as const,
    lastLogin: "2025-04-26 16:45",
  },
  {
    id: "5",
    name: "Charlie Wilson",
    email: "charlie@example.com",
    role: "User",
    status: "active" as const,
    lastLogin: "2025-04-24 13:10",
  },
]

export default function BIDashboard() {
  const { language } = useLanguage()

  return (
    <div className="flex flex-col min-h-screen">
      <Header userName="Admin User" />

      <div className="flex flex-1">
        <Sidebar type="bi" />
        <MobileSidebar type="bi" />

        <main className="flex-1 p-6 bg-black">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gold">
              {language === "es" ? "Panel de Control BI" : "BI Dashboard"}
            </h1>
            <p className="text-gray-400">
              {language === "es" ? "Gestiona tus usuarios y accesos de BI" : "Manage your BI users and access"}
            </p>
          </div>

          <div className="bg-gray-900 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">{language === "es" ? "Usuarios" : "Users"}</h2>
            <UserTable users={users} type="bi" />
          </div>

          {/* Quote Section */}
          <div className="bg-gray-900 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">{language === "es" ? "Solicitar Cotización" : "Get a Quote"}</h2>
            <form className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                  <label className="block text-sm font-medium mb-1">{language === "es" ? "Empresa" : "Company"}</label>
                  <input type="text" className="form-input" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{language === "es" ? "Mensaje" : "Message"}</label>
                <textarea className="form-input" rows={3}></textarea>
              </div>
              <div>
                <button type="submit" className="btn-gold">
                  {language === "es" ? "Enviar Solicitud" : "Submit Request"}
                </button>
              </div>
            </form>
          </div>
        </main>
      </div>

      <Footer />
    </div>
  )
}

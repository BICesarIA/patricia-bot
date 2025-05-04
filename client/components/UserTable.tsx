"use client"

import { useState } from "react"
import { useLanguage } from "@/context/language-context"
import { LinkIcon, Lock, XCircle } from "lucide-react"

interface User {
  id: string
  name: string
  email: string
  role: string
  status: "active" | "inactive"
  lastLogin: string
}

interface UserTableProps {
  users: User[]
  type: "bi" | "bot"
}

export default function UserTable({ users, type }: UserTableProps) {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const { language } = useLanguage()

  const handleOpenModal = (user: User) => {
    setSelectedUser(user)
    setIsModalOpen(true)
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-800">
        <thead className="bg-gray-900">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
              {language === "es" ? "Nombre" : "Name"}
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider hidden md:table-cell">
              {language === "es" ? "Correo" : "Email"}
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider hidden md:table-cell">
              {language === "es" ? "Rol" : "Role"}
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
              {language === "es" ? "Estado" : "Status"}
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider hidden md:table-cell">
              {language === "es" ? "Último Acceso" : "Last Login"}
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">
              {language === "es" ? "Acciones" : "Actions"}
            </th>
          </tr>
        </thead>
        <tbody className="bg-gray-800 divide-y divide-gray-700">
          {users.map((user) => (
            <tr key={user.id} className="hover:bg-gray-700">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium">{user.name}</div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap hidden md:table-cell">
                <div className="text-sm text-gray-300">{user.email}</div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap hidden md:table-cell">
                <div className="text-sm text-gray-300">{user.role}</div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span
                  className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    user.status === "active" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                  }`}
                >
                  {user.status === "active"
                    ? language === "es"
                      ? "Activo"
                      : "Active"
                    : language === "es"
                      ? "Inactivo"
                      : "Inactive"}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300 hidden md:table-cell">
                {user.lastLogin}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex justify-end space-x-2">
                  <button onClick={() => handleOpenModal(user)} className="text-gold hover:text-gold/80" title="Links">
                    <LinkIcon size={18} />
                  </button>
                  <button className="text-blue-400 hover:text-blue-300" title="Reset Password">
                    <Lock size={18} />
                  </button>
                  <button className="text-red-400 hover:text-red-300" title="Disable">
                    <XCircle size={18} />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Links Modal */}
      {isModalOpen && selectedUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-900 p-6 rounded-lg w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">
              {language === "es"
                ? `Gestionar Enlaces para ${selectedUser.name}`
                : `Manage Links for ${selectedUser.name}`}
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span>Dashboard</span>
                <input type="checkbox" className="h-4 w-4" defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <span>{language === "es" ? "Reportes" : "Reports"}</span>
                <input type="checkbox" className="h-4 w-4" defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <span>{language === "es" ? "Analíticas" : "Analytics"}</span>
                <input type="checkbox" className="h-4 w-4" />
              </div>
              <div className="flex items-center justify-between">
                <span>{language === "es" ? "Configuración" : "Settings"}</span>
                <input type="checkbox" className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-6 flex justify-end space-x-3">
              <button onClick={() => setIsModalOpen(false)} className="px-4 py-2 bg-gray-700 rounded-md">
                {language === "es" ? "Cancelar" : "Cancel"}
              </button>
              <button onClick={() => setIsModalOpen(false)} className="px-4 py-2 bg-gold text-black rounded-md">
                {language === "es" ? "Guardar" : "Save"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

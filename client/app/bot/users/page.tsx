import type { Metadata } from "next"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Sidebar from "@/components/Sidebar"
import MobileSidebar from "@/components/MobileSidebar"
import UserTable from "@/components/UserTable"

export const metadata: Metadata = {
  title: "BOT Users | CESARIA.NET",
  description: "Manage BOT Suite Users",
  keywords: "AI, Artificial Intelligence, Bot, Chat, user management",
}

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
  {
    id: "6",
    name: "David Lee",
    email: "david@example.com",
    role: "User",
    status: "active" as const,
    lastLogin: "2025-04-23 10:05",
  },
  {
    id: "7",
    name: "Eva Garcia",
    email: "eva@example.com",
    role: "Manager",
    status: "active" as const,
    lastLogin: "2025-04-22 16:30",
  },
  {
    id: "8",
    name: "Frank Miller",
    email: "frank@example.com",
    role: "User",
    status: "inactive" as const,
    lastLogin: "2025-04-15 09:45",
  },
]

export default function BOTUsers() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header userName="Admin User" />

      <div className="flex flex-1">
        <Sidebar type="bot" />
        <MobileSidebar type="bot" />

        <main className="flex-1 p-6 bg-black">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-white">User Management</h1>
            <p className="text-gray-400">Manage BOT Suite users and their permissions</p>
          </div>

          <div className="bg-gray-900 rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Users</h2>
              <button className="btn-white text-sm py-2">Add New User</button>
            </div>
            <UserTable users={users} type="bot" />
          </div>
        </main>
      </div>

      <Footer />
    </div>
  )
}

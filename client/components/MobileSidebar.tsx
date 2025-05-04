"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { useLanguage } from "@/context/language-context"
import {
  Users,
  UserCog,
  MessageSquare,
  Phone,
  Upload,
  Calendar,
  BarChart3,
  LinkIcon,
  Menu,
  X,
  Tag,
  MessageCircle,
  ChevronDown,
  ChevronRight,
  UserCheck,
} from "lucide-react"

interface MobileSidebarProps {
  type: "bi" | "bot"
}

export default function MobileSidebar({ type }: MobileSidebarProps) {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()
  const { t } = useLanguage()
  const [patriciaOpen, setPatriciaOpen] = useState(false)
  const [cesariaOpen, setCesariaOpen] = useState(false)
  const [customerOpen, setCustomerOpen] = useState(false)

  const botLinks = [
    { href: "/bot/dashboard", label: t("dashboard"), icon: <BarChart3 size={18} /> },
    { href: "/bot/roles", label: t("roles"), icon: <UserCog size={18} /> },
    { href: "/bot/users", label: t("users"), icon: <Users size={18} /> },
  ]

  const patriciaLinks = [
    { href: "/bot/patricia/messages", label: "Messages", icon: <MessageSquare size={18} /> },
    { href: "/bot/patricia/labels", label: "Labels", icon: <Tag size={18} /> },
    { href: "/bot/patricia/conversations", label: "Conversations", icon: <MessageCircle size={18} /> },
  ]

  const customerLinks = [
    { href: "/bot/customers", label: "Customer Records", icon: <UserCheck size={18} /> },
    { href: "/bot/customers/reminders", label: "Reminders", icon: <Calendar size={18} /> },
  ]

  const cesariaLinks = [
    { href: "/bot/cesaria/configure", label: "Configure Number", icon: <Phone size={18} /> },
    { href: "/bot/cesaria/upload", label: "Upload Data", icon: <Upload size={18} /> },
    { href: "/bot/cesaria/schedule", label: "Schedules", icon: <Calendar size={18} /> },
  ]

  const biLinks = [
    { href: "/bi/dashboard", label: t("dashboard"), icon: <BarChart3 size={18} /> },
    { href: "/bi/users", label: t("users"), icon: <Users size={18} /> },
    { href: "/bi/links", label: "Links", icon: <LinkIcon size={18} /> },
  ]

  const links = type === "bi" ? biLinks : botLinks

  return (
    <div className="md:hidden">
      <button
        onClick={() => setIsOpen(true)}
        className="fixed top-4 left-4 z-40 p-2 bg-gray-900 rounded-md"
        aria-label="Open menu"
      >
        <Menu size={24} />
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-50">
          <div className="fixed inset-y-0 left-0 w-64 bg-gray-900 border-r border-gray-800 h-screen overflow-y-auto">
            <div className="flex justify-end p-4">
              <button onClick={() => setIsOpen(false)} aria-label="Close menu">
                <X size={24} />
              </button>
            </div>
            <div className="p-4">
              <h2 className="text-xl font-bold mb-6 text-gold">
                {type === "bi" ? "BI Admin Panel" : "BOT Admin Panel"}
              </h2>
              <nav className="space-y-1">
                {links.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`sidebar-link ${pathname === link.href ? "active" : ""}`}
                    onClick={() => setIsOpen(false)}
                  >
                    {link.icon}
                    <span>{link.label}</span>
                  </Link>
                ))}

                {type === "bot" && (
                  <>
                    {/* Customer Records Section */}
                    <div className="mt-6">
                      <button
                        onClick={() => setCustomerOpen(!customerOpen)}
                        className="sidebar-link w-full flex justify-between"
                      >
                        <div className="flex items-center">
                          <UserCheck size={18} className="mr-2" />
                          <span>Customer Records</span>
                        </div>
                        {customerOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                      </button>
                      {customerOpen && (
                        <div className="pl-4 mt-1 space-y-1">
                          {customerLinks.map((link) => (
                            <Link
                              key={link.href}
                              href={link.href}
                              className={`sidebar-link ${pathname === link.href ? "active" : ""}`}
                              onClick={() => setIsOpen(false)}
                            >
                              {link.icon}
                              <span>{link.label}</span>
                            </Link>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* PatriciaBOT Section */}
                    <div className="mt-6">
                      <button
                        onClick={() => setPatriciaOpen(!patriciaOpen)}
                        className="sidebar-link w-full flex justify-between"
                      >
                        <div className="flex items-center">
                          <MessageSquare size={18} className="mr-2" />
                          <span>PatriciaBOT</span>
                        </div>
                        {patriciaOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                      </button>
                      {patriciaOpen && (
                        <div className="pl-4 mt-1 space-y-1">
                          {patriciaLinks.map((link) => (
                            <Link
                              key={link.href}
                              href={link.href}
                              className={`sidebar-link ${pathname === link.href ? "active" : ""}`}
                              onClick={() => setIsOpen(false)}
                            >
                              {link.icon}
                              <span>{link.label}</span>
                            </Link>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* CesarIABOT Section */}
                    <div className="mt-2">
                      <button
                        onClick={() => setCesariaOpen(!cesariaOpen)}
                        className="sidebar-link w-full flex justify-between"
                      >
                        <div className="flex items-center">
                          <Phone size={18} className="mr-2" />
                          <span>CesarIABOT</span>
                        </div>
                        {cesariaOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                      </button>
                      {cesariaOpen && (
                        <div className="pl-4 mt-1 space-y-1">
                          {cesariaLinks.map((link) => (
                            <Link
                              key={link.href}
                              href={link.href}
                              className={`sidebar-link ${pathname === link.href ? "active" : ""}`}
                              onClick={() => setIsOpen(false)}
                            >
                              {link.icon}
                              <span>{link.label}</span>
                            </Link>
                          ))}
                        </div>
                      )}
                    </div>
                  </>
                )}
              </nav>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

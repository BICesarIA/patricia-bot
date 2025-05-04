import type { Metadata } from "next"
import Image from "next/image"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Sidebar from "@/components/Sidebar"
import MobileSidebar from "@/components/MobileSidebar"
import { Phone, Upload, Calendar } from "lucide-react"

export const metadata: Metadata = {
  title: "CesarIABOT | CESARIA.NET",
  description: "Configure and manage CesarIABOT calls",
  keywords: "AI, Artificial Intelligence, Bot, calls, automation",
}

export default function CesarIABOT() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header userName="Admin User" />

      <div className="flex flex-1">
        <Sidebar type="bot" />
        <MobileSidebar type="bot" />

        <main className="flex-1 p-6 bg-black">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">CesarIABOT</h1>
              <p className="text-gray-400">Configure call automation settings</p>
            </div>
            <div className="hidden md:block">
              <Image src="/images/cesaria-bot.png" alt="CesarIA Bot" width={100} height={100} />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-gray-900 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Phone size={20} className="mr-2 text-gold" /> Configure Number
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Phone Number</label>
                  <input
                    type="tel"
                    className="form-input"
                    placeholder="+1 (XXX) XXX-XXXX"
                    defaultValue="+1 (849) 286-6787"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Display Name</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="Display Name"
                    defaultValue="CesarIA Collections"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Caller ID</label>
                  <input type="text" className="form-input" placeholder="Caller ID" defaultValue="CESARIA.NET" />
                </div>
                <button className="btn-gold mt-2">Save Configuration</button>
              </div>
            </div>

            <div className="bg-gray-900 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Calendar size={20} className="mr-2 text-gold" /> Configure Schedules
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Active Days</label>
                  <div className="grid grid-cols-7 gap-1">
                    {["M", "T", "W", "T", "F", "S", "S"].map((day, index) => (
                      <button
                        key={index}
                        className={`py-2 rounded-md text-center ${
                          index < 5 ? "bg-gold text-black" : "bg-gray-800 text-gray-400"
                        }`}
                      >
                        {day}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Active Hours</label>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs text-gray-400 mb-1">Start Time</label>
                      <input type="time" className="form-input" defaultValue="08:00" />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-400 mb-1">End Time</label>
                      <input type="time" className="form-input" defaultValue="18:00" />
                    </div>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Call Frequency</label>
                  <select className="form-input">
                    <option>Once per day</option>
                    <option>Twice per day</option>
                    <option>Once per week</option>
                    <option>Custom</option>
                  </select>
                </div>
                <button className="btn-gold mt-2">Save Schedule</button>
              </div>
            </div>
          </div>

          <div className="bg-gray-900 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Upload size={20} className="mr-2 text-gold" /> Upload Data
            </h2>
            <div className="space-y-6">
              <div className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center">
                <div className="flex flex-col items-center">
                  <Upload size={40} className="text-gray-500 mb-4" />
                  <p className="mb-2">Drag and drop your Excel file here</p>
                  <p className="text-sm text-gray-500 mb-4">or</p>
                  <button className="btn-gold">Browse Files</button>
                  <p className="text-xs text-gray-500 mt-4">Supported formats: .xlsx, .xls, .csv (Max size: 10MB)</p>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-medium mb-3">Connect via API</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">API Endpoint</label>
                    <input type="text" className="form-input" placeholder="https://api.example.com/data" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">API Key</label>
                    <input type="password" className="form-input" placeholder="Enter API key" />
                  </div>
                </div>
                <button className="btn-gold mt-4">Connect API</button>
              </div>
            </div>
          </div>
        </main>
      </div>

      <Footer />
    </div>
  )
}

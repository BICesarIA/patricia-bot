"use client"

import Image from "next/image"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Sidebar from "@/components/Sidebar"
import MobileSidebar from "@/components/MobileSidebar"
import { MessageSquare, Tag } from "lucide-react"
import { useEffect, useRef, useState } from "react"
import axios from "axios"
import { formatDateTime } from "@/utils/formatDate"
import ChatWindow from "../chat/page"

type Message = {
  id: string;
  to: string;
  from_number: string;
  incoming_msg: string;
  response: string;
  type_response: string;
  created_at: string;
};

export default function PatriciaBOT() {
  const API_BASE_PROTOCOLE = process.env.NEXT_PUBLIC_API_PROTOCOLE
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL
  const [messages, setMessages] = useState<Message[]>([])
  const messageRef = useRef<Message[]>([])
  const [selectedChatNumber, setselectedChatNumber] = useState<string | null>(null);


  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const res = await axios.get(`${API_BASE_PROTOCOLE}${API_BASE_URL}/conversations/`)
        setMessages(res.data)
      } catch (error) {
        console.log(error)
      }
    }
    fetchMessages()

    const ws = new WebSocket(`wss://${API_BASE_URL}/ws`)
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "message") {
        setMessages((prevMessages) => {
          const index = prevMessages.findIndex(
            (msg) => msg.from_number === data.payload.from_number
          );

          if (index !== -1) {
            const updated = [...prevMessages];
            updated[index] = {
              ...updated[index],
              incoming_msg: data.payload.incoming_msg,
              response: data.payload.response,
              type_response: data.payload.type_response,
              created_at: data.payload.created_at,
            };
            return updated;
          } else {
            return [...prevMessages, data.payload];
          }
        })
      }
    }

    return () => ws.close()
  }, [])

  // setMessages((prev) => [...prev, data.payload])
  useEffect(() => {
    messageRef.current = messages
  }, [messages])

  return (
    <div className="flex flex-col min-h-screen">
      <Header userName="Admin User" />

      <div className="flex flex-1">
        <Sidebar type="bot" />
        <MobileSidebar type="bot" />

        <main className="flex-1 p-6 bg-black">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">PatriciaBOT</h1>
              <p className="text-gray-400">Monitor chat messages and conversations</p>
            </div>
            <div className="hidden md:block">
              <Image src="/images/patricia-bot.png" alt="Patricia Bot" width={100} height={100} />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
            <div className="lg:col-span-1 bg-gray-900 rounded-lg p-4">
              <h2 className="text-lg font-semibold mb-4 flex items-center">
                <Tag size={18} className="mr-2" /> Labels
              </h2>
              <div className="space-y-2">
                <button className="w-full text-left px-3 py-2 rounded-md bg-gray-800 hover:bg-gray-700">
                  All Messages
                </button>
              </div>
            </div>

            <div className="lg:col-span-3 bg-gray-900 rounded-lg p-4">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold flex items-center">
                  <MessageSquare size={18} className="mr-2" /> Messages
                </h2>
                {/* <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Search messages..."
                    className="px-3 py-1 text-sm bg-gray-800 border border-gray-700 rounded-md"
                  />
                  <button className="btn-white text-sm py-1 px-3">Search</button>
                </div> */}
              </div>

              <div className="space-y-3">
                {messages.map((message) => (
                  <div key={message["id"]} className="bg-gray-800 p-3 rounded-md hover:bg-gray-700 cursor-pointer"
                    onClick={() => setselectedChatNumber(message["from_number"])}>
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-medium">{message["from_number"]}</h3>
                        <p className="text-sm text-gray-400">{message["from_number"]}</p>
                      </div>
                      <div className="text-xs text-gray-400">
                        {formatDateTime(message["created_at"])}
                      </div>
                    </div>
                    <p className="mt-2 text-sm">{message["response"] || message["incoming_msg"]}</p>
                    <div className="flex justify-between items-center mt-2">
                      {/* <span
                        className={`text-xs px-2 py-1 rounded-full ${message.label === "Account"
                          ? "bg-blue-900 text-blue-200"
                          : message.label === "Payment"
                            ? "bg-green-900 text-green-200"
                            : message.label === "Technical"
                              ? "bg-purple-900 text-purple-200"
                              : message.label === "Support"
                                ? "bg-red-900 text-red-200"
                                : "bg-gray-700 text-gray-300"
                          }`}
                      >
                        {message.label}
                      </span> */}
                      {/* <span
                        className={`text-xs ${message.status === "Answered"
                          ? "text-green-400"
                          : message.status === "Pending"
                            ? "text-yellow-400"
                            : "text-red-400"
                          }`}
                      >
                        {message.status}
                      </span> */}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>

      <Footer />

      {selectedChatNumber && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-xl w-[90%] max-w-md h-[80%] relative">
            <button
              className="absolute top-2 right-2 text-gray-600 hover:text-gray-800"
              onClick={() => setselectedChatNumber(null)}
            >
              ✕
            </button>
            <ChatWindow currentUser={selectedChatNumber} />
          </div>
        </div>
      )}

    </div>
  )
}

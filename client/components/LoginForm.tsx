"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"

interface LoginFormProps {
  formId: string
  buttonId: string
  buttonText: string
  buttonColor: "gold" | "white"
  redirectPath: string
}

export default function LoginForm({ formId, buttonId, buttonText, buttonColor, redirectPath }: LoginFormProps) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const router = useRouter()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, you would authenticate the user here
    console.log("Login attempted with:", { email })
    router.push(redirectPath)
  }

  return (
    <div className="bg-gray-900 p-8 rounded-lg border border-gray-800 shadow-xl">
      <h2 className="text-2xl font-semibold mb-6">Sign In</h2>

      <form id={formId} onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-2">
            Email Address
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
            Password
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

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="remember-me"
              type="checkbox"
              className="h-4 w-4 rounded border-gray-700 text-gold focus:ring-gold"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm">
              Remember me
            </label>
          </div>

          <a href="#" className="text-sm text-gold hover:underline">
            Forgot password?
          </a>
        </div>

        <button
          id={buttonId}
          type="submit"
          className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${
            buttonColor === "gold" ? "bg-gold text-black hover:bg-gold/90" : "bg-white text-black hover:bg-gray-100"
          }`}
        >
          {buttonText}
        </button>
      </form>
    </div>
  )
}

import type { Metadata } from "next"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import LoginForm from "@/components/LoginForm"
import InfoSection from "@/components/InfoSection"

export const metadata: Metadata = {
  title: "Login - CesarIA BOT Suite | CESARIA.NET",
  description: "Access your AI-powered bots for sales, collections, and customer service",
  keywords: "AI, Artificial Intelligence, Bot, Chat, customer service, sales automation",
}

export default function LoginBOT() {
  const benefits = [
    { icon: "🤖", text: "Collection automation" },
    { icon: "📞", text: "Patricia bot (messages)" },
    { icon: "🧠", text: "CesarIA bot (calls)" },
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center text-white">CesarIA BOT Suite Login</h1>

          <div className="flex flex-col md:flex-row gap-12 items-center md:items-start">
            <div className="w-full md:w-1/2">
              <LoginForm
                formId="botLoginForm"
                buttonId="botLoginButton"
                buttonText="Login to BOT Platform"
                buttonColor="white"
                redirectPath="/bot/dashboard"
              />
            </div>

            <div className="w-full md:w-1/2">
              <InfoSection
                title="BOT Suite Benefits"
                benefits={benefits}
                chartTitle="Bot Interaction Metrics"
                imageSrc="/images/cesaria-patricia.png"
                imageAlt="CesarIA and Patricia Bots"
              />
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

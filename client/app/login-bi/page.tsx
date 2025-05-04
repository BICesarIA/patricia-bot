import type { Metadata } from "next"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import LoginForm from "@/components/LoginForm"
import InfoSection from "@/components/InfoSection"

export const metadata: Metadata = {
  title: "Login - CesarIA BI | CESARIA.NET",
  description: "Access your Business Intelligence dashboards and analytics tools",
  keywords: "powerbi, dashboard, Excel, BI, Business Intelligence, login",
}

export default function LoginBI() {
  const benefits = [
    { icon: "📊", text: "KPI Dashboards" },
    { icon: "📈", text: "Report Automation" },
    { icon: "🤖", text: "Real-time Processes" },
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center text-gold">CesarIA BI Login</h1>

          <div className="flex flex-col md:flex-row gap-12 items-center md:items-start">
            <div className="w-full md:w-1/2">
              <LoginForm
                formId="biLoginForm"
                buttonId="biLoginButton"
                buttonText="Login to BI Platform"
                buttonColor="gold"
                redirectPath="/bi/dashboard"
              />
            </div>

            <div className="w-full md:w-1/2">
              <InfoSection
                title="Business Intelligence Benefits"
                benefits={benefits}
                chartTitle="BI Usage by Department"
                imageSrc="/images/logo.png"
                imageAlt="CESARIA.NET Logo"
              />
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

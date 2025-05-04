"use client"

import Image from "next/image"
import Link from "next/link"
import { useLanguage } from "@/context/language-context"
import Header from "@/components/Header"
import Footer from "@/components/Footer"

export default function Home() {
  const { t, language } = useLanguage()

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="text-center mb-16">
          <div className="flex justify-center mb-8">
            <Image src="/images/logo.png" alt="CESARIA.NET" width={250} height={150} priority />
          </div>
          <h1 className="text-4xl md:text-6xl font-bold mb-8">{t("welcomeTitle")}</h1>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto mb-16">
          {/* BI Card */}
          <div className="card">
            <h2 className="text-gold text-2xl font-bold mb-4">{t("biTitle")}</h2>
            <p className="text-gray-300 mb-6 h-24">{t("biDescription")}</p>
            <Link href="/login" className="btn-gold inline-block">
              {t("exploreBi")}
            </Link>
          </div>

          {/* BOT Suite Card */}
          <div className="card">
            <h2 className="text-white text-2xl font-bold mb-4">{t("botTitle")}</h2>
            <p className="text-gray-300 mb-6 h-24">{t("botDescription")}</p>
            <Link href="/login" className="btn-white inline-block">
              {t("exploreBots")}
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-12 max-w-5xl mx-auto mb-16">
          <div className="flex flex-col items-center">
            <Image src="/images/cesaria-bot.png" alt="CesarIA Bot" width={200} height={200} className="mb-4" />
            <p className="text-center text-gray-300">{t("cesariaSubtext")}</p>
          </div>
          <div className="flex flex-col items-center">
            <Image src="/images/patricia-bot.png" alt="Patricia Bot" width={200} height={200} className="mb-4" />
            <p className="text-center text-gray-300">{t("patriciaSubtext")}</p>
          </div>
        </div>

        {/* About Me Section */}
        <div className="max-w-5xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-center mb-8">{t("about")}</h2>
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="md:w-1/3">
              <Image src="/images/profile.jpeg" alt="César Ramírez" width={300} height={400} className="rounded-lg" />
            </div>
            <div className="md:w-2/3">
              <h3 className="text-xl font-bold mb-4">César Ramírez</h3>
              <p className="text-gray-300 mb-4">
                {language === "es"
                  ? "Especialista en soluciones de Inteligencia de Negocios y automatización con IA. Con más de 10 años de experiencia en el desarrollo de dashboards, análisis de datos y sistemas de automatización para empresas."
                  : "Specialist in Business Intelligence solutions and AI automation. With over 10 years of experience in dashboard development, data analysis, and automation systems for businesses."}
              </p>
              <p className="text-gray-300">
                {language === "es"
                  ? "Fundador de CESARIA.NET, combinando el poder de Power BI con soluciones de IA para transformar la manera en que las empresas gestionan sus datos y procesos de comunicación con clientes."
                  : "Founder of CESARIA.NET, combining the power of Power BI with AI solutions to transform how businesses manage their data and customer communication processes."}
              </p>
            </div>
          </div>
        </div>

        {/* Logo Gallery Placeholder */}
        <div className="max-w-5xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-8">
            {language === "es" ? "Nuestros Clientes" : "Our Clients"}
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 justify-items-center">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-gray-800 w-32 h-16 rounded flex items-center justify-center">
                <span className="text-gray-500">Logo {i}</span>
              </div>
            ))}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

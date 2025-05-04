"use client"

import Link from "next/link"
import { Twitter, Linkedin, Instagram, Mail, Phone } from "lucide-react"
import { useLanguage } from "@/context/language-context"

export default function Footer() {
  const { t } = useLanguage()

  return (
    <footer className="bg-black py-8 border-t border-gray-800 mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center">
          <p className="text-center text-gold mb-6">{t("copyright")}</p>

          <div className="flex space-x-6 mb-4">
            <Link href="#" aria-label="Twitter" className="text-white hover:text-gold transition-colors">
              <Twitter size={20} />
            </Link>
            <Link href="#" aria-label="LinkedIn" className="text-white hover:text-gold transition-colors">
              <Linkedin size={20} />
            </Link>
            <Link href="#" aria-label="Instagram" className="text-white hover:text-gold transition-colors">
              <Instagram size={20} />
            </Link>
            <Link
              href="mailto:cramirez@cesaria.net"
              aria-label="Email"
              className="text-white hover:text-gold transition-colors"
            >
              <Mail size={20} />
            </Link>
            <Link
              href="https://wa.me/18492866787"
              aria-label="WhatsApp"
              className="text-white hover:text-gold transition-colors"
            >
              <Phone size={20} />
            </Link>
          </div>

          <div className="text-sm text-gray-500">
            <Link href="mailto:cramirez@cesaria.net" className="hover:text-gold transition-colors">
              cramirez@cesaria.net
            </Link>
            <span className="mx-2">|</span>
            <Link href="https://wa.me/18492866787" className="hover:text-gold transition-colors">
              +1 (849) 286-6787
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}

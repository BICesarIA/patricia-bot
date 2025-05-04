"use client"

import Image from "next/image"
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from "recharts"

interface Benefit {
  icon: string
  text: string
}

interface InfoSectionProps {
  title: string
  benefits: Benefit[]
  chartTitle: string
  imageSrc: string
  imageAlt: string
}

export default function InfoSection({ title, benefits, chartTitle, imageSrc, imageAlt }: InfoSectionProps) {
  // Sample data for the pie chart
  const data = [
    { name: "Sales", value: 35 },
    { name: "Marketing", value: 25 },
    { name: "Operations", value: 20 },
    { name: "Finance", value: 20 },
  ]

  const COLORS = ["#FFB84C", "#FFFFFF", "#FFD700", "#E5E5E5"]

  return (
    <div className="bg-gray-900 p-8 rounded-lg border border-gray-800 shadow-xl h-full">
      <div className="flex justify-center mb-6">
        <Image
          src={imageSrc || "/placeholder.svg"}
          alt={imageAlt}
          width={200}
          height={200}
          className="object-contain"
        />
      </div>

      <h2 className="text-2xl font-semibold mb-6">{title}</h2>

      <ul className="space-y-4 mb-8">
        {benefits.map((benefit, index) => (
          <li key={index} className="flex items-start">
            <span className="text-2xl mr-3">{benefit.icon}</span>
            <span>{benefit.text}</span>
          </li>
        ))}
      </ul>

      <div className="mt-8">
        <h3 className="text-lg font-medium mb-4">{chartTitle}</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

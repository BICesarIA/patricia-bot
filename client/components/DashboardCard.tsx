import type React from "react"
interface DashboardCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  trend?: {
    value: number
    isPositive: boolean
  }
}

export default function DashboardCard({ title, value, icon, trend }: DashboardCardProps) {
  return (
    <div className="dashboard-card">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-sm font-medium text-gray-400">{title}</h3>
          <p className="text-2xl font-bold mt-1">{value}</p>
          {trend && (
            <div className="flex items-center mt-1">
              <span className={`text-xs ${trend.isPositive ? "text-green-500" : "text-red-500"}`}>
                {trend.isPositive ? "+" : "-"}
                {trend.value}%
              </span>
              <span className="text-xs text-gray-400 ml-1">vs last month</span>
            </div>
          )}
        </div>
        <div className="p-2 bg-gray-800 rounded-lg">{icon}</div>
      </div>
    </div>
  )
}

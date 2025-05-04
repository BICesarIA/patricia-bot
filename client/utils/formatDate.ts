export function formatDateTime(dateString: string): string {
    return new Date(dateString).toLocaleString("es-DO", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    }).replace(",", " - :");
  }
  
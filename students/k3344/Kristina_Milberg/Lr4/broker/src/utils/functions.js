export function getOrderStatus(status) {
    const statuses = {
        Opened: "Открыт",
        Approved: "Подтверждён",
        Paid: "Оплачен",
        Delivered: "Доставлен"
    }
    return statuses[status] || "Unknown";
}

export function getOrderPaid(prePaid) {
    return prePaid ? "Есть" : "Нет"
}

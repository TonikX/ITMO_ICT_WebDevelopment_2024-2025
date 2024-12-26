export function getRoomType(type) {
    const types = {
        s: "Одиночная",
        d: "Двухместная",
        t: "Трёхместная"
    }
    return types[type] || "Unknown";
}

export function getDayOfWeek(dayOfWeek) {
    const days = {
        mon: "Понедельник",
        tue: "Вторник",
        wed: "Среда",
        thu: "Четверг",
        fri: "Пятница",
        sat: "Суббота",
        sun: "Воскресенье"
    }
    return days[dayOfWeek] || "Unknown";
}
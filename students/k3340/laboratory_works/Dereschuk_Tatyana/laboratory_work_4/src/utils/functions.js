export function getGroupStatus(result) {
    const statuses = {
        s: "Успех",
        f: "Неудача",
        o: "Другое",
    }
    return statuses[result] || "Не назначен";
}

export function getMemberStatus(result) {
    const statuses = {
        s: "Успех",
        f: "Неудача",
        e: "ЧС",
        o: "Другое",
    }
    return statuses[result] || "Не назначен";
}

export function getEmergencyStatus(result) {
    const statuses = {
        t: "Травма",
        l: "Смерть",
        m: "Пропал",
    }
    return statuses[result] || null;
}
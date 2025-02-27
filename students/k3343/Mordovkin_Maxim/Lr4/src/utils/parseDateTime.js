// src/utils/parseDateTime.js
export const parseDateTimeArray = (arr) => {
    if (!Array.isArray(arr) || arr.length < 6) return null;
    const [year, month, day, hour, minute, second] = arr;
    return new Date(year, month - 1, day, hour, minute, second); // Месяц корректируется
};

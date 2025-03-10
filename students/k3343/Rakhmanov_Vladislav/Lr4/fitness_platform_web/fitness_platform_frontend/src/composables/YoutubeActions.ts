function extractVideoId(videoURL: string): string | undefined {
    if (videoURL.includes('watch')) {
        return videoURL.split('watch?v=').pop()?.split('&')[0]
    }
    return videoURL.split('/').pop()?.split('?')[0]
}

export function convertVideoToThumbnail(videoURL: string) {
    return `https://img.youtube.com/vi/${extractVideoId(videoURL)}/mqdefault.jpg`
}
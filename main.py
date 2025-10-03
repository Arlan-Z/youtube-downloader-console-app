import asyncio
import os
from dotenv import load_dotenv
import yt_dlp

load_dotenv()
MAX_SIZE = os.getenv("MAX_SIZE", "2G")  

os.makedirs("videos", exist_ok=True)


async def download_video(url: str):
    print(f"▶ Начинаю загрузку: {url}")

    ydl_opts = {
        "outtmpl": "videos/%(title)s.%(ext)s",
        "format": f"bestvideo+bestaudio/best[filesize<{MAX_SIZE}]",
        "merge_output_format": "mp4",
        "noplaylist": False,  
    }

    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        print(f"✅ Загрузка завершена: {url}")
    except Exception as e:
        print(f"❌ Ошибка при загрузке {url}: {e}")


async def main():
    print("Введите ссылки (видео или плейлисты). Для выхода — 'exit'.")
    tasks = []

    while True:
        url = input("URL: ").strip()
        if url.lower() == "exit":
            break
        task = asyncio.create_task(download_video(url))
        tasks.append(task)

    if tasks:
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
import threading
from dotenv import load_dotenv
import yt_dlp

load_dotenv()
MAX_SIZE = os.getenv("MAX_SIZE", "2G")

os.makedirs("videos", exist_ok=True)

url_queue = asyncio.Queue()

async def download_video(url: str):
    print(f"▶ Начинаю загрузку: {url}")

    ydl_opts = {
        "outtmpl": "videos/%(title)s.%(ext)s",
        "format": f"bestvideo+bestaudio/best[filesize<{MAX_SIZE}]",
        "merge_output_format": "mp4",
        "noplaylist": False,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }

    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(
            None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url])
        )
        print(f"✅ Завершено: {url}")
    except Exception as e:
        print(f"❌ Ошибка при загрузке {url}: {e}")


async def worker():
    while True:
        url = await url_queue.get()   
        asyncio.create_task(download_video(url))


def input_thread():
    """Вводим ссылки без блокировки"""
    print("Вводите ссылки (Ctrl+C для выхода):")
    while True:
        try:
            url = input("URL: ").strip()
            if url:
                asyncio.run_coroutine_threadsafe(url_queue.put(url), asyncio.get_event_loop())
        except EOFError:
            break


async def main():
    threading.Thread(target=input_thread, daemon=True).start()
    await worker()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹ Работа завершена пользователем.")

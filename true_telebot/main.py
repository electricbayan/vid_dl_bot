import telebot
import yt_dlp
import os
import time


class TooLargeVideo(Exception):
    pass


def download_video(url, filename):  # Main function for downloading videos
    ydl_opts = {'outtmpl': f'videos\\{filename}.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    token = 'TOKEN'
    bot = telebot.TeleBot(token)  # Creating bot

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "Hi! This bot provides you to download videos from YouTube, Dzen and VK.\n"
                                          "To start using bot, send video URL.\n"
                                          "To get help type /help.")

    @bot.message_handler(commands=['help'])
    def help_msg(message):
        bot.send_message(message.chat.id, """
             Technical support: https://t.me/artemvolkovich
            """)

    @bot.message_handler(content_types=['text'])
    def send_video(message):  # Main func for sending videos
        try:
            bot.send_message(message.chat.id, 'Please, wait...')
            start_time = time.time()  # Time of downloading
            download_video(message.text, f'{message.from_user.id}')
            a = os.path.getsize(f'videos\\{message.from_user.id}.mp4') // (1024 ** 2)
            if a > 50:  # Checking if size is more than 50 Mb
                raise TooLargeVideo
            with open(f'videos\\{message.from_user.id}.mp4', 'rb') as f:  # Sending video
                bot.send_video(chat_id=message.chat.id, video=f, timeout=10000)
            end_time = time.time()
            bot.send_message(message.chat.id, f'Done! Running time: {round(end_time - start_time, 1)}s')
            os.remove(f'videos\\{message.from_user.id}.mp4')  # Remove downloaded video from videos\
        except TooLargeVideo:  # If user sent video larger than 50 Mb
            bot.send_message(message.chat.id, 'Video is too large to send (50Mb>)')
            if os.path.exists(f'videos\\{message.from_user.id}.mp4'):
                os.remove(f'videos\\{message.from_user.id}.mp4')
        except Exception:  # If user sent wrong URL
            bot.send_message(message.chat.id, 'Something went wrong')
            if os.path.exists(f'videos\\{message.from_user.id}.mp4'):
                os.remove(f'videos\\{message.from_user.id}.mp4')

    bot.infinity_polling()


if __name__ == '__main__':
    main()

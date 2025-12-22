
from django.core.management.base import BaseCommand
import asyncio
import logging


from Hubly_bot.main import main 

class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Бот остановлен")
        except Exception as e:
            print(f"Ошибка: {e}")
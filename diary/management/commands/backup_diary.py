import csv
import os
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Diary

class Command(BaseCommand):
    help="Backup Diary data"

    def handle(self, *args, **options):
        date=datetime.date.today().strftime('%Y%m%d')
        file_path=settings.BACK_UP_PATH+'diary_'+date+'.csv'
        os.makedirs(settings.BACK_UP_PATH, exist_ok=True)
        with open(file_path, 'w') as file:
            writer=csv.writer(file)
            header=[field.name for field in Diary._meta.fields]
            writer.writerow(header)
            diaries=Diary.objects.all()
            for diary in diaries:
                writer.writerow([str(diary.user),
                                 diary.title,
                                 diary.content,
                                 str(diary.photo1),
                                 str(diary.photo2),
                                 str(diary.photo3),
                                 str(diary.created_at),
                                 str(diary.updated_at),
                                 ])
    files=os.listdir(settings.BACK_UP_PATH)
    if len(files)>=settings.BACK_UP_PATH:
        files.sort()
        os.remove(settings.BACK_UP_PATH+files[0])

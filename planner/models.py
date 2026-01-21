from django.conf import settings
from django.db import models
from django.utils import timezone


class Event(models.Model):
    class Type(models.TextChoices):
        VACCINE = "vaccine", "疫苗"
        MEDICAL = "medical", "醫療 / 看診"
        CHECKUP = "checkup", "定期健檢"
        PARASITE = "parasite", "驅蟲 / 寄生蟲"
        GROOMING = "grooming", "美容 / 洗牙"
        TRAINING = "training", "訓練"
        TRAVEL = "travel", "旅遊 / 住宿"
        SOCIAL = "social", "聚會"
        BIRTHDAY = "birthday", "生日"
        HOLIDAY = "holiday", "節日"
        OTHER = "other", "其他"

    class Status(models.TextChoices):
        PLANNED = "planned", "未完成"
        DONE = "done", "已完成"
        CANCELED = "canceled", "已取消"

    pet = models.ForeignKey(
        "pets.Pets",
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name="寵物",
    )

    title = models.CharField(max_length=200, verbose_name="標題")
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.OTHER, verbose_name="類型")

    start_at = models.DateTimeField(verbose_name="開始時間")
    end_at = models.DateTimeField(null=True, blank=True, verbose_name="結束時間")
    all_day = models.BooleanField(default=False, verbose_name="全天")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED, verbose_name="狀態")

    description = models.TextField(blank=True, default="", verbose_name="說明")
    note = models.TextField(blank=True, default="", verbose_name="備註")
    remind_at = models.DateTimeField(null=True, blank=True, verbose_name="提醒時間")
    reminded_at = models.DateTimeField(null=True, blank=True, verbose_name="已提醒時間")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_events",
        verbose_name="建立者",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        ordering = ["-start_at", "-id"]
        indexes = [
            models.Index(fields=["pet", "start_at"]),
            models.Index(fields=["type", "start_at"]),
            models.Index(fields=["status", "remind_at", "reminded_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.pet} - {self.title} ({timezone.localtime(self.start_at):%Y-%m-%d %H:%M})"

    @property
    def day(self):
        return timezone.localtime(self.start_at).date()

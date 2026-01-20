from django.db import models
from django.utils import timezone


class DailyRecord(models.Model):
    class Mood(models.TextChoices):
        HAPPY = "happy", "快樂"
        CALM = "calm", "平靜"
        ANXIOUS = "anxious", "焦慮"
        ANGRY = "angry", "生氣"
        SAD = "sad", "悲傷"
        TIRED = "tired", "疲倦"
        HEAT = "heat", "發情"

    class PoopStatus(models.TextChoices):
        NORMAL = "normal", "正常"
        HARD = "hard", "偏硬"
        SOFT = "soft", "偏軟"
        DIARRHEA = "diarrhea", "稀便"
        CONSTIPATION = "constipation", "無法排便"

    SUPPLEMENT_CHOICES = [
        ("vitamin_a", "維生素A"),
        ("fish_oil", "魚油"),
        ("probiotics", "益生菌"),
        ("glucosamine", "葡萄糖胺"),
        ("l_lysine", "離胺酸"),
        ("taurine", "牛磺酸"),
        ("cranberry", "蔓越莓"),
        ("hairball", "排毛粉"),
        ("coq10", "輔酶Q10"),
        ("other", "其他"),
    ]

    pet = models.ForeignKey(
        "pets.Pets",
        on_delete=models.CASCADE,
        related_name="daily_records",
        verbose_name="寵物",
    )

    recorded_at = models.DateField(default=timezone.localdate, verbose_name="日期")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="體重(公斤)")
    water_ml = models.PositiveIntegerField(null=True, blank=True, verbose_name="飲水量(ml)")
    food_g = models.PositiveIntegerField(null=True, blank=True, verbose_name="飼料量(克)")
    supplements = models.CharField(max_length=300, null=True, blank=True, verbose_name="營養品(複選)")
    mood = models.CharField(max_length=20, choices=Mood.choices, null=True, blank=True, verbose_name="情緒")
    poop_and_pee_count = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="上廁所次數")
    poop_status = models.CharField(max_length=20, choices=PoopStatus.choices, null=True, blank=True, verbose_name="排便狀況")
    exercise_min = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="運動時間(分鐘)")
    medications = models.CharField(max_length=200, null=True, blank=True, verbose_name="藥品")
    note = models.TextField(null=True, blank=True, verbose_name="備註")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-recorded_at"]
        indexes = [
            models.Index(fields=["pet", "recorded_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.pet.name} - {self.recorded_at:%Y-%m-%d %H:%M}"

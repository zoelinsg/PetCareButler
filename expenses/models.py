from django.conf import settings
from django.db import models
from django.utils import timezone

class Expense(models.Model):

    CATEGORY_CHOICES = [
        ("eat", "飲食"),
        ("supplies", "用品"),
        ("medical", "醫療"),
        ("grooming", "美容"),
        ("transportation", "交通"),
        ("education", "教育"),
        ("entertainment", "娛樂"),
        ("travel", "旅遊"),
        ("other", "其他"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name="主人",
    )
    pet = models.ForeignKey(
        "pets.Pets",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
        verbose_name="寵物",
    )

    name = models.CharField(max_length=100, verbose_name="項目")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, verbose_name="類別")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金額")
    date = models.DateField(default=timezone.localdate, verbose_name="日期")
    notes = models.TextField(blank=True, default="", verbose_name="備註")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "開支"
        verbose_name_plural = "開支"
        ordering = ("-date", "-id")

    def __str__(self) -> str:
        pet_part = f"({self.pet.name}) " if self.pet_id else ""
        return f"{pet_part}{self.name} - {self.amount} - {self.date}"

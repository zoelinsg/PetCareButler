from django.conf import settings
from django.db import models

class Pets(models.Model):
    class Species(models.TextChoices):
        DOG = "dog", "狗"
        CAT = "cat", "貓"
        OTHER = "other", "其他"

    class Gender(models.TextChoices):
        MALE = "M", "公"
        FEMALE = "F", "母"
        UNKNOWN = "U", "不詳"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pets",
        verbose_name="主人",
    )

    name = models.CharField(max_length=50, verbose_name="名字")
    species = models.CharField(max_length=10, choices=Species.choices, default=Species.CAT, verbose_name="種類")
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNKNOWN, verbose_name="性別")
    breed = models.CharField(max_length=80, blank=True, null=True, verbose_name="品種")
    pet_chip = models.CharField(max_length=50, blank=True, null=True, verbose_name="晶片")
    birth_date = models.DateField(blank=True, null=True, verbose_name="生日")
    features = models.TextField(blank=True, null=True, verbose_name="特徵")
    remark = models.TextField(blank=True, null=True, verbose_name="備註")

    avatar = models.ImageField(
        upload_to="pets/avatars/",
        blank=True,
        null=True,
        verbose_name="頭像",
    )

    is_neutered = models.BooleanField(default=False, verbose_name="是否結紮")
    is_deceased = models.BooleanField(default=False, verbose_name="是否過世")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "寵物"
        verbose_name_plural = "寵物"
        ordering = ("-updated_at", "-id")

    def __str__(self) -> str:
        return f"{self.name}"

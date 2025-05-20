from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.CharField("Telegram ID", max_length=50, unique=True)
    first_name = models.CharField("Имя", max_length=100, blank=True)
    username = models.CharField("Юзернейм", max_length=100, blank=True)

    def __str__(self):
        return f"@{self.username or self.telegram_id}"

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"


class Coffee(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    image = models.URLField("Ссылка на изображение", blank=True)
    price = models.DecimalField("Цена", max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кофе"
        verbose_name_plural = "Кофе"


class Addon(models.Model):
    name = models.CharField("Название", max_length=100)
    price = models.DecimalField("Цена", max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Добавка"
        verbose_name_plural = "Добавки"


class Order(models.Model):
    user = models.ForeignKey(
        TelegramUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.user}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, verbose_name="Заказ", related_name='items',
        on_delete=models.CASCADE)
    coffee = models.ForeignKey(Coffee, verbose_name="Кофе",
                               on_delete=models.CASCADE)
    addons = models.ManyToManyField(Addon, verbose_name="Добавки", blank=True)

    def __str__(self):
        return f"{self.coffee.name} в заказе #{self.order.id}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

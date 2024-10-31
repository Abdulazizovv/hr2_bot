from django.db import models


class BotUser(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    language_code = models.CharField(max_length=10, blank=True, null=True, default='uz')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id


class BotAdmin(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    is_superadmin = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name


class Position(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


    
class UserRequest(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE) # user
    full_name = models.CharField(max_length=255) # ismi va familiyasi
    phone_number = models.CharField(max_length=255) #
    birth_year = models.CharField(max_length=255) # tug'ilgan yili
    position = models.CharField(max_length=255) # lavozim
    region = models.CharField(max_length=255) # viloyat
    nationality = models.CharField(max_length=255) # millati
    education = models.CharField(max_length=100) # ta'lim
    marriage = models.BooleanField(default=False) # oilaviy ahvoli
    first_answer = models.TextField(blank=True, null=True) # qaysi korxonalarda ishlaganligi
    salary = models.CharField(max_length=255) # kutayotgan maosh
    second_answer = models.TextField(blank=True, null=True) # qancha muddat ishlay olishi
    convince = models.BooleanField(default=False) # sudlanganlik
    driver_license = models.CharField(max_length=100) # haydovchilik guvohnomasi
    has_car = models.BooleanField(default=False) # mashina borligi
    english_level = models.CharField(max_length=25) # ingliz tili
    russian_level = models.CharField(max_length=25) # rus tili
    other_language = models.CharField(max_length=255) # boshqa tillar
    third_answer = models.CharField(max_length=25) # word dasturida ishlay olish darajasi
    fourth_answer = models.CharField(max_length=25) # excel dasturida ishlay olish darajasi
    c1_program_level = models.CharField(max_length=25) # C1 dasturida ishlay olish darajasi
    
    worked_furniture = models.BooleanField(default=False) # mebel korxonalari bilan ishlaganligi
    fifth_answer = models.TextField() # boshqa dasturlarda ishlay olish darajasi
    sixth_answer = models.TextField(null=True, blank=True) # qayerdan ma'lumot olishganligi
    image = models.CharField(max_length=255) # foydalanuvchi rasmi(telegram file id)
    file_id = models.CharField(max_length=255, blank=True, null=True) # fayl idsi

    created_at = models.DateTimeField(auto_now_add=True) # qachon yaratilganligi
    updated_at = models.DateTimeField(auto_now=True) # qachon yangilanganligi

    def __str__(self):
        return f'{self.user.full_name} - {self.position}'

    class Meta:
        ordering = ['-created_at']
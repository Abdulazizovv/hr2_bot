from botapp.models import BotUser, UserRequest, Position, BotAdmin
import logging

def add_user(user_id, username, full_name):
    user, created = BotUser.objects.get_or_create(user_id=user_id, username=username, full_name=full_name)
    return user


def get_user(user_id):
    try:
        user = BotUser.objects.get(user_id=user_id)
        return user
    except BotUser.DoesNotExist:
        return None
    

def set_user_language(user_id, language_code):
    user = get_user(user_id)
    if user:
        print("set_user_language: ", language_code)
        user.language_code = language_code
        user.save()
        return user
    return None


def add_position(position_name):
    try:
        position = Position.objects.create(name=position_name)
        return position
    except Exception as e:
        logging.error(e)
        return None
    

def get_position(position_id):
    try:
        position = Position.objects.get(id=position_id)
        return position
    except Position.DoesNotExist:
        return None
    

def get_all_positions():
    positions = Position.objects.all()
    return positions


def add_user_request(user_id, full_name, phone_number, is_worked, birth_year, position, region, nationality, education, marriage, first_answer, salary, second_answer, convince, driver_license, has_car, english_level, russian_level, other_language, third_answer, fourth_answer, c1_program_level, fifth_answer, sixth_answer, image, file_id):
    user = get_user(user_id)
    if user:
        try:
            user_request = UserRequest.objects.create(
            user=user,
            full_name=full_name,
            phone_number=phone_number,
            worked_furniture=is_worked,
            birth_year=birth_year,
            position=position,
            region=region,
            nationality=nationality,
            education=education,
            marriage=marriage,
            first_answer=first_answer,
            salary=salary,
            second_answer=second_answer,
            convince=convince,
            driver_license=driver_license,
            has_car=has_car,
            english_level=english_level,
            russian_level=russian_level,
            other_language=other_language,
            third_answer=third_answer,
            fourth_answer=fourth_answer,
            c1_program_level=c1_program_level,
            fifth_answer=fifth_answer,
            sixth_answer=sixth_answer,
            image=image,
            file_id=file_id
        )
            return user_request
        except Exception as e:
            logging.error(e)
            return None
    return None


def get_user_request(request_id):
    try:
        user_request = UserRequest.objects.get(id=request_id)
        data = {
            "id": user_request.id,
            "full_name": user_request.full_name,
            "phone_number": user_request.phone_number,
            "worked_furniture": user_request.worked_furniture,
            "birth_year": user_request.birth_year,
            "position": user_request.position,
            "region": user_request.region,
            "nationality":user_request.nationality,
            "education": user_request.education,
            "marriage": user_request.marriage,
            "first_answer": user_request.first_answer,
            "salary": user_request.salary,
            "second_answer": user_request.second_answer,
            "convince": user_request.convince,
            "driver_license": user_request.driver_license,
            "has_car": user_request.has_car,
            "english_level": user_request.english_level,
            "russian_level": user_request.russian_level,
            "other_language": user_request.other_language,
            "third_answer": user_request.third_answer,
            "fourth_answer": user_request.fourth_answer,
            "c1_program_level": user_request.c1_program_level,
            "fifth_answer": user_request.fifth_answer,
            "sixth_answer": user_request.sixth_answer,
            "image": user_request.image,
            "file_id": user_request.file_id
        }
        return data
    except UserRequest.DoesNotExist:
        return None



def add_bot_admin(user_id):
    user = get_user(user_id)
    if user:
        user.is_admin = True
        user.save()
        return user
    return None


def remove_bot_admin(user_id):
    user = BotUser.objects.get(id=user_id)
    if user:
        user.is_admin = False
        user.save()
        return user
    return None


def get_bot_admins():
    users = BotUser.objects.filter(is_admin=True)
    return list(users)


def get_bot_admins_id():
    users = BotUser.objects.filter(is_admin=True)
    return list(users.values_list('user_id', flat=True))


def fetch_todays_requests():
    from datetime import datetime
    requests = UserRequest.objects.filter(created_at__date=datetime.now().date())
    return requests


def fetch_all_users():
    users = BotUser.objects.all()
    return users


def fetch_all_requests():
    requests = UserRequest.objects.all()
    return requests



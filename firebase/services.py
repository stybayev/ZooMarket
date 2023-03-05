import firebase_admin

from firebase_admin import credentials

from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError, ExpiredIdTokenError, InvalidIdTokenError

'''
Создание сертификата учетных данных
'''
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "zoomarket-abb51",
    "private_key_id": "a92808817ab658b84a9e9cbebf5f84435d6427e0",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCUNGypGyRm3kWT\ncKUjFktbF5bCgEgvRomrzUMzaA4+lA2ZJ6qIEMj04MZZ9rUgX2NCJY8yMxFiRcJV\nsj2Tp81xoigt/zP3A4CLOZ2SBh7yi1FUAreX9Jjs85OW0J+0qpTEZzuwO6wKrDJi\nEc7pQg+RuqmgKhupM78ssFdRWoKidNbm6396tsPamC0Q1D+0XnRmrhTkkLUtKuIv\nKckymBTPre3nDdNRBNC3Z/dGNDC2rTLDMk0W/TmwOjcxbO8bCAScPDwARIFzyt1u\nxDGS7KkFMEQJFR6ZaORfahcMif6GQvBs8C+CUS8vIHv2qGDHr5wEJF9Uqt6FbMbH\nmm9mbEH1AgMBAAECggEAPoPYnAKHed7jcVyQQ/spAT0zikrraAm0k+QrJxmK/Kme\nDM8XF3shEW5pLNSstYGXEHVgcFfrSs1LOrPLVqfvOLIiibh/NoBjLhc5GLn9Puk2\nfp4AzJfQFA9w36qT23Ui+K/lFSMuoHffbs+9PFZx09Jtr9JjRZ2+0/50bqwjs5u6\nIDvxOS+rgW5ptBBxWYkp7GRE3aslsWt2kBWiY8mCVRdmJmhP3bpWGamiQw/ywvdk\n6LKXUXJnQOFflYSRYXNfH7aBqztw6J/FMY0VeLWTnSncBcjT8cCrn3206+kk0Bnc\nmxU0chHJfiyn2tIc1dwOju4pchmVCXbbdwe7A4Y9JwKBgQDD69SR9NuFx9RtRIst\ncM8IYCDQLi4FC72jGNqurm18Pr+aEvq2U98dbExTjA0McN3z7uKNT0iyMnTJPuOE\nu+XWfAnzcnxoj92S/INebNBG4NGwTP2ov1A0UKBr89XjUuqFfCsHtNdWgTU7rKxK\nVduG7kBZ+kPtgV6a8CvMnNOk2wKBgQDBpsSgSij311wXYPSnb45yBD6D64t9ogBz\nTmgobRl+1vhYUk7/d1r1bUDumI8JPgZT33FLfxsiC5bDCbNJmUlkjZyhnSOX90xP\nJJtHze/uKFZ49PTqtWVy1xZ9M2HaYBJXljNDAdr+DNnTzaLNQUzW0rfXLZ5QHYux\nQyJBZKaFbwKBgBlnkQ7EA1sbiE4K30krIY1ieZ7E/i6lURe+90xDTesYb9vYri3K\nPlogWt1SgbalRAKHbVUJfNGufTpDL1lcy/a96sRoif08+mw+1gH+dhtat5X2xcWF\n2S6Pbd3RpmBttf9NFH9RUcLjyjVMtKKG84pRhoKkUv6PEedhUSydAUyVAoGAORu0\nOs0D/esN5nsaS1JzwJ4NzZumHFutJFQIFXvvG9/Lh0hmsaICOgSJNJPbAs++z/dC\nExCd8NFYGZZ/wAGrijLU8ThFKeitIV3bSTarPiG5NpyOqbTrAQ37PNrtTZgtcJUD\n8wvWCDvD9VlcXImYXnXv704ttNSxwInazUwga5MCgYEAg1gccxpZeq5eNLu+28+9\n/rkl9PVaU1QeEqboz8HVFIe8Skml6WPU2ifg6Zyf4/+np6rgrn8wNu0tpHAdPiXl\njNXkYT+PYUmuW90iDY8oMLAsZ0SuiPBboXLpiayoh3fEme8w3ikG/GmIDA3r3GAb\nWacL45lNRvg8Mb9ELjryNZ0=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-bllgh@zoomarket-abb51.iam.gserviceaccount.com",
    "client_id": "106339462435372530409",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-bllgh%40zoomarket-abb51.iam.gserviceaccount.com"
})

'''
Подключение к приложению FireBase
'''

default_app = firebase_admin.initialize_app(cred)

'''
Функция для проверки id токена и получения от него сведений о пользователе
'''


def firebase_validation(id_token):
    '''
    Эта функция получает идентификатор токена, отправленный Firebase,
    и проверяет токен идентификатора, а затем проверяет, существует ли пользователь в
    Firebase или нет, если он существует, он возвращает True, иначе False
    '''
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        phone_number = decoded_token['phone_number']
        provider = decoded_token['firebase']['sign_in_provider']
        image = decoded_token.get('picture')
        name = decoded_token.get('name')

        user = auth.get_user(uid)
        email = user.email
        return {
            "status": True,
            "uid": uid,
            "email": email,
            "name": name,
            "provider": provider,
            "image": image,
            "phone_number": phone_number
        }

    except UserNotFoundError:
        return False

    except (ExpiredIdTokenError, InvalidIdTokenError):
        return False

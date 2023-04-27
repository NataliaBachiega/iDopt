from profiles.models import IdoptUser
from faker import Faker


def create_dummy_user() -> IdoptUser:
    '''
    Função para ajudar nos testes. Cria um usuário na base de dados.
    '''
    faker = Faker()
    
    user =  IdoptUser(
        username=faker.user_name()[:15],
        email=faker.email(),
    )
    user.set_password('12345678')
    user.save()
    
    return user

from profiles.models import IdoptUser
from posts.models import Post
from faker import Faker


def create_dummy_user() -> IdoptUser:
    '''
    Função para ajudar nos testes. Cria um usuário na base de dados.
    '''
    faker = Faker()
    
    user =  IdoptUser(
        username=faker.user_name()[:14],
        email=faker.email(),
    )
    user.set_password('12345678')
    user.save()
    
    return user

def create_dummy_post(author: IdoptUser, comment_of: Post = None) -> Post:
    '''
    Função para ajudar nos testes. Cria um post na base de dados.
    '''
    faker = Faker()
    
    post = Post(
        author=author,
        content=faker.text(max_nb_chars=280),
        comment_of=comment_of,
    )
    post.save()
    return post
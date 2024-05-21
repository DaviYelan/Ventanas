import random
from models.attention import Attention

def generate_random_attention(users, ventanilla):
    user = random.choice(users)
    return Attention(user, ventanilla)


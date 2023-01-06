from rooms.models import RoomType
from users.models import User


def create_roomTypeDog_with_user(
    # user: User,
    roomType_data: dict = None,
) -> RoomType:

    if not roomType_data:
        roomType_data = {
            "image": "img_url_2",
            "title": "Quarto Privativo (cães)",
            "description": "Busca conforto e privacidade para o seu cãozinho? O quarto privativo é a opção ideal!",
            "capacity": 2,
            "price": 250,
        }

        roomTypeDog = RoomType.objects.create(**roomType_data)

        return roomTypeDog


def create_roomTypeCat_with_user(roomType_data: dict = None) -> RoomType:

    if not roomType_data:
        roomType_data = {
            "image": "img_url_2",
            "title": "Quarto Privativo (gatos)",
            "description": "Quarto privativo de alto padrão para o seu felino aproveitar com classe!",
            "capacity": 2,
            "price": 250,
        }

        roomTypeCat = RoomType.objects.create(**roomType_data)

        return roomTypeCat


def create_roomTypeShared_with_user(roomType_data: dict = None) -> RoomType:

    if not roomType_data:
        roomType_data = {
            "image": "img_url_1",
            "title": "Quarto Compartilhado",
            "description": "Ótimo custo benefício, essa opção é ideal para você que deseja que o seu pet interaja com outros catioros!",
            "capacity": 30,
            "price": 120,
        }

        roomTypeShared = RoomType.objects.create(**roomType_data)

        return roomTypeShared

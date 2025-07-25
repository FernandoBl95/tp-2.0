# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    cardList=[] #Se arma una lista vista para agregar los nuevos elementos.
    
    for i in transport.getAllImages() : #Se recorre elemento por elemento de la lista con imagenes cruda.
        
        cardList.append(translator.fromRequestIntoCard(i)) #Transforma cada imagen en una card.
    return cardList    


# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    imagenesCard=getAllImages()
    if not name.strip(): #Si la busqueda es vacio, devuelve todas las cartas.
        return imagenesCard
    
    filtered_cards = []
    for card in imagenesCard:
        if card.name.lower().startswith(name.lower()): #Compara el nombre escrito por el usuario con el nombre de las cartas.
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        if type_filter in card.types:# debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
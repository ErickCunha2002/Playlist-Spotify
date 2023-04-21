import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp=spotipy.client.Spotify(
    auth_manager=SpotifyOAuth(
        client_id='209e9dd7e37b484f92696ed1cfea38b8',
        client_secret='4a70d5ba3b4f4296a27bc0844012d438',
        redirect_uri='http://example.com',
        scope='playlist-modify-private',
        show_dialog=True,
        cache_path='token.txt'
    ))
user_id = sp.current_user()["id"]

def Musicas(year):
    
    url=f'https://www.billboard.com/charts/hot-100/{year}'
    response=requests.get(url=url)
    soup=BeautifulSoup(response.text, 'html.parser')

    dados_musicas=soup.find_all('span', class_='a-no-trucate')
    musicas=[art.getText().strip() for art in dados_musicas]

    lista_uri=[]
    for n in range(len(musicas)):
        query=musicas[n]
        try:
            results = sp.search(q=query, type='track')
            uri = results['tracks']['items'][0]['uri']
            lista_uri.append(uri)
        except IndexError:
            print(f'{query} não existe.')
            
    playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
    sp.playlist_add_items(playlist_id=playlist["id"], items=lista_uri)
    print('Playlist criada com sucesso!')

    
continuar=True
while continuar:
    year=input('Digite o ano para o qual deseja viajar: ')
    if len(year) == 10:
        Musicas(year)
    else:
        print('Por favor, digite um ano correto! (YYYY-MM-DD)')
    
    
    


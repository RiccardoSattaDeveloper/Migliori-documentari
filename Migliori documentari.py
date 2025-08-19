import pandas as pd 
import numpy as np 

informazioni = pd.read_csv('title.basics.tsv.gz', sep='\t', nrows=10000) 

valutazioni = pd.read_csv('title.ratings.tsv.gz', sep='\t') 
 
filtro_film = informazioni['titleType'] == 'movie'  
film_base = informazioni[filtro_film].copy()

valutazioni['logNumVoti'] = np.log(valutazioni['numVotes'])  
valutazioni['averageRating'] /= valutazioni['averageRating'].max()  
valutazioni['logNumVoti'] /= valutazioni['logNumVoti'].max()  

valutazioni['RiccardoRating'] = valutazioni['averageRating'] * valutazioni['logNumVoti'] 

film_valutati = film_base.merge(valutazioni, on='tconst') 

filtro_documentary = film_valutati['genres'].str.contains('Documentary', na=False)  
film_documentary = film_valutati[filtro_documentary].copy()  

colonne_utili = {
    'primaryTitle': 'Titolo', 
    'startYear': 'Anno', 
    'runtimeMinutes': 'Durata_Minuti', 
    'genres': 'Generi', 
    'RiccardoRating': 'Punteggio di Riccardo'
}

film_documentary_finale = film_documentary[list(colonne_utili.keys())].copy() 
film_documentary_finale.rename(columns=colonne_utili, inplace=True) 

film_documentary_finale['Durata_Minuti'] = pd.to_numeric(film_documentary_finale['Durata_Minuti'], errors='coerce').fillna(0).astype(int)  
film_documentary_finale['Punteggio di Riccardo'] = pd.to_numeric(film_documentary_finale['Punteggio di Riccardo'], errors='coerce').fillna(0).round(2)  

film_documentary_finale = film_documentary_finale.sort_values(by='Punteggio di Riccardo', ascending=False) 

film_documentary_finale.to_csv('film_documentary.csv', index=False, sep=',', float_format='%.2f')
import json, re
d=json.load(open('raw.json'))
d['itinerary']=[r for r in d['itinerary'] if isinstance(r.get('Leg'),int)]
json.dump(d,open('raw.json','w'),indent=1,ensure_ascii=False)

CITY = {
 'Madrid':'Madrid, Spain','Madrid (start)':'Madrid, Spain','Madrid (end)':'Madrid, Spain',
 'Granada':'Granada, Spain','Seville':'Sevilla, Spain','Lisbon':'Lisboa, Portugal',
 'Porto':'Porto, Portugal','Haro':'Haro, La Rioja, Spain','Haro (La Rioja)':'Haro, La Rioja, Spain',
 'San Sebastian':'Donostia-San Sebastian, Spain','Atxondo (Bizkaia)':'Atxondo, Bizkaia, Spain',
 'Seville / Jerez':'Jerez de la Frontera, Spain','En route':'Spain',
}

# (query, daytrip, is_area)
OV = {
 ('Madrid','Sacha'):('Restaurante Sacha, Calle Juan Hurtado de Mendoza, Madrid',0,0),
 ('Madrid','Casa Dani'):('Mercado de la Paz, Calle de Ayala 28, Madrid',0,0),
 ('Madrid','Casa Dani (Mercado de la Paz)'):('Mercado de la Paz, Calle de Ayala 28, Madrid',0,0),
 ('Madrid','Cava Baja bars (La Latina)'):('Calle de la Cava Baja, Madrid',0,1),
 ('Madrid','Botin'):('Sobrino de Botin, Calle de Cuchilleros 17, Madrid',0,0),
 ('Madrid','Museo del Prado'):('Museo Nacional del Prado, Madrid',0,0),
 ('Madrid','Reina Sofia'):('Museo Nacional Centro de Arte Reina Sofia, Madrid',0,0),
 ('Madrid','Thyssen-Bornemisza'):('Museo Nacional Thyssen-Bornemisza, Madrid',0,0),
 ('Madrid','Royal Palace'):('Palacio Real de Madrid',0,0),
 ('Madrid','Retiro Park + Crystal Palace'):('Palacio de Cristal, Parque del Retiro, Madrid',0,0),
 ('Madrid','Mercado de la Paz / San Miguel'):('Mercado de San Miguel, Madrid',0,0),
 ('Granada','Bodegas Castaneda'):('Bodegas Castaneda, Calle Almireceros, Granada',0,0),
 ('Granada','Los Diamantes'):('Los Diamantes, Calle Navas, Granada',0,0),
 ('Granada','Bar Poe'):('Bar Poe, Calle Veronica de la Magdalena, Granada',0,0),
 ('Granada','El Bar de Fede'):('El Bar de Fede, Calle Marques de Gerona, Granada',0,0),
 ('Granada','La Riviera'):('Bar La Riviera, Calle Cetti Meriem, Granada',0,0),
 ('Granada','Ruta del Azafran'):('Ruta del Azafran, Paseo del Padre Manjon, Granada',0,0),
 ('Granada','Teterias (Albaicin)'):('Calle Calderaria Nueva, Granada',0,1),
 ('Granada','ALHAMBRA TICKETS'):('Alhambra, Granada',0,0),
 ('Granada','Alhambra + Nasrid Palaces'):('Palacios Nazaries, Alhambra, Granada',0,0),
 ('Granada','Generalife gardens'):('Generalife, Granada',0,0),
 ('Granada','Mirador de San Nicolas'):('Mirador de San Nicolas, Granada',0,0),
 ('Granada','Albaicin'):('Albaicin, Granada',0,1),
 ('Granada','Sacromonte + cave zambra'):('Sacromonte, Granada',0,1),
 ('Granada','Sacromonte zambra (flamenco in a cave)'):('Sacromonte, Granada',0,1),
 ('Granada','Granada Cathedral + Royal Chapel'):('Capilla Real de Granada',0,0),
 ('Granada','Mercado de San Agustín'):('Mercado de San Agustin, Granada',0,0),
 ('Granada','Hammam Al Andalus'):('Hammam Al Andalus, Calle Santa Ana, Granada',0,0),
 ('Granada','Sierra Nevada foothills drive'):('Sierra Nevada, Granada, Spain',1,1),
 ('Seville','Las Golondrinas'):('Las Golondrinas, Calle Antillano Campos, Triana, Sevilla',0,0),
 ('Seville','Las Golondrinas (Triana)'):('Las Golondrinas, Calle Antillano Campos, Triana, Sevilla',0,0),
 ('Seville','La Brunilda'):('La Brunilda Tapas, Calle Galera 5, Sevilla',0,0),
 ('Seville','Bodeguita Romero'):('Bodeguita Romero, Calle Harinas, Sevilla',0,0),
 ('Seville','Taberna la Plazuela'):('Plaza de Santa Isabel, Triana, Sevilla',0,0),
 ('Seville','Taberna la Plazuela (Triana)'):('Plaza de Santa Isabel, Triana, Sevilla',0,0),
 ('Seville','Pelayo Bar de Tapas'):('Calle Pelay Correa, Triana, Sevilla',0,0),
 ('Seville','Real Alcazar'):('Real Alcazar de Sevilla',0,0),
 ('Seville','Cathedral + Giralda'):('Catedral de Sevilla, Giralda',0,0),
 ('Seville','Flamenco - Casa del Flamenco'):('Casa del Flamenco, Calle Ximenez de Enciso, Sevilla',0,0),
 ('Seville','Plaza de Espana'):('Plaza de Espana, Sevilla',0,0),
 ('Seville','Barrio Santa Cruz'):('Barrio de Santa Cruz, Sevilla',0,1),
 ('Seville','Triana'):('Triana, Sevilla',0,1),
 ('Seville','Jerez sherry bodega day trip'):('Bodegas Gonzalez Byass, Jerez de la Frontera',1,0),
 ('Seville / Jerez','Sherry bodega (Gonzalez Byass)'):('Bodegas Gonzalez Byass, Jerez de la Frontera',1,0),
 ('Lisbon','O Velho Eurico'):('O Velho Eurico, Rua de Sao Cristovao, Lisboa',0,0),
 ('Lisbon','Cervejaria Ramiro'):('Cervejaria Ramiro, Avenida Almirante Reis 1, Lisboa',0,0),
 ('Lisbon','Marisqueira do Lis'):('Avenida Almirante Reis, Lisboa',0,0),
 ('Lisbon','Prado'):('Prado Restaurante, Travessa das Pedras Negras, Lisboa',0,0),
 ('Lisbon','Canalha'):('Canalha, Rua Bartolomeu Dias, Belem, Lisboa',0,0),
 ('Lisbon','Feitoria'):('Feitoria Restaurante, Altis Belem Hotel, Lisboa',0,0),
 ('Lisbon','Gambrinus'):('Gambrinus, Rua das Portas de Santo Antao 23, Lisboa',0,0),
 ('Lisbon','Black Sheep Lisboa'):('Praca das Flores, Lisboa',0,0),
 ('Lisbon','Vino Vero Lisboa'):('Vino Vero, Travessa do Monte, Graca, Lisboa',0,0),
 ('Lisbon','Senhor Uva'):('Senhor Uva, Rua Santo Amaro, Estrela, Lisboa',0,0),
 ('Lisbon','Manteigaria'):('Manteigaria, Rua do Loreto 2, Lisboa',0,0),
 ('Lisbon','O Trevo'):('O Trevo, Praca Luis de Camoes, Lisboa',0,0),
 ('Lisbon','As Bifanas do Afonso'):('Rua da Madalena, Lisboa',0,0),
 ('Lisbon','Casa das Bifanas'):('Casa das Bifanas, Praca da Figueira, Lisboa',0,0),
 ('Lisbon','Time Out Market'):('Time Out Market Lisboa, Mercado da Ribeira',0,0),
 ('Lisbon','Sao Jorge Castle (Alfama)'):('Castelo de Sao Jorge, Lisboa',0,0),
 ('Lisbon','Jeronimos Monastery (Belem)'):('Mosteiro dos Jeronimos, Lisboa',0,0),
 ('Lisbon','Belem Tower'):('Torre de Belem, Lisboa',0,0),
 ('Lisbon','Fado in Alfama'):('Parreirinha de Alfama, Beco do Espirito Santo, Lisboa',0,0),
 ('Lisbon','Alfama wandering + tram 28'):('Alfama, Lisboa',0,1),
 ('Lisbon','Sintra day trip'):('Palacio Nacional da Pena, Sintra',1,0),
 ('Lisbon','Cabo da Roca + Cascais'):('Cabo da Roca, Portugal',1,0),
 ('Lisbon','Evora day trip'):('Templo Romano de Evora, Evora',1,0),
 ('Porto','Ode Porto Wine House'):('Ode Porto Wine House, Largo do Terreiro, Porto',0,0),
 ('Porto','Adega Sao Nicolau'):('Adega Sao Nicolau, Rua Sao Nicolau, Porto',0,0),
 ('Porto','Cafe Santiago'):('Cafe Santiago, Rua Passos Manuel, Porto',0,0),
 ('Porto','Cafe Santiago or Brasao'):('Cafe Santiago, Rua Passos Manuel, Porto',0,0),
 ('Porto','Brasao Aliados'):('Brasao Cervejaria Aliados, Rua Ramalho Ortigao, Porto',0,0),
 ('Porto','Matosinhos seafood'):('Rua Heroismo, Matosinhos, Portugal',1,1),
 ('Porto','Matosinhos grilled fish'):('Rua Heroismo, Matosinhos, Portugal',1,1),
 ('Porto','O Buraco / Restaurante Antunes'):('Restaurante Antunes, Rua do Bonjardim, Porto',0,0),
 ('Porto','Port lodges - Vila Nova de Gaia'):('Taylor s Port, Rua do Choupelo, Vila Nova de Gaia',0,0),
 ('Porto',"Port lodge tasting (Taylor's / Graham's)"):('Taylor s Port, Rua do Choupelo, Vila Nova de Gaia',0,0),
 ('Porto','Douro Valley'):('Pinhao, Alijo, Portugal',1,1),
 ('Porto','Douro Valley wine day'):('Pinhao, Alijo, Portugal',1,1),
 ('Porto','Ribeira riverfront'):('Cais da Ribeira, Porto',0,1),
 ('Porto','Livraria Lello'):('Livraria Lello, Porto',0,0),
 ('Porto','Sao Bento station'):('Estacao de Sao Bento, Porto',0,0),
 ('Porto','Clerigos Tower'):('Torre dos Clerigos, Porto',0,0),
 ('Porto','Matosinhos / Foz beaches'):('Praia de Matosinhos, Portugal',1,1),
 ('Porto','Porto River Soul Hotel'):('Rua das Flores, Porto',0,0),
 ('San Sebastian','Martin Berasategui'):('Restaurante Martin Berasategui, Loidi Kalea, Lasarte-Oria',1,0),
 ('San Sebastian','Asador Etxebarri'):('Asador Etxebarri, Axpe, Atxondo, Bizkaia',1,0),
 ('Atxondo (Bizkaia)','Asador Etxebarri'):('Asador Etxebarri, Axpe, Atxondo, Bizkaia',1,0),
 ('San Sebastian','Ganbara'):('Ganbara, San Jeronimo Kalea 21, Donostia',0,0),
 ('San Sebastian','Ganbara downstairs dining room'):('Ganbara, San Jeronimo Kalea 21, Donostia',0,0),
 ('San Sebastian','La Cuchara de San Telmo'):('La Cuchara de San Telmo, 31 de Agosto Kalea, Donostia',0,0),
 ('San Sebastian','Txepetxa'):('Bar Txepetxa, Pescaderia Kalea, Donostia',0,0),
 ('San Sebastian','La Vina'):('La Vina, 31 de Agosto Kalea 3, Donostia',0,0),
 ('San Sebastian','Bar Gandarias'):('Bar Gandarias, 31 de Agosto Kalea 23, Donostia',0,0),
 ('San Sebastian','Jose Mari Taberna'):('Parte Vieja, Donostia-San Sebastian',0,0),
 ('San Sebastian','Pintxos crawl - old town'):('Parte Vieja, Donostia-San Sebastian',0,1),
 ('San Sebastian','Parte Vieja (old town)'):('Parte Vieja, Donostia-San Sebastian',0,1),
 ('San Sebastian','La Concha beach + promenade'):('Playa de la Concha, Donostia-San Sebastian',0,0),
 ('San Sebastian','Monte Igueldo funicular'):('Monte Igueldo, Donostia-San Sebastian',0,0),
 ('San Sebastian','Monte Urgull'):('Monte Urgull, Donostia-San Sebastian',0,0),
 ('San Sebastian','Bilbao / Guggenheim'):('Museo Guggenheim Bilbao',1,0),
 ('Haro','Barrio de la Estacion wineries'):('Barrio de la Estacion, Haro, La Rioja',0,1),
 ('Haro','Hotel Arrope'):('Hotel Arrope, Haro, La Rioja',0,0),
 ('En route','Cordoba - Mezquita'):('Mezquita-Catedral de Cordoba',1,0),
 ('En route','Coimbra'):('Universidade de Coimbra, Biblioteca Joanina',1,0),
 ('En route','Salamanca or Burgos'):('Plaza Mayor, Salamanca',1,0),
 ('Lisbon','Corinthia Lisbon'):('Corinthia Lisbon Hotel, Avenida Columbano Bordalo Pinheiro',0,0),
}

WINE_N=['bodega','port lodge','douro','winer','sherry','wine house','wine bar','vino','black sheep']
def cat(name,category,src):
    c=(category or '').lower(); n=name.lower()
    if src=='lodging' or 'lodging' in c or 'hotel' in n: return 'lodging'
    if 'wine' in c or 'tasting' in c or any(k in n for k in WINE_N): return 'wine'
    if src=='restaurant': return 'food'
    if src=='sight': return 'sight'
    FOODC=['market','pastry','bifana','tapas','pintxos','michelin','seafood','francesinha',
           'tasca','bistro','institution','local','refined','traditional','historic','grilled',
           'stall','crawl','dessert','tea house','old-world','neo-tasca','bar','food','portuguese','seasonal']
    if any(k in c for k in FOODC): return 'food'
    return 'sight'

pois={}
order=[]
def add(city,name,category,src,payload):
    if not name: return
    key=name.strip().lower()
    if key in pois:
        pois[key]['sources'][src]=payload
        if src=='sight' and pois[key]['category']=='food' and 'wine' not in (category or '').lower():
            pass
        return
    q,dt,area=OV.get((city,name),(None,0,0))
    if q is None: q=f"{name}, {CITY.get(city,city)}"
    pois[key]={'name':name,'city':city,'category':cat(name,category,src),
               'raw_category':category,'query':q,'daytrip':bool(dt),'area':bool(area),
               'sources':{src:payload}}
    order.append(key)

for r in d['restaurants']: add(r['City'],r['Restaurant'],r['Category'],'restaurant',r)
for r in d['sights']: add(r['City'],r['Site / Activity'],r['Category'],'sight',r)
for r in d['reservations']: add(r['City'],r['Restaurant / Booking'],r['Type'],'reservation',r)
for r in d['itinerary']:
    if r.get('Lodging') and r['Lodging']!='Apartment':
        c=r['City'].replace(' (start)','').replace(' (end)','').replace(' (La Rioja)','')
        add(c,r['Lodging'],'Lodging','lodging',r)

out=[pois[k] for k in order]
json.dump(out,open('pois.json','w'),indent=1,ensure_ascii=False)
print('unique POIs:',len(out))
from collections import Counter
print(Counter(p['category'] for p in out))
miss=[p for p in out if (p['city'],p['name']) not in OV]
print('no curated query:',len(miss))
for p in miss: print('  ->',p['city'],'|',p['name'],'|',p['query'])

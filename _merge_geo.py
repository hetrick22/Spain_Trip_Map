import json

# key = the curated query string in pois.json -> [lat, lon, osm_type, matched_name, exact?]
GEO = {
 # Madrid
 "Restaurante Sacha, Calle Juan Hurtado de Mendoza, Madrid":[40.460794,-3.687470,"restaurant","Sacha",1],
 "Mercado de la Paz, Calle de Ayala 28, Madrid":[40.426949,-3.685925,"restaurant","Casa Dani, Mercado de la Paz",1],
 "Calle de la Cava Baja, Madrid":[40.412364,-3.709246,"street","Calle de la Cava Baja",0],
 "Sobrino de Botin, Calle de Cuchilleros 17, Madrid":[40.414175,-3.707981,"restaurant","Botin",1],
 "Museo Nacional del Prado, Madrid":[40.413792,-3.692041,"museum","Museo del Prado",1],
 "Museo Nacional Centro de Arte Reina Sofia, Madrid":[40.408049,-3.694422,"museum","Reina Sofia",1],
 "Museo Nacional Thyssen-Bornemisza, Madrid":[40.416216,-3.694932,"museum","Museo Thyssen-Bornemisza",1],
 "Palacio Real de Madrid":[40.416740,-3.713622,"palace","Palacio Real de Madrid",1],
 "Palacio de Cristal, Parque del Retiro, Madrid":[40.413598,-3.682065,"attraction","Palacio de Cristal",1],
 "Mercado de San Miguel, Madrid":[40.415374,-3.709015,"marketplace","Mercado de San Miguel",1],
 # Granada
 "Bodegas Castaneda, Calle Almireceros, Granada":[37.176828,-3.596989,"restaurant","Bodegas Castaneda",1],
 "Los Diamantes, Calle Navas, Granada":[37.173730,-3.598333,"pub","Bar Los Diamantes (Navas)",1],
 "Bar Poe, Calle Veronica de la Magdalena, Granada":[37.174383,-3.603445,"restaurant","Bar Poe",1],
 "El Bar de Fede, Calle Marques de Gerona, Granada":[37.178722,-3.600192,"restaurant","El Bar de Fede",1],
 "Bar La Riviera, Calle Cetti Meriem, Granada":[37.177322,-3.597514,"pub","La Riviera",1],
 "Ruta del Azafran, Paseo del Padre Manjon, Granada":[37.178845,-3.590291,"restaurant","Ruta del Azafran",1],
 "Calle Calderaria Nueva, Granada":[37.177857,-3.596947,"street","Calle Caldereria Nueva",0],
 "Alhambra, Granada":[37.176055,-3.588110,"castle","Alhambra",1],
 "Palacios Nazaries, Alhambra, Granada":[37.177264,-3.589618,"castle","Palacios Nazaries",1],
 "Generalife, Granada":[37.176993,-3.585228,"attraction","Generalife",1],
 "Mirador de San Nicolas, Granada":[37.181041,-3.592662,"viewpoint","Mirador de San Nicolas",1],
 "Albaicin, Granada":[37.181569,-3.594667,"neighbourhood","Albaicin",0],
 "Sacromonte, Granada":[37.181872,-3.584990,"neighbourhood","Sacromonte",0],
 "Capilla Real de Granada":[37.176296,-3.598565,"place_of_worship","Capilla Real",1],
 "Mercado de San Agustin, Granada":[37.177782,-3.599383,"marketplace","Mercado de San Agustin",1],
 "Hammam Al Andalus, Calle Santa Ana, Granada":[37.177625,-3.593967,"spa","Hammam Al Andalus",1],
 "Sierra Nevada, Granada, Spain":[37.095511,-3.142543,"mountain_range","Sierra Nevada",0],
 # Seville
 "Las Golondrinas, Calle Antillano Campos, Triana, Sevilla":[37.384867,-6.005512,"restaurant","Bar Las Golondrinas",1],
 "La Brunilda Tapas, Calle Galera 5, Sevilla":[37.388319,-5.999398,"restaurant","La Brunilda",1],
 "Bodeguita Romero, Calle Harinas, Sevilla":[37.387069,-5.995660,"restaurant","Bodeguita Romero",1],
 "Plaza de Santa Isabel, Triana, Sevilla":[37.382568,-6.000755,"restaurant","Taberna La Plazuela",1],
 "Calle Pelay Correa, Triana, Sevilla":[37.382754,-6.000856,"street","Calle Pelay Correa, Triana",0],
 "Real Alcazar de Sevilla":[37.383210,-5.990183,"castle","Real Alcazar",1],
 "Catedral de Sevilla, Giralda":[37.385915,-5.993141,"place_of_worship","Catedral de Sevilla",1],
 "Casa del Flamenco, Calle Ximenez de Enciso, Sevilla":[37.386355,-5.988526,"theatre","Casa del Flamenco",1],
 "Plaza de Espana, Sevilla":[37.376974,-5.986940,"attraction","Plaza de Espana",1],
 "Barrio de Santa Cruz, Sevilla":[37.386230,-5.991630,"neighbourhood","Barrio de Santa Cruz",0],
 "Triana, Sevilla":[37.383452,-6.004067,"neighbourhood","Triana",0],
 "Bodegas Gonzalez Byass, Jerez de la Frontera":[36.680074,-6.142952,"winery","Bodegas Gonzalez Byass",1],
 # Lisbon
 "O Velho Eurico, Rua de Sao Cristovao, Lisboa":[38.712715,-9.135417,"restaurant","O Velho Eurico",1],
 "Cervejaria Ramiro, Avenida Almirante Reis 1, Lisboa":[38.720198,-9.135706,"restaurant","Cervejaria Ramiro",1],
 "Avenida Almirante Reis, Lisboa":[38.722437,-9.135526,"restaurant","Marisqueira do Lis",1],
 "Prado Restaurante, Travessa das Pedras Negras, Lisboa":[38.710563,-9.135024,"restaurant","Prado",1],
 "Canalha, Rua Bartolomeu Dias, Belem, Lisboa":[38.697397,-9.193712,"restaurant","Canalha",1],
 "Feitoria Restaurante, Altis Belem Hotel, Lisboa":[38.693057,-9.210710,"restaurant","Feitoria",1],
 "Gambrinus, Rua das Portas de Santo Antao 23, Lisboa":[38.715302,-9.139776,"restaurant","Gambrinus",1],
 "Praca das Flores, Lisboa":[38.715156,-9.151029,"bar","Black Sheep, Praca das Flores",1],
 "Vino Vero, Travessa do Monte, Graca, Lisboa":[38.718688,-9.130500,"bar","Vino Vero",1],
 "Senhor Uva, Rua Santo Amaro, Estrela, Lisboa":[38.714487,-9.156842,"restaurant","Senhor Uva",1],
 "Manteigaria, Rua do Loreto 2, Lisboa":[38.710764,-9.144062,"bakery","Manteigaria (Chiado)",1],
 "O Trevo, Praca Luis de Camoes, Lisboa":[38.710902,-9.143013,"restaurant","O Trevo",1],
 "Rua da Madalena, Lisboa":[38.711531,-9.135644,"fast_food","As Bifanas do Afonso",1],
 "Casa das Bifanas, Praca da Figueira, Lisboa":[38.714198,-9.137887,"cafe","Casa das Bifanas",1],
 "Time Out Market Lisboa, Mercado da Ribeira":[38.707093,-9.145897,"food_court","Time Out Market",1],
 "Castelo de Sao Jorge, Lisboa":[38.713926,-9.133483,"attraction","Castelo de Sao Jorge",1],
 "Mosteiro dos Jeronimos, Lisboa":[38.697758,-9.206624,"monastery","Mosteiro dos Jeronimos",1],
 "Torre de Belem, Lisboa":[38.691586,-9.215929,"fort","Torre de Belem",1],
 "Parreirinha de Alfama, Beco do Espirito Santo, Lisboa":[38.711478,-9.128022,"restaurant","Parreirinha de Alfama",1],
 "Alfama, Lisboa":[38.711770,-9.128380,"neighbourhood","Alfama",0],
 "Palacio Nacional da Pena, Sintra":[38.787568,-9.390565,"attraction","Palacio Nacional da Pena",1],
 "Cabo da Roca, Portugal":[38.780904,-9.499416,"locality","Cabo da Roca",1],
 "Templo Romano de Evora, Evora":[38.572635,-7.907339,"temple","Templo Romano de Evora",1],
 "Corinthia Lisbon Hotel, Avenida Columbano Bordalo Pinheiro":[38.738765,-9.166490,"hotel","Corinthia Lisbon",1],
 # Porto
 "Ode Porto Wine House, Largo do Terreiro, Porto":[41.140363,-8.614815,"restaurant","Ode Porto Wine House",1],
 "Adega Sao Nicolau, Rua Sao Nicolau, Porto":[41.140429,-8.614887,"restaurant","Adega Sao Nicolau",1],
 "Cafe Santiago, Rua Passos Manuel, Porto":[41.146431,-8.604772,"restaurant","Cafe Santiago",1],
 "Brasao Cervejaria Aliados, Rua Ramalho Ortigao, Porto":[41.149167,-8.611778,"restaurant","Brasao Aliados",1],
 "Rua Heroismo, Matosinhos, Portugal":[41.186999,-8.693099,"marketplace","Mercado de Matosinhos",0],
 "Restaurante Antunes, Rua do Bonjardim, Porto":[41.151994,-8.608161,"restaurant","Antunes",1],
 "Taylor s Port, Rua do Choupelo, Vila Nova de Gaia":[41.134340,-8.614403,"winery","Taylor's Port",1],
 "Pinhao, Alijo, Portugal":[41.191050,-7.545998,"village","Pinhao (Douro Valley)",0],
 "Cais da Ribeira, Porto":[41.140500,-8.611140,"attraction","Cais da Ribeira",0],
 "Livraria Lello, Porto":[41.146832,-8.614849,"shop","Livraria Lello",1],
 "Estacao de Sao Bento, Porto":[41.145480,-8.610522,"train_station","Estacao de Sao Bento",1],
 "Torre dos Clerigos, Porto":[41.145655,-8.614627,"tower","Torre dos Clerigos",1],
 "Praia de Matosinhos, Portugal":[41.176539,-8.692741,"beach","Praia de Matosinhos",0],
 "Rua das Flores, Porto":[41.143400,-8.613500,"street","Porto historic centre",0],
 # San Sebastian / Basque
 "Restaurante Martin Berasategui, Loidi Kalea, Lasarte-Oria":[43.266438,-2.015050,"restaurant","Martin Berasategui, Lasarte-Oria",1],
 "Asador Etxebarri, Axpe, Atxondo, Bizkaia":[43.115911,-2.598439,"restaurant","Asador Etxebarri, Axpe",1],
 "Ganbara, San Jeronimo Kalea 21, Donostia":[43.323404,-1.985532,"bar","Ganbara",1],
 "La Cuchara de San Telmo, 31 de Agosto Kalea, Donostia":[43.324501,-1.985299,"restaurant","La Cuchara de San Telmo",1],
 "Bar Txepetxa, Pescaderia Kalea, Donostia":[43.323771,-1.983978,"bar","Txepetxa",1],
 "La Vina, 31 de Agosto Kalea 3, Donostia":[43.324391,-1.984742,"restaurant","La Vina",1],
 "Bar Gandarias, 31 de Agosto Kalea 23, Donostia":[43.323994,-1.985767,"bar","Bar Gandarias",1],
 "Parte Vieja, Donostia-San Sebastian":[43.323245,-1.985193,"neighbourhood","Parte Zaharra (old town)",0],
 "Playa de la Concha, Donostia-San Sebastian":[43.317701,-1.986368,"beach","Playa de la Concha",1],
 "Monte Igueldo, Donostia-San Sebastian":[43.321044,-2.009651,"viewpoint","Monte Igueldo",1],
 "Monte Urgull, Donostia-San Sebastian":[43.325353,-1.988865,"hill","Monte Urgull",1],
 "Museo Guggenheim Bilbao":[43.268428,-2.934061,"museum","Museo Guggenheim Bilbao",1],
 # Haro / en route
 "Barrio de la Estacion, Haro, La Rioja":[42.581751,-2.850245,"neighbourhood","Barrio de la Estacion",0],
 "Hotel Arrope, Haro, La Rioja":[42.576767,-2.849418,"hotel","Hotel Arrope",1],
 "Mezquita-Catedral de Cordoba":[37.879026,-4.779453,"place_of_worship","Mezquita-Catedral de Cordoba",1],
 "Universidade de Coimbra, Biblioteca Joanina":[40.207122,-8.426522,"library","Biblioteca Joanina, Coimbra",1],
 "Plaza Mayor, Salamanca":[40.965028,-5.664056,"attraction","Plaza Mayor, Salamanca",1],
}

pois = json.load(open('pois.json'))
hit = miss = 0
for p in pois:
    g = GEO.get(p['query'])
    if g:
        p['lat'], p['lon'], p['osm_type'], p['matched'] = g[0], g[1], g[2], g[3]
        p['exact'] = bool(g[4]) and not p['area']
        hit += 1
    else:
        p['lat'] = p['lon'] = None
        p['exact'] = False
        p['matched'] = None
        miss += 1
        print('NO GEO:', p['city'], '|', p['name'], '|', p['query'])

# not in OpenStreetMap at all -- placed by hand, flagged approximate
MANUAL = {
 'jose mari taberna': (43.323500,-1.984500,'Parte Vieja, San Sebastian'),
 'porto river soul hotel': (41.143400,-8.613500,'Porto historic centre'),
}
for p in pois:
    k = p['name'].strip().lower()
    if k in MANUAL:
        p['lat'], p['lon'], p['matched'] = MANUAL[k][0], MANUAL[k][1], MANUAL[k][2]
        p['exact'] = False
        p['manual'] = True

json.dump(pois, open('pois_geo.json','w'), indent=1, ensure_ascii=False)
nogeo = [p for p in pois if p['lat'] is None]
approx = [p for p in pois if p['lat'] and not p['exact']]
print(f'\ngeocoded: {len(pois)-len(nogeo)}/{len(pois)}   exact: {sum(1 for p in pois if p.get("exact"))}   approximate: {len(approx)}   unplaced: {len(nogeo)}')
for p in approx: print('  ~', p['city'], '|', p['name'], '->', p['matched'])
for p in nogeo: print('  X', p['city'], '|', p['name'])

# sanity: everything must be inside the Iberian bounding box
BAD = [p for p in pois if p['lat'] and not (36.0 <= p['lat'] <= 44.0 and -9.6 <= p['lon'] <= -1.5)]
print('\noutside Iberia:', len(BAD))
for p in BAD: print('  !!', p['name'], p['lat'], p['lon'])

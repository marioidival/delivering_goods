# Entrega de mercadorias

## O Problema

Uma rede grande de varejo esta desenvolvendo um novo sistema de logística e sua ajuda é muito importante neste momento. Sua tarefa será desenvolver o novo sistema de entregas visando sempre o menor custo. Para popular sua base de dados o sistema precisa expor um web service que aceite o formato de malha logística (exemplo abaixo), nesta mesma requisição o requisitante deverá informar um nome para este mapa. É importante que os mapas sejam persistidos para evitar que a cada novo deploy todas as informações desapareçam. O formato de malha logística é bastante simples, cada linha mostra uma rota: ponto de origem, ponto de destino e distância entre os pontos em quilômetros.
```
A B 10
B D 15
A C 20
C D 30
B E 50
D E 30
```

Com os mapas carregados o requisitante irá procurar o menor valor de entrega e seu caminho, para isso ele passará o mapa, nome do ponto de origem, nome do ponto de destino, autonomia do caminhão (km/l) e o valor do litro do combustível, agora sua tarefa é criar este web service. Um exemplo de entrada seria, mapa SP, origem A, destino D, autonomia 10, valor do litro 2,50; a resposta seria a rota A B D com custo de 6,25.

## A Solução

O problema foi solucionado usando as seguintes tecnologias (e algoritmo):

* Python 3
* Django _(versão 1.10.4)_
* Django Rest Framework
* PostgreSQL
* Memcached
* Docker
* Dijkstra

### Motivações
- Python 3
-- É uma versão nova da linguagem Python e bem amadurecida, pronta para produção. Na comunidade ainda existe uma certa resistencia de alguns para o uso, mas essa versão vem repletas de melhorias e novas formas de solucionar problemas (novos e antigos).
- Djongo
-- O framework web escrito em Python mais popular e completo, com diversas features interessantes e que ajudam o programador a resolver problemas comuns no desenvolvimento Web de uma maneira divertida.
- Django Rest Framework
-- Pacote incremental para o framework Django, permitindo-o criar API's de maneira muito rapida.
- PostgreSQL
-- O banco de dados relacional mais robusto do mercado atualmente. Não tenho muita experiencia com outros do mercado.
- Memcached
-- Sistema de cache extremamente rapido e muito adotado em varias empresas. Existe o Redis tambem, porem o Djando se comporta melhor usando o Memcached.

- Docker
-- Uma ferramenta muito util que ajuda tanto no desenvolvimento, criando ambientes similares a produção, quanto em produção, ajudando a escalar aplicações mais facilmente usando containers.

- Dijkstra
-- Acredito que o algoritmo de Dijkstra se encaixa muito bem no problema de achar a distancia mais curta e acabei usando este algoritmo para resolver.

## Requisitos

* Docker
* Docker Compose

## Executando

```
cd delivering_goods/
 # A aplicação ficará em background
docker-compose up -d
 # Ira executar os migrations
docker-compose run web python manage.py migrate
```

## API
### POST /api/map
- Endpoind criado para salvar um novo mapa com sua malha logística
```
 # Exemplo com httpie 
 http localhost:8000/api/map name='SP' mesh='A B 10 B D 15 A C 20 C D 30 B E 50 D E 30'
 
 HTTP/1.0 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Date: Thu, 08 Dec 2016 21:09:35 GMT
Server: WSGIServer/0.2 CPython/3.5.2
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "id": 5,
    "mesh": "A B 10 B D 15 A C 20 C D 30 B E 50 D E 30",
    "name": "SP"
}
```

### GET /api/mesh
 - Endpoint criado para retornar o menor caminho/custo de um mapa com sua mapa logística
```
# Exemplo com httpie

http localhost:8000/api/mesh map=='SP' root=='A' destination=='D' autonomy=='10' gas=='2.50'

HTTP/1.0 200 OK
Allow: GET, OPTIONS
Cache-Control: max-age=900
Content-Type: application/json
Date: Thu, 08 Dec 2016 21:12:24 GMT
Expires: Thu, 08 Dec 2016 21:27:24 GMT
Last-Modified: Thu, 08 Dec 2016 21:12:24 GMT
Server: WSGIServer/0.2 CPython/3.5.2
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "mesh": "Route A B D coast 6.25"
}


```

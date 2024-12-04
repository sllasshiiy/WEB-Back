from flask import Blueprint, render_template, request, abort

lab7=Blueprint('lab7',__name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films=[
    {
        "title": "IT",
        "title_ru": "ОНО",
        "year": 2017,
        "description": "Когда в городке Дерри штата Мэн начинают пропадать дети,\
            несколько ребят сталкиваются со своими величайшими страхами — \
            не только с группой школьных хулиганов, но со злобным клоуном \
            Пеннивайзом, список жертв которого уходит вглубь веков."
    },
    {
        "title": "Bridge to Terabithia",
        "title_ru": "Мост в Терабитию",
        "year": 2006,
        "description": "Надежды ученика пятого класса Джесса Аарона стать \
            самым быстрым бегуном в классе разбились после того, \
            как новичок Лесли Берк одержала победу в соревнованиях.\
            Оснований для враждебности по отношению друг к друг у \
            Джесса и Лесли более чем достаточно, и тем не менее между \
            ними завязывается дружба. Как тут не подружиться, если \
            приходится быть королем и королевой в обнаруженном в лесу \
            волшебном царстве?"
    },
    {
        "title": "Desperate Housewives",
        "title_ru": "Отчаянные домохозяйки",
        "year": 2004,
        "description": "В центре событий - четыре современные домохозяйки,\
            которые живут в тихом пригороде и отчаянно ищут личного счастья."
    }
]

@lab7.route('/lab7/rest-api/films/',methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>',methods=['GET'])
def get_film(id):
    if id<0 or id>=len(films):
        abort(404)
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>',methods=['DELETE'])
def del_film(id):
    if id<0 or id>=len(films):
        abort(404)
    del films[id]
    return '',204

@lab7.route('/lab7/rest-api/films/<int:id>',methods=['PUT'])
def put_film(id):
    if id<0 or id>=len(films):
        abort(404)
    film=request.get_json()
    films[id]=film
    return films[id]

@lab7.route('/lab7/rest-api/films/',methods=['POST'])
def add_film():
    if id<0 or id>=len(films):
        abort(404)
    return films[id]
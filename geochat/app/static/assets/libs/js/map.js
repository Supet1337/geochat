ymaps.ready(init);
var myMap;
function init () {
geolocation = ymaps.geolocation;

    myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 11
    }, {
        balloonMaxWidth: 300,
        searchControlProvider: 'yandex#search'
    });
    $.ajax({
        url: "/ajax-circle-draw",
        success: function (result) {
            var json = $.parseJSON(result);

            geolocation.get({
                provider: 'browser',
                mapStateAutoApply: true
            }).then(function (result) {
                result.geoObjects.options.set('preset', 'islands#blueCircleIcon');
                objects = ymaps.geoQuery([
                {
                    type: 'Point',
                    coordinates: result.geoObjects.position
                }
                ]).addToMap(myMap);
            });
            $("#place-chat").html("");
            json.forEach(function(item, i, json) {
                if(json[i].is_private){
                    var myCircle = new ymaps.Circle([
                        [json[i].x, json[i].y],
                        json[i].diametr
                    ], {
                        balloonContentHeader: '<img alt="User Avatar" style="width: 32px; height: 32px;" class="rounded-circle user-avatar-xxl" src="'+json[i].image+'">'+json[i].name+'' +
                                                '<p> Участники: '+json[i].members+'/'+json[i].max_members+'</p>',
                        balloonContentBody:
                                                '<div>'+
                                                    '<form method="post" action="/join-room">'+
                                                    '{% csrf_token %}'+
                                                    '<input type="password" name="password" class="form-control" placeholder="пароль">'+
                                                    '<input type="hidden" name="id" value="'+json[i].id+'">'+
                                                    '<input type="submit" value="Присоединиться" class="btn btn-secondary">'+
                                                '</form>'+
                                                '</div>',
                        balloonContentFooter: '<sup>Geo Chat</sup>',
                        hintContent:[ json[i].name]
                    }, {
                        fillColor: "#ff2200",
                        fillOpacity: 0.5,
                        strokeColor: "#ff2200",
                        strokeOpacity: 0.8,
                        strokeWidth: 1
                    });
                }
                else{
                    var myCircle = new ymaps.Circle([
                        [json[i].x, json[i].y],
                        json[i].diametr
                    ], {
                        balloonContentHeader: '<img alt="User Avatar" style="width: 32px; height: 32px;" class="rounded-circle user-avatar-xxl" src="'+json[i].image+'">'+json[i].name+'' +
                        '<p> Участники: '+json[i].members+'/'+json[i].max_members+'</p>',
                        balloonContentBody:
                                                '<div>'+
                                                    '<form method="post" action="/join-room">'+
                                                    '{% csrf_token %}'+
                                                    '<input type="hidden" name="id" value="'+json[i].id+'">'+
                                                    '<input type="submit" value="Присоединиться" class="btn btn-secondary">'+
                                                '</form>'+
                                                '</div>',
                        balloonContentFooter: '<sup>Geo Chat</sup>',
                        hintContent:[ json[i].name]
                    }, {
                        fillColor: "#ff2200",
                        fillOpacity: 0.5,
                        strokeColor: "#ff2200",
                        strokeOpacity: 0.8,
                        strokeWidth: 1
                    });
                }
                myMap.geoObjects.add(myCircle);
                geolocation.get({
                    provider: 'browser',
                    mapStateAutoApply: true
                }).then(function (result) {
                    objects = ymaps.geoQuery([
                        {
                            type: 'Point',
                            coordinates: result.geoObjects.position
                        }
                    ]);
                    if(json[i].is_place){
                        var objectsInsideCircle = objects.searchInside(myCircle);
                        if (objectsInsideCircle._objects.length == 0){
                            myMap.geoObjects.remove(myCircle);
                        }
                        else{
                            if('+{{request.user.is_authenticated}}+'){
                                if(json[i].is_private){
                                    $("#place-chat").append('<li class="nav-item">'+
                                                    '<img alt="User Avatar" style="width: 32px; height: 32px;" class="rounded-circle user-avatar-xxl" src="'+json[i].image+'">' +
                                                    '<a class="nav-link">'+json[i].name+'</a>'+
                                                    '<p> Участники: '+json[i].members+'/'+json[i].max_members+'</p>' +
                                                    '<form method="post" action="/join-room">'+
                                                    '{% csrf_token %}'+
                                                    '<input type="password" name="password" class="form-control" placeholder="пароль">'+
                                                    '<input type="hidden" name="id" value="'+json[i].id+'">'+
                                                    '<input type="submit" value="Присоединиться" class="btn btn-secondary">'+
                                                    '</form>'+
                                                '</li>');
                                }
                                else{
                                    $("#place-chat").append('<li class="nav-item">'+
                                                            '<img alt="User Avatar" style="width: 32px; height: 32px;" class="rounded-circle user-avatar-xxl" src="'+json[i].image+'">'+
                                                            '<a class="nav-link">'+json[i].name+'</a>'+
                                                            '<p> Участники: '+json[i].members+'/'+json[i].max_members+'</p>' +
                                                            '<form method="post" action="/join-room">'+
                                                            '{% csrf_token %}'+
                                                            '<input type="hidden" name="id" value="'+json[i].id+'">'+
                                                            '<input type="submit" value="Присоединиться" class="btn btn-secondary">'+
                                                            '</form>'+
                                                            '</li>');
                                }
                            }
                        }
                    }
                });

            });
        }
});
$.ajax({
    url: "/ajax-circle-draw-joined",
    success: function (result) {
        var json = $.parseJSON(result);
        json.forEach(function(item, i, json) {
            var myCircle = new ymaps.Circle([
                [json[i].x, json[i].y],
                json[i].diametr
            ], {
                balloonContentHeader: '<img alt="User Avatar" style="width: 32px; height: 32px;" class="rounded-circle user-avatar-xxl" src="'+json[i].image+'">'+json[i].name+'' +
                                        '<p> Участники: '+json[i].members+'/'+json[i].max_members+'</p>',
                balloonContentBody:'<div>'+
                                    '<a href="../../../../room/'+json[i].id+'"><button style="width: 100%" class="btn btn-secondary" >Войти</button></a>'+
                                    '</div>',
                balloonContentFooter: '<sup>Geo Chat</sup>',
                hintContent:[ json[i].name]
            }, {
                fillColor: "#3caa3c",
                fillOpacity: 0.5,
                strokeColor: "#3caa3c",
                strokeOpacity: 0.8,
                strokeWidth: 1
            });
            myMap.geoObjects.add(myCircle);
        });
    }
});
    myMap.events.add('click', function (e) {
            var coords = e.get('coords');
            if (!myMap.balloon.isOpen()) {
            myMap.balloon.open(coords, {
                contentHeader:'Вы можете создать здесь чат!',
                contentBody:'<button type="button" class="btn btn-primary" onclick="create('+coords[0]+','+coords[1]+')" data-toggle="modal" data-target="#myModal1">Создать чат</button>',
                contentFooter:'<sup>Geo Chat</sup>',
            });
        }
        else {
            myMap.balloon.close();
        }

    });

}
function create(x,y){
    document.getElementById('x').value = x;
    document.getElementById('y').value = y;
}

function open_balloon(x1,x2,y1,y2){
        var x = parseFloat(x1+'.'+x2);
        var y = parseFloat(y1+'.'+y2);
        var myAction = new ymaps.map.action.Single({
          center: [x, y],
          zoom: 15
    });
    myMap.action.execute(myAction);
    }



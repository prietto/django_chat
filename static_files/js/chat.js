var ngApp = angular.module('myNgApp', []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});;
ngApp.controller('myController', function ($scope, $http) {
    $scope.messages = [];
    $scope.current_user = '';

    $scope.getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    $scope.add = function() {
        var f = document.getElementById('file').files[0],
            r = new FileReader();
    
        r.onloadend = function(e) {
          var data = e.target.result;
          console.log('data=> ',data);
          //send your binary data via $http or $resource or do anything else with it
        }
    
        r.readAsBinaryString(f);
    }



    $scope.showPreviewImg = (element) => {
        let reader = new FileReader();
        let file = element.files[0];
        reader.readAsDataURL(file);

        reader.onloadend = function (e) {
            // const formData = new FormData();
            // formData.append('file', file);
            // formData.append('generateAttach', true);
            $scope.carga_imagen(file);
        }
        
    }


    $scope.carga_imagen = function (imagen) {
        
        //$scope.formData.imagenes[imagen_index].valor = imagen.value;
        $scope.pre_message_img_url = '';
        $scope.loading_img = true;
        var url = '/upload_img/';
        let ERROR = 'Ocurrió un error durante el guardado de la imagen';
        var imagenformData = new FormData();
        imagenformData.append('imagen', imagen);
        $http({
            method: 'POST',
            data: imagenformData,
            url: url,
            headers: { 'Content-Type': undefined, "X-CSRFToken": $scope.getCookie('csrftoken'), }
            
        }).then(function successCallback(response) {
            console.log('response!=> ',response);
            try {
                if (response.data.status === true ) {
                    console.log(response.data.mensaje);

                    const newImg = {
                        "nombre": "",
                        "ruta": response.data.url,
                        "bloquear_nombre" : false,
                        "valor": "",
                    }
                    $scope.pre_message_img_url = response.data.url;
                    $scope.message = response.data.url;                   

                    //$scope.selectedIndex = imagen_index;
                    //$scope.formData.imagenes[imagen_index].ruta = response.data.url;
                } else {
                    console.log(ERROR);
                    
                }
            } catch (error) {
                console.log(ERROR);
            }
            $scope.loading_img = false;
        }, function errorCallback(response) {
            console.log('error=> ',ERROR);
            console.log(ERROR);
            $scope.loading_img = false;
        });

        $scope.$apply();
    };




    var socket;
    angular.element(document).ready(function(){
        $scope.scrolltoend();
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        socket = new WebSocket(protocol+':'+ window.location.host + '/chat/');
        socket.onopen = $scope.websocket_conn_ok;
        socket.onmessage = $scope.websocket_msg_received;

        $('#chat-box').on('submit', function (e) {
            console.log('submit');
            e.preventDefault();
            e.stopPropagation();
            const datos = {
                message: $scope.message,
                username: $scope.current_user,
                action: 'create'
            }
            socket.send(JSON.stringify(datos));
            $scope.message = ''
            $scope.pre_message_img_url = '';
            $scope.$apply();
            return false;
        })
    })




    $scope.delete_msg = (id) => {
        const datos = {
            id: id,
            message: '',
            username: $scope.current_user,
            action: 'delete'
        }
        socket.send(JSON.stringify(datos));        
    }

    $scope.scrolltoend = () => {
        $('#board').stop().animate({
            scrollTop: $('#board')[0].scrollHeight
        }, 800);
    }

    // angular.element(document).ready(function(){
    //     $scope.scrolltoend();
    //     $('#chat-box').on('submit', function (e) {
    //         e.preventDefault();
    //         e.stopPropagation();

    //         const message = $scope.message;
    //         $scope.send();
            
    //         return false;
    //     })
    // })


    $scope.send = () => {
        const sender_user = $scope.current_user;
        const message = $scope.message;
        const data = {
            sender_user, 
            message,            
        }

        $http({
            method: 'POST',
            url: '/api/create_message/',
            data: data,
            headers: {
                "X-CSRFToken": $scope.getCookie('csrftoken'),
            },
        }).then(function successCallback(response){
            if(response && response.status == 201){
                const data_msg = response.data;
                let new_msg = {
                    "id": data_msg.id,
                    "sender_user": data_msg.sender_user,
                    "message": data_msg.message,
                    "creation_date": data_msg.creation_date
                }
                $scope.messages.push(new_msg);
                $scope.scrolltoend();
                
            }
        }, function errorCallback(response){

        });

    }


    $scope.websocket_conn_ok = () => {
        console.log('LA CONEXION SE HA ESTABLECIDO');
    }

    $scope.websocket_msg_received = (e) => {
        datos = JSON.parse(e.data)
        console.log('websocket_msg_received=> ',datos);
        const action = datos.action;

        if(action == 'create'){
            let new_msg = {
                "id": datos.id,
                "sender_user": datos.username,
                "message": datos.message,
                "creation_date": datos.creation_date
            }
            
            //new_msg['message'] ="<img src='"+datos.message+"' />"
            $scope.messages.push(new_msg);
            $scope.$apply();
            $scope.scrolltoend();
        }

        if(action == 'delete'){
            $scope.messages = $scope.messages.filter(m => m.id !== datos.id)
            $scope.$apply();
        }
        
    }

});

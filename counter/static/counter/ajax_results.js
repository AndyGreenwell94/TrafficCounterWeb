var table = $('#res').DataTable({
    paging: false,
    searching: false,
    language: {
                  "processing": "Подождите...",
                  "search": "Поиск:",
                  "lengthMenu": "Показать _MENU_ записей",
                  "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
                  "infoEmpty": "Записи с 0 до 0 из 0 записей",
                  "infoFiltered": "(отфильтровано из _MAX_ записей)",
                  "infoPostFix": "",
                  "loadingRecords": "Загрузка записей...",
                  "zeroRecords": "Записи отсутствуют.",
                  "emptyTable": "В таблице отсутствуют данные",
                  "paginate": {
                    "first": "Первая",
                    "previous": "Предыдущая",
                    "next": "Следующая",
                    "last": "Последняя"
                  },
                  "aria": {
                    "sortAscending": ": активировать для сортировки столбца по возрастанию",
                    "sortDescending": ": активировать для сортировки столбца по убыванию"
                  }
    } ,
});

$(document).ready( function () {
} );


$('#post-form').on('submit', function(event){
    event.preventDefault();
    create_post();
});

function create_post() {
    var date1 = $("#dp1").data("DateTimePicker").date().format('YYYY-MM-DD HH:mm:ss');
    var date2 = $("#dp2").data("DateTimePicker").date().format('YYYY-MM-DD HH:mm:ss');
    var zoneList = $("#zoneSelect").val();

    $.ajax({
         // the endpoint
        type : "POST", // http method
        data : {
            dateres1 : date1,
            dateres2 : date2,
            zones: zoneList

                }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity chec
            table.destroy();
            $('#res thead th').remove();
            $('#res tbody').remove();
            $.each(json.header, function (index, value) {
                $('#res thead').find('tr').append('<th>'+value.title+ '</th>');
            });

            table = $('#res').DataTable({
                data: json.table,
                destroy: true,
                paging: true,
                searching: false,
                "processing": true,
                "serverSide": false,
                 language: {
                              "processing": "Подождите...",
  "search": "Поиск:",
  "lengthMenu": "Показать _MENU_ записей",
  "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
  "infoEmpty": "Записи с 0 до 0 из 0 записей",
  "infoFiltered": "(отфильтровано из _MAX_ записей)",
  "infoPostFix": "",
  "loadingRecords": "Загрузка записей...",
  "zeroRecords": "Записи отсутствуют.",
  "emptyTable": "В таблице отсутствуют данные",
  "paginate": {
    "first": "Первая",
    "previous": "Предыдущая",
    "next": "Следующая",
    "last": "Последняя"
  },
  "aria": {
    "sortAscending": ": активировать для сортировки столбца по возрастанию",
    "sortDescending": ": активировать для сортировки столбца по убыванию"
  }
                        }
            });
        },

        error : function(xhr,errmsg,err) {
            console.log('err'); // provide a bit more info about the error to the console
        }
    });
};


function download_results(cam) {
    var date1 = $("#dp1").data("DateTimePicker").date().format('YYYY-MM-DD HH:mm:ss');
    var date2 = $("#dp2").data("DateTimePicker").date().format('YYYY-MM-DD HH:mm:ss');
    var zoneList = $("#zoneSelect").val();
    $.ajax({
        url : '/counter/'+cam+'/getres/',
        type : "POST", // http method
        data : {
            dateres1 : date1,
            dateres2 : date2,
            zones: zoneList

                },
        success :function (data) {
                    var hiddenElement = document.createElement('a');
                    hiddenElement.href = 'data:attachment/csv;charset=utf-8,%EF%BB%BF' + encodeURI(data);
                    hiddenElement.target = '_blank';
                    hiddenElement.download = 'Результаты.csv';
                    document.body.appendChild(hiddenElement)
                    hiddenElement.click();
        },
        error : function(xhr,errmsg,err) {
            console.log('err'); // provide a bit m  ore info about the error to the console
        }
    });// data sent with the post request
};


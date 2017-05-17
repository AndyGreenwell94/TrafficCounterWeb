/**
 * Created by Andy on 22-Sep-16.
 */
$(document).ready(function () {
    var tableAvail = $('#camsTab').DataTable({
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
        searching: false,
        "lengthChange": false,
        "columnDefs": [
            {
                "targets": [ 0 ],
                "visible": false,
                "searchable": false
            }]
    });
    var tableSetup = $('#camsAddedTab').DataTable({
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
        searching: false,
        "lengthChange": false,
        "columnDefs": [
            {
                "targets": [ 0 ],
                "visible": false,
                "searchable": false
            }]
    });
    $('#camsTab tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    });
    $('#camsAddedTab tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    });

    $('#tableSend').click(function () {
        selCams = [];
        tableAvail.rows('.selected').data().each(function (index) {
            selCams.push(index[0]);
        });
        delCams = [];
        tableSetup.rows('.selected').data().each(function (index) {
            delCams.push(index[0]);
        });
        $.ajax({
            type: "POST",
            data: {
                'selCams': selCams,
                'delCams': delCams
            },
            success: function (json) {
                //alert(json.message);
                location.reload();
            },
            error: function () {
                alert('Что-то пошло не так')
            }
        });
    })
});
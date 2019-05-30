var table;
$(document).ready(function (){

    table = $('#example').DataTable( {
        select: true,
        buttons: [
            {
                text: 'Select all',
                action: function () {
                    table.rows().select();
                }
            },
            {
                text: 'Select none',
                action: function () {
                    table.rows().deselect();
                }
            }
        ]
    } );
});

function Download() {

    var url = $.map(table.rows('.selected').data(), function (item) {
        return item[5];
    });
    var names = $.map(table.rows('.selected').data(), function (item) {
        return item[0];
    });
    var duration = $.map(table.rows('.selected').data(), function (item) {
        return item[1];
    });
    var views = $.map(table.rows('.selected').data(), function (item) {
        return item[2];
    });
    var cmnts = $.map(table.rows('.selected').data(), function (item) {
        return item[4];
    });
    var likes = $.map(table.rows('.selected').data(), function (item) {
        return item[3];
    });
    let videoList = [];
    let durationList = [];
    let ViewsList = [];
    let CommentsList = [];
    let LikesList = [];
    if(url.length === 0){
        alert("Select One video at least");
        return;
    }
    else {
        for(var video in url){
            let lenght = url[video].length;

            let videoUrl = url[video].substr(9, lenght-19);
            videoList.push(videoUrl);
        }
        for(var dur in duration){
            durationList.push(duration[dur]);
        }
        for(var view in views)
            ViewsList.push(views[view]);
        for(var like in likes)
            LikesList.push(likes[like]);
        for(var cmnt in cmnts)
            CommentsList.push(cmnts[cmnt]);
    }
    let stillImageSetting;
    let stillImageValue;
    if($('#StillImage2:checked')){
        stillImageSetting = 'Sec';
        stillImageValue = $('#Sec').val();
        if (stillImageValue === "")
            stillImageValue = 1;
    }

    let titelDate = $('#Date').val();
    let titlePrefix = $('#prefix').val();
    let quality = $('#qualite').val();
    let operation_id = $('#operation_id').val();
    $.ajax({
        url : 'savefile',
        type : 'POST',
        data : {
            'videosUrls[]': videoList,
            'durationList[]': durationList,
            'likesList[]' : LikesList,
            'viewsList[]' : ViewsList,
            'commentsList[]' : CommentsList,
            'stillImageSetting' : stillImageSetting,
            'stillImageValue' : stillImageValue,
            'titelDate' : titelDate,
            'titelPrefix' : titlePrefix,
            'quality' : quality,
            'operation_id':operation_id
        },
        beforeSend: function() {
            var loader = document.getElementById('loaderMother');
            loader.style.visibility = 'visible';
            $('#loaderMother').show();
        },
        success: function(data) {
            $('#loaderMother').hide();
            var loader = document.getElementById('loaderMother');
            loader.style.visibility = 'hidden';
            window.location = "/"
        },
        cache: false
    });
}

function timestamp(duration) {
    let dur = duration.substr(2, duration.indexOf('M')-2);
    dur = dur+':'+duration.substr(duration.indexOf('M')+1, 2);
    var m = moment.duration(duration).minutes();
    var s = moment.duration(duration).seconds();
    return m+":"+s;
}
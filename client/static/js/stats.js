var createGraph = function(data, id)
{
    data.forEach(function (d) {
        d.inserted_at_date = timeConverter(d.inserted_at);
    });

    console.log("check:");
    console.log(data);

    var chart = makeLineChart(data, 'inserted_at_date', {
        'View count': {column: 'viewCount'},
        'Like count': {column: 'likeCount'},
        'Dislike count': {column: 'dislikeCount'}
    }, {xAxis: 'Time', yAxis: 'Amount'});
    chart.bind("#chart-" + id);
    chart.render();
};

function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;

  return date;
}
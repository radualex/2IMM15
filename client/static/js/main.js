enterKeycode = 13;

submitSearch = function()
{
    var query = $("#search").val();

    if (query.length <= 0)
    {
        alert("You must provide a query!");
    }
    else
    {
        var url_query = $.param({query:query}).replace("query=", "");

        var paths = location.pathname.split("/");
        paths[paths.length-1] = url_query;
        location.pathname = paths.join("/");
    }
}

$(document).ready(function()
{
    $("#search-button").on("click", submitSearch);

    $("#search").on("keypress", function (keyEvent)
    {
        if (keyEvent.keyCode === enterKeycode)
        {
            submitSearch();
        }
    });
});
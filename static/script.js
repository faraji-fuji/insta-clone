$(document).ready(function () {
  // ajax

  // get users
  $.get("http://127.0.0.1:8080/user", function (data, status) {
    if (status == "success") {
      $("#name").text(data[0].name);
    }
  });
});

// $(document).ready(function () {
//   $("#following").click(function () {
//     $.get("http://127.0.0.1:8080/user/id", function (data, status) {
//       window.location.assign("followers.html");

//       var user_id = data.user_id;

//       // get following
//       $.get(
//         `http://127.0.0.1:8080/user/${user_id}/following`,
//         function (data, status) {
//           console.log(data);
//         }
//       );
//     });
//   });

//   // get user_id
//   $.get("http://127.0.0.1:8080/user/id", function (data, status) {
//     console.log(data);
//     var user_id = data.user_id;

//     // get following
//     $.get(
//       `http://127.0.0.1:8080/user/${user_id}/following`,
//       function (data, status) {
//         console.log(data);
//       }
//     );

//     // get followers
//     $.get(
//       `http://127.0.0.1:8080/user/${user_id}/followers`,
//       function (data, status) {
//         console.log(data);
//       }
//     );
//   });
// });

$(document).ready(function () {
  $("#profile").click(function () {
    $.get("http://127.0.0.1:8080/post", function (data, status) {
      posts = data.posts;
      console.log(posts);

      console.log("possts");
    });
  });
});

console.log("resources.js loaded");

$(document).ready(function () {
  // Trigger loadVideos function when "Next" button is clicked
  $("#next-btn").on("click", function () {
    var nextToken = $(this).data("next-token");
    loadVideos(nextToken);
  });

  // Trigger loadVideos function when "Previous" button is clicked
  $("#prev-btn").on("click", function () {
    var prevToken = $(this).data("prev-token");
    loadVideos(prevToken);
  });
});

function loadVideos(pageToken) {
  $.ajax({
    url: "/resources/",
    data: {
      page_token: pageToken,
    },
    dataType: "json",
    success: function (response) {
      console.log(response); // Log the response to inspect the videos and tokens

      // Clear the current videos
      $("#video-cards").empty();

      // Loop through the videos and append them to the video container
      $.each(response.videos, function (index, video) {
        var videoCard = `
                    <div class="card mb-3">
                        <div class="ratio ratio-16x9">
                            <iframe src="https://www.youtube.com/embed/${video.id.videoId}" allowfullscreen></iframe>
                        </div>
                    </div>
                `;
        $("#video-cards").append(videoCard);
      });

      // Update the "Next" and "Previous" buttons
      if (response.next_page_token) {
        $("#next-btn").data("next-token", response.next_page_token).show();
      } else {
        $("#next-btn").hide();
      }

      if (response.prev_page_token) {
        $("#prev-btn").data("prev-token", response.prev_page_token).show();
      } else {
        $("#prev-btn").hide();
      }
    },
    error: function (error) {
      console.log("Error fetching videos:", error);
    },
  });
}

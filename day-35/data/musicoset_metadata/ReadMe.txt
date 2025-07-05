
+-------------------------+
|    	 METADATA		  |
+-------------------------+

The Metadata folder consists of textual and numeric information about songs, artists and albums.
+---------------------------------------------------------------------------+

╔═════════════════════════════════════════════╗
║                    Files                    ║
╠══════════════╦══════════════════════════════╣
║  albums.csv  ║  Albums metadata collection. ║
╠══════════════╬══════════════════════════════╣
║  artists.csv ║ Artists metadata collection. ║
╠══════════════╬══════════════════════════════╣
║ releases.csv ║  Album release information.  ║
╠══════════════╬══════════════════════════════╣
║   songs.csv  ║  Songs metadata collection.  ║
╠══════════════╬══════════════════════════════╣
║  tracks.csv  ║    Song track information.   ║
╚══════════════╩══════════════════════════════╝

+---------------------------------------------------------------------------+

╔═══════════════════════════════════════════════════════════╗
║                           Albums                          ║
╠════════════════╦══════════════════════════════════════════╣
║    album_id    ║ The Spotify ID for the album.            ║
╠════════════════╬══════════════════════════════════════════╣
║      name      ║ The name of the album in Spotify.        ║
╠════════════════╬══════════════════════════════════════════╣
║    billboard   ║ The name of the album in Billboard.      ║
╠════════════════╬══════════════════════════════════════════╣
║     artists    ║ The artists of the album.                ║
╠════════════════╬══════════════════════════════════════════╣
║  total_tracks  ║ The total number of tracks of the album. ║
╠════════════════╬══════════════════════════════════════════╣
║   album_type   ║ The type of the album: one of "album",   ║
║                ║ "single", or "compilation".              ║
╠════════════════╬══════════════════════════════════════════╣
║    image_url   ║ The source URL of the image.             ║
╚════════════════╩══════════════════════════════════════════╝

+---------------------------------------------------------------------------+

╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                                          Artists                                         ║
╠═════════════╦════════════════════════════════════════════════════════════════════════════╣
║  artist_id  ║ The Spotify ID for the artist.                                             ║
╠═════════════╬════════════════════════════════════════════════════════════════════════════╣
║     name    ║ The name of the artist.                                                    ║
╠═════════════╬════════════════════════════════════════════════════════════════════════════╣
║  followers  ║ The total number of followers.                                             ║
╠═════════════╬════════════════════════════════════════════════════════════════════════════╣
║             ║ The popularity of the artist. The value will be between 0 and 100,         ║
║  popularity ║ with 100 being the most popular. The artist's popularity is calculated     ║
║             ║ from the popularity of all the artist's tracks.                            ║
╠═════════════╬════════════════════════════════════════════════════════════════════════════╣
║ artist_type ║ The type of the artists: one of "singer", "band", "duo", "rapper" or "DJ". ║
╠═════════════╬════════════════════════════════════════════════════════════════════════════╣
║  main_genre ║ The main genre that the artist is associated with.                         ║
╠═════════════╬════════════════════════════════════════════════════════════════════════════╣
║    genres   ║ A list of the genres the artist is associated with.                        ║
║             ║ For example: "Prog Rock", "Post-Grunge".                                   ║
║             ║ (If not yet classified, the array is empty).                               ║
╠═════════════╬════════════════════════════════════════════════════════════════════════════╣
║  image_url  ║ The source URL of the image.                                               ║
╚═════════════╩════════════════════════════════════════════════════════════════════════════╝

+---------------------------------------------------------------------------+

╔═════════════════════════════════════════════════════════════════════════════════╗
║                                     Releases                                    ║
╠════════════════════════╦════════════════════════════════════════════════════════╣
║        artist_id       ║ The Spotify ID for the artist.                         ║
╠════════════════════════╬════════════════════════════════════════════════════════╣
║        album_id        ║ The Spotify ID for the album.                          ║
╠════════════════════════╬════════════════════════════════════════════════════════╣
║      release_date      ║ The date the album was first released,                 ║
║                        ║ for example, "1981-12-15".                             ║
╠════════════════════════╬════════════════════════════════════════════════════════╣
║ release_date_precision ║ The precision with which release_date value is known:  ║
║                        ║ "year", "month", or "day".                             ║
╚════════════════════════╩════════════════════════════════════════════════════════╝

+---------------------------------------------------------------------------+

╔════════════════════════════════════════════════════════════════════════════════════╗
║                                        Songs                                       ║
╠════════════════╦═══════════════════════════════════════════════════════════════════╣
║     song_id    ║ The Spotify ID for the song.                                      ║
╠════════════════╬═══════════════════════════════════════════════════════════════════╣
║      name      ║ The name of the track in Spotify.                                 ║
╠════════════════╬═══════════════════════════════════════════════════════════════════╣
║    billboard   ║ The name of the track in Billboard.                               ║
╠════════════════╬═══════════════════════════════════════════════════════════════════╣
║     artists    ║ The artists who performed the track.                              ║
╠════════════════╬═══════════════════════════════════════════════════════════════════╣
║   popularity   ║ The popularity of the track. The popularity of a track is         ║
║                ║ a value between 0 and 100, with 100 being the most popular.       ║
║                ║ The popularity is calculated by algorithm and is based,           ║
║                ║ in the most part, on the total number of plays the track          ║
║                ║ has had and how recent those plays are. Generally speaking,       ║
║                ║ songs that are being played a lot now will have higher            ║
║                ║ popularity than songs that were played a lot in the past.         ║
╠════════════════╬═══════════════════════════════════════════════════════════════════╣
║    explicit    ║ Whether or not the track has explicit lyrics true = yes it does;  ║
║                ║ false = no it does not OR unknown.                                ║
╠════════════════╬═══════════════════════════════════════════════════════════════════╣
║    song_type   ║ The type of the song: one of "solo songs"                         ║
║                ║ (with only one artist present in its execution) or                ║
║                ║ "collaborative songs" (where there is more than one artist).      ║
╚════════════════╩═══════════════════════════════════════════════════════════════════╝


+---------------------------------------------------------------------------+

╔══════════════════════════════════════════════════════════════════════════════════╗
║                                      Tracks                                      ║
╠════════════════════════╦═════════════════════════════════════════════════════════╣
║         song_id        ║ The Spotify ID for the song.                            ║
╠════════════════════════╬═════════════════════════════════════════════════════════╣
║        album_id        ║ The Spotify ID for the album.                           ║
╠════════════════════════╬═════════════════════════════════════════════════════════╣
║      track_number      ║ The number of the track. If an album has several discs, ║
║                        ║ the track number is the number on the specified disc.   ║
╠════════════════════════╬═════════════════════════════════════════════════════════╣
║      release_date      ║ The date the album was first released,                  ║
║                        ║ for example, "1981-12-15".                              ║
╠════════════════════════╬═════════════════════════════════════════════════════════╣
║ release_date_precision ║ The precision with which release_date                   ║
║                        ║ value is known: "year" , "month" , or "day".            ║
╚════════════════════════╩═════════════════════════════════════════════════════════╝

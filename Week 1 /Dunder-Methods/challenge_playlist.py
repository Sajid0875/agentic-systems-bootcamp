class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):
        return self.songs[index]

    def __iter__(self):
        return iter(self.songs)

    def __str__(self):
        return f"Playlist with {len(self)} songs"

    def __repr__(self):
        return f"Playlist({self.songs})"


playlist = Playlist([
    "Song A",
    "Song B",
    "Song C"
])

print(len(playlist))

print(playlist[1])

for song in playlist:
    print(song)

print(playlist)

print(repr(playlist))
class Artist:
    external_urls: dict
    followers: int
    genres: list
    href: str
    id: str
    images: list
    name: str
    popularity: int
    uri: str

    def __init__(self, data):
        self.external_urls = data['external_urls']
        self.followers = data['followers']['total']
        self.genres = data['genres']
        self.href = data['href']
        self.id = data['id']
        self.images = data['images']
        self.name = data['name']
        self.popularity = data['popularity']
        self.uri = data['uri']

    def __repr__(self):
        return f"{self.name} - {self.followers}/{self.popularity}% [{'] ['.join(self.genres)}] https://open.spotify.com/artist/{self.id}"

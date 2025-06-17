# ProMediaPaket  - PMP

ProMediaPaket im folgenden PMP sind umbenannte ZIP Dateien.

## Namensgebung der PMP Datei
\<provider\>@\<provider_id\>@\<title\>.pmp

## Aufbau der Datei
datei.pmp  
|- metadata.json    # Metadata für die Datei  
|- video.mkv        # Genauer Dateiname kann in metadata.json definiert werden  
|- thumbnail_horizontal.png         # Haupt Titelbild für Breitbild.  
|- thumbnail_vertical.png           # Haupt Titelbild für Hochkant.  
|- series_thumbnail_horizontal.png  # Haupt Titelbild der Serie für Breitbild, nur bei type "episode".  
|- series_thumbnail_vertical.png    # Haupt Titelbild der Serie für Hochkant, nur bei type "episode".  
|- audios/  # audio ordner mit verschiedenen Sprachen werden nach ISO 639 benannt und können optional einen Anhang nach ISO 3166-1 Alpha 2 haben.  
 |- deu.mkv  
 |- ja.mkv  
 |- de-DE.mkv  
 |- en-US.mkv  
|- subtitles/ # untertitle ordner mit gleicher Benennung wie der audios ordner mit verschiedenen Dateiformaten, falls der Untertitel erzwungen ist muss 'forced@' vorangestellt werden.  
 |- deu.ass  
 |- forced@ja.ttml  
 |- de-DE.srt  
 |- en-US.vtt  


## Aufbau metadata.json
```python
{
    version: int = 1                        # Version der Datei
    video_filepath: str = "video.mkv"       # Relativer Pfad zur Videodatei
    audio_in_videofile: bool = False        # Ob der Ton in der Videodatei ist. Bitte vermeiden.
    audio_filepaths: list[str] = None       # Liste der Audiodateinamen. Der audios/ Prefix ist nicht enthalten. Die Sprache kann mit Path().stem abgelesen werden.
    subtitle_filepaths: list[str] = None    # Liste der Untertitledateinamen. Det subtitles/ Prefix ist nicht enthalten. Die Sprache und ob erzwungen kann mit Path().stem abgelesen werden.

    provider: str | None = None             # Quelle des Videos. None für unbekannt/anders
    provider_id: str | None = None          # ID des Videos beim Provider selber.

    type: int = None                        # Typ des Videos; 0 = None; 1 = "episode"; 2 = "movie"
    title: str = None                       # Titel des Videos
    description: str = None                 # Beschreibung des Videos

    thumbnail_horizontal: str | None = None # Pfad zum horizontalem Titelbild.
    thumbnail_vertical: str | None = None   # Pfad zum vertikalem Titelbild.
}
```

Wenn der type "episode" ist kommen folgende dazu:
```python
{
    series_title: str = None                # Titel der Serie
    series_id: str = None                   # Serien ID beim Provider
    series_description: str = None          # Beschreibung der Serie
    series_thumbnail_horizontal: str | None = None # Pfad zum horizontalem Serientitelbild.
    series_thumbnail_vertical: str | None = None   # Pfad zum vertikalem Serientitelbild.
    
    season_number: str = None               # Staffelnummer
    season_id: str = None                   # Staffel ID beim Provider
    episode_number: str = None              # Episodennummer
}
```

# Sonderfall Extras
Wenn ein Film der Serie extras hat, können diese mit dem Prefix 'extra@' gekennzeichnet werden.

### Filme
Für Filme sollte die PMP datei im selben Ordner wie der Hauptfilm liegen und folgende Namesformat folgen:
extra@\<provider\>@\<main_movie_id\>@\<extras_provider_id\>@\<title\>.pmp

### Serien
Bei Serien sollte eine Seperate Staffel mit dem Namen 'extras' angelegt werden und alle Extras als Staffel Extras angespeichert werden.

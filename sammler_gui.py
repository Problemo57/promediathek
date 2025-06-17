from tkinter import Button

from lib.baseclass.downloader import BaseDownloadHandler
from lib.pakete.sammelpaket import Sammelpaket, EpisodeSammelpaket, MovieSammelpaket
from lib.utils.gui import ProGUI
from lib.utils.threader import MultiThreader
from providers import providers
from lib.utils.logger import enable_console_log
enable_console_log()

show_images = True
show_stream_details = False

max_download_threads = 5
active_provider = providers[0]
cache_vars = {
    "Serien": None,
    "Filme": None,
    "Hörbücher": None,
    "Musik": None,

    "last_series_episodes": [],
}


def switch_provider(new_provider):
    global active_provider
    global top_selection_list
    active_provider = [provider for provider in providers if provider.name == new_provider][0]
    [cache_vars.__setitem__(key, None) for key in cache_vars.keys()]
    gui.deleteColumns(until_len=2)

    top_selection_list.destroy()
    top_selection_list = top_selection_column.addList()


def show_episode(episode_id):
    def download_episode(_):
        downloader = BaseDownloadHandler(active_provider.get_downloader(episode))
        threader.add_thread(downloader.download)
        gui.addProgressbar(downloader.progresspaket)

    # noinspection PyTypeChecker
    episode: EpisodeSammelpaket = [episode for episode in cache_vars['last_series_episodes'] if episode.id == episode_id][0]

    gui.deleteColumns(until_len=4)
    episode_details_column = gui.addColumn()
    episode_details_column.addText(f"Serienname: {episode.series_title}")
    episode_details_column.addText(f"Folgenname: {episode.titel}")
    episode_details_column.addText("")
    episode_details_column.addText(f"Staffel: {episode.season_number}")
    episode_details_column.addText(f"Folge: {episode.episode_number}")
    episode_details_column.addText("")
    episode_details_column.addButtons(f"Download", download_episode)
    episode_details_column.addText("")
    episode_details_column.addText(episode.description)


def switch_episodes(season_id):
    def download():
        with MultiThreader(max_threads=max_download_threads) as threader2:
            for episode in cache_vars['last_series_episodes']:
                if episode.season_id != season_id:
                    continue

                downloader = BaseDownloadHandler(active_provider.get_downloader(episode))
                threader2.add_thread(downloader.download)
                gui.addProgressbar(downloader.progresspaket)

    # noinspection PyTypeChecker
    season_episodes = {episode.id: f"{episode.episode_number} - {episode.titel}" for episode in cache_vars['last_series_episodes'] if episode.season_id == season_id}

    gui.deleteColumns(until_len=3)
    episode_column = gui.addColumn()
    episode_column.addText("Folgen")
    episode_column.addButtons("Download All", lambda x: threader.add_thread(download))
    episode_column.addList(season_episodes, callback=show_episode)


def switch_seasons(clicked_series_id: str):
    def download():
        with MultiThreader(max_threads=max_download_threads) as threader2:
            for episode in cache_vars['last_series_episodes']:
                downloader = BaseDownloadHandler(active_provider.get_downloader(episode))
                threader2.add_thread(downloader.download)
                gui.addProgressbar(downloader.progresspaket)

    # noinspection PyTypeChecker
    series_episodes: list[EpisodeSammelpaket] = [sammelpaket for sammelpaket in cache_vars['Serien'] if sammelpaket.series_id == clicked_series_id]
    series_seasons = {episode.season_id: episode.season_number for episode in series_episodes}

    gui.deleteColumns(until_len=2)
    season_column = gui.addColumn()
    season_column.addText(series_episodes[0].series_description)
    season_column.addButtons("Download All", callback=download)
    season_column.addList(series_seasons, callback=switch_episodes)

    # noinspection PyTypedDict
    cache_vars['last_series_episodes'] = series_episodes


def switch_filme(clicked_movie_id: str):
    def download_movie(_):
        download_handler = BaseDownloadHandler(movie_downloader)
        threader.add_thread(download_handler.download)
        gui.addProgressbar(download_handler.progresspaket)

    # noinspection PyTypeChecker
    movie: MovieSammelpaket = [sammelpaket for sammelpaket in cache_vars['Filme'] if sammelpaket.id == clicked_movie_id][0]
    gui.deleteColumns(until_len=2)

    movie_column = gui.addColumn()
    movie_column.addText(movie.titel)
    movie_column.addText("")
    movie_description_text = movie_column.addText(movie.description)

    gui.tick()
    movie_downloader = active_provider.get_downloader(movie)
    movie_description_text.destroy()
    movie_column.addText(movie.description)

    if show_stream_details:
        movie_downloader.init()
        movie_column.addText(f"Video: {movie_downloader.video}")
        movie_column.addText(f"Audios: {[str(a) for a in movie_downloader.audios]}")
        movie_column.addText(f"Subtitles: {[str(s) for s in movie_downloader.subtitles]}")

    movie_column.addButtons("Download", download_movie)
    gui.tick()

    if show_images:
        movie_poster = movie_downloader.download_thumbnail_vertical()
        if movie_poster:
            movie_column.addImage(movie_poster, width=300)
        gui.tick()
        movie_landscape = movie_downloader.download_thumbnail_horizontal()
        if movie_landscape:
            movie_column.addImage(movie_landscape, width=600)


def switch_top_selection(clicked_button: Button):
    global top_selection_list
    global top_selection_list_amount_text
    if top_selection_list_amount_text:
        top_selection_list_amount_text.destroy()
    [button.config(bg="#d9d9d9", activebackground="#d9d9d9") for button in top_selection_buttons]
    clicked_button.config(bg="gray", activebackground="gray")
    button_text = clicked_button.cget("text")
    top_selection_list.destroy()
    loading_text = top_selection_column.addText("\n\nLade Daten")
    gui.tk.update()
    loading_text.destroy()

    sammler_funcs = {
        "Serien": active_provider.get_all_episodes,
        "Filme": active_provider.get_all_movies,
    }

    if cache_vars[button_text]:
        sammelpakete = cache_vars[button_text]
    else:
        sammelpakete: list[EpisodeSammelpaket | Sammelpaket] = sammler_funcs[button_text]()
        cache_vars[button_text] = sammelpakete

    if button_text == "Serien":
        series_ids_names = {sammelpaket.series_id: sammelpaket.series_title for sammelpaket in sorted(sammelpakete, key=lambda x: x.series_title)}
        top_selection_list_amount_text = top_selection_column.addText(f'{len(series_ids_names)} Einträge')
        top_selection_list = top_selection_column.addList(series_ids_names, has_search=True, callback=switch_seasons)

    elif button_text == "Filme":
        movie_ids_names = {sammelpaket.id: sammelpaket.titel for sammelpaket in sorted(sammelpakete, key=lambda x: x.titel)}
        top_selection_list_amount_text = top_selection_column.addText(f'{len(movie_ids_names)} Einträge')
        top_selection_list = top_selection_column.addList(movie_ids_names, has_search=True, callback=switch_filme)

    else:
        series_ids_names = {sammelpaket.id: sammelpaket.titel for sammelpaket in sammelpakete}
        top_selection_list = top_selection_column.addList(series_ids_names)


top_selection_list_amount_text = None

if __name__ == "__main__":
    with MultiThreader() as threader:
        gui = ProGUI(title="Sammler")

        provider_column = gui.addColumn()
        provider_column.addText("Anbieter")
        provider_column.addList([provider.name for provider in providers], callback=switch_provider)

        top_selection_column = gui.addColumn()
        top_selection_buttons = top_selection_column.addButtons(["Serien", "Filme"], callback=switch_top_selection)
        top_selection_list = top_selection_column.addList()

        gui.run()

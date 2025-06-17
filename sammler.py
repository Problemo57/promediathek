from argparse import ArgumentParser

from lib.baseclass import BaseProvider
from lib.baseclass.downloader import BaseDownloadHandler
from lib.pakete.sammelpaket import Sammelpaket
from providers import providers
from lib.utils.db import ProDB
from lib.utils.threader import MultiThreader

from lib.utils.logger import enable_console_log
enable_console_log()

# Can only use half of your RAM.
# RAM usage: max_concurrent_provider_downloads * max_downloads_threads_per_provider * 2GB
max_concurrent_provider_downloads = 1
max_downloads_threads_per_provider = 1


def download_sammelpaket(provider: BaseProvider, sammelpaket: Sammelpaket):
    print(f"Downloading {sammelpaket.titel}")
    download_handler = provider.get_downloader(sammelpaket)
    downloader = BaseDownloadHandler(download_handler)
    downloader.download()


def download_provider(provider: BaseProvider):
    with MultiThreader(max_threads=max_downloads_threads_per_provider, ignore_exceptions=True) as threader:
        for sammelpaket in ProDB().sort_sammelpakete(provider.get_all()):
            if ProDB().already_downloaded(sammelpaket) and not args.update:
                continue

            threader.add_thread(download_sammelpaket, provider, sammelpaket)


def main():
    with MultiThreader(max_threads=max_concurrent_provider_downloads) as threader:
        for provider in providers:
            if args.provider and args.provider != provider.name:
                continue

            if not provider.check_if_subscribed():
                continue

            threader.add_thread(download_provider, provider)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description="Promediathek Downloader")
    arg_parser.add_argument("--provider", default=None, type=str, help="Provider name to download")
    arg_parser.add_argument('--update', default=False, action='store_true', help="Check every Video for new Audio/Subtitles.")
    arg_parser.add_argument('--threads', default=1, type=int, help="Number of threads to use")
    args = arg_parser.parse_args()

    max_downloads_threads_per_provider = args.threads

    main()

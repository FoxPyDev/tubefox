import requests
from tqdm import tqdm


class Downloader:
    def __init__(self, path, filename, file_type, best_quality_link, extension, chunk_size=1024):
        self.path = path
        self.filename = filename
        self.file_type = file_type
        self.best_quality_link = best_quality_link
        self.extension = extension
        self.chunk_size = chunk_size

    def _download_file(self):
        # Check if the link is empty or None
        if not self.best_quality_link:
            print(f"No {self.file_type} download link available.")
            return

        response = requests.get(self.best_quality_link, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        print(f"Start download {self.file_type}")
        with open(f'{self.path}{self.filename}.{self.extension}', 'wb') as file, tqdm(
                desc=f"{self.filename}.{self.extension}", total=total_size, unit='B', unit_scale=True
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        print(f"{self.file_type} downloaded")


if __name__ == "__main__":
    pass

from TTS.api import TTS
import pathlib
import torch
import tqdm

from .ebook import EBook

device = "cuda" if torch.cuda.is_available() else "cpu"


def orate(book_path, out_path):
    """Load `epub` path, clean it, and generate a `wav` file. Generates the
    `wav` in the same directory as the `epub`.

    Parameters
    ----------
    path: str
        Path to `epub` file.
    """
    book_path = pathlib.Path(book_path)
    filename = book_path.stem + '.txt'
    text_path = book_path.parent / filename

    audio_path = pathlib.Path(out_path) # / (path.stem + '.wav')

    book = EBook(book_path)
    book.write(text_path)

    voice = Voice()
    orator = Orator(
        voice=voice
    )
    orator.generate_audiobook(book, audio_path)

    
class Orator:
    # Parameters should be in relation to the oration
    def __init__(
            self,
            voice,
        ):
        self.voice=voice

    def set_voice(self, voice):
        self.voice = voice

    def generate_audiobook(
            self,
            book,
            path
    ):
        if not self.voice:
            raise ValueError('Please set a Voice first')

        path = pathlib.Path(path)
        path.mkdir(parents=True, exist_ok=True)

        self.voice.speak_to_path(
            book,
            path
        )
    
    # TODO: handle this in voice so that it intelligently chunks the string
    def generate_audiobook_from_string(
            self,
            text,
            path
    ):
        raise NotImplementedError('Not done yet!')
        if not self.voice:
            raise ValueError('Please set a Voice first')
        path = pathlib.Path(path)
        self.voice.speak_to_path(
            text,
            path
        )


# TODO: Load Tortoise TTS - https://github.com/neonbjb/tortoise-tts
# TODO: Load VALL-E-X - https://github.com/Plachtaa/VALL-E-X
class Voice:
    """A speaker for any audiobook that you want to generate.

    Parameters
    ----------
    speaker_path: pathlike, optional
        Path to a `.wav` file that contains a voice that you would like to use
        for audio generation. When not included, the audio is generated with
        the default voice.
    """

    def __init__(self, speaker_path=None):
        self.model = self.load_model()
        if speaker_path:
            speaker_path = pathlib.Path(speaker_path)
        self.speaker_path=speaker_path

    def load_model(self):
        # Init TTS with the target model name
        tts = TTS(
            model_name="tts_models/en/ljspeech/vits",
            progress_bar=True
        ).to(device)
        return tts
    
    def speak_to_path(self, book, path):
        path = pathlib.Path(path)
        print(f'Writing audiobook to {path}')
        for i, c in tqdm.tqdm(
                enumerate(book.chunks),
                desc='Generating book parts',
                total=len(book.chunks)
        ):
            file_path = path / f'part_{i}.wav'
            if self.speaker_path:
                self.model.tts_to_file(
                    text=c,
                    speaker_wav=self.speaker_path.as_posix(),
                    file_path=file_path.as_posix()
                )
            else:
                self.model.tts_to_file(
                    text=c,
                    file_path=file_path.as_posix()
                )
            print('Done')
        return path
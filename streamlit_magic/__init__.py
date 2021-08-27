from .magic import StreamlitMagics


def load_ipython_extension(ipython):
    ipython.register_magics(StreamlitMagics)


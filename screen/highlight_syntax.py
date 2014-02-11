import os
from termsaverlib.i18n import _
from termsaverlib.screen.base.filereader import FileReaderBase 
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import TerminalFormatter


class ProgrammerColor(FileReaderBase):
    """
        A simple screen that displays colorized source code.
    """

    def __init__(self):
        FileReaderBase.__init__(self, 
            'colorize', _('display colorized source code'))
        self.cleanup_per_cycle = True
        self.cleanup_per_file = True

    def _run_cycle(self):
        # validate path
        if not os.path.exists(self.path):
            raise exception.PathNotFoundException(self.path)

        # get the list of available files
        file_list = []
        if os.path.isdir(self.path):    
            for dirpath, dirnames, filenames in os.walk(self.path):
                for f in filenames:
                    file_list.append(os.path.join(dirpath, f))
        else:
            file_list.append(self.path)

        if len(file_list) == 0:
            raise exception.PathNotFoundException(self.path)

        self.clear_screen()
        for path in file_list:
            f = open(path, 'r')
            try:
                lexer = guess_lexer_for_filename(f.name, f.readline())
            except ClassNotFound:
                continue
            h = highlight(f.read(), lexer, TerminalFormatter())
            self.typing_print(h)
            f.close()

            if self.cleanup_per_file:
                self.clear_screen()

        def _message_no_path(self):
            return 'Please specify a file or directory to colorize'

import os
import re
from pathlib import Path


class Cleaner:
    build_output_patterns = [".*\.out$", ".*\.exe$", ".*\.exp$", ".*\.lib$", ".*\.pdb$"]

    def clean_build_outputs(self, path):
        self.clean(path, self.build_output_patterns)

    def clean(self, path, patterns):
        path = Path(path).absolute()
        for pathname, _, filenames in os.walk(path):
            to_remove = filter(
                lambda filename: any(
                    re.match(pattern, filename) for pattern in patterns
                ),
                filenames,
            )
            for filename in to_remove:
                os.remove(Path(pathname) / filename)

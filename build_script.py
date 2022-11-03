import os
import PyInstaller.__main__

if __name__ == "__main__":
    PyInstaller.__main__.run(
        [
            "main.py",
            "--add-data=data%sdata" % os.pathsep,
            "--name=BirdRage",
            "-w",
            "-F",
        ]
    )

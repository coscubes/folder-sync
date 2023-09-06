"""
Folder synchronizer including scheduler
"""

import  argparse
import  logging
import  time

import  schedule
from    sync import FolderSynchronization

def main():
    """Main driver program"""
    parser = argparse.ArgumentParser("Simple script to synchronize two folders")

    parser.add_argument("--source", "-s", type = str, default = "",
                        help = "Absolute path of the source folder")
    parser.add_argument("--destination", "-d", type = str, default = "",
                        help="Absoulute path of the destination folder")
    parser.add_argument(
        "--interval", "-i", type = float, default = None,
        help="Time interval in minutes for synchronization. Can be float"
    )
    parser.add_argument("--log", "-l", type = str, default = "./log.txt",
                        help="absolute file path to logger")

    args = parser.parse_args()

    # Prevent scheduler module from accessing logging
    logging.getLogger('schedule').propagate = False

    folder_synchronizer = FolderSynchronization(
        args.source,
        args.destination,
        args.log
    )

    # If there is no interval given then synchonize the folders once.
    if args.interval is not None:
        # Create a scheduled call of the synchronization function after
        # every args.interval minutes
        schedule.every(args.interval).minutes.do(
            folder_synchronizer.synchronize_folders
        )

        while True:
            schedule.run_pending() # Launches scheduler
            time.sleep(1)
    else:
        folder_synchronizer.synchronize_folders()

if __name__ == "__main__":
    main()

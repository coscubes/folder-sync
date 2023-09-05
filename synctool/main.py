import  argparse
import  logging
import  schedule
from    sync import FolderSynchronization
import  time

def main():
    """Main driver program"""
    parser = argparse.ArgumentParser("Simple script to synchronize two folders")

    parser.add_argument("--source", "-s", type=str, default="",
                        help = "Absolute path of the source folder")
    parser.add_argument("--destination", "-d", type = str, default="",
                        help="Absoulute path of the destination folder")
    parser.add_argument("--interval", "-i", type=float, default=None,
                        help="Time interval in minutes for synchronization")
    parser.add_argument("--log", "-l", type=str, default="./log.txt",
                        help="absolute file path to logger")

    args = parser.parse_args()

    # log file cannot be in source or destination directories
    # add check TODO


    logging.getLogger('schedule').propagate = False

    folder_synchronizer = FolderSynchronization(
        args.source,
        args.destination,
        args.log
    )

    if args.interval is not None:
        schedule.every(args.interval).minutes.do(
            folder_synchronizer.synchronize_folders
        )

        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        folder_synchronizer.synchronize_folders()

if __name__ == "__main__":
    main()

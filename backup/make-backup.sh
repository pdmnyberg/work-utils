if [ "$#" -ne 1 ]; then
    echo "Wrong number of parameters"
    exit 1
fi


DATE=$(date '+%Y-%m-%d')
BACKUP_DIR="$1/home-${DATE}"
echo "Backing up Home to: $BACKUP_DIR"
rsync -a --delete --quiet --exclude-from rsync-homedir-excludes.txt ~/ "$BACKUP_DIR"
echo "Done"

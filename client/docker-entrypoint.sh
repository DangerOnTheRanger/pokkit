#/usr/local/bin/pokkit-client

# sane shell environment
set -o noclobber -o errexit -o nounset -o xtrace
#cd $(dirname $0)

# start fuse server
python3 -m "pokkit.client.fuse" &
fuse_pid=$!
sleep 1
# TODO: test fuse server
kill ${fuse_pid}

# test other components
python3 -m "pokkit.client.core"
#python3 -m "pokkit.client.gui"

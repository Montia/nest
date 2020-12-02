#/usr/bin/sh
export FLASK_APP=$(dirname $0)/server
export FLASK_ENV=development
if [ $# > 0 -a "$1"x == "init-db"x ];
then
	flask init-db
elif [ $# -gt 0 ];
then
	echo "Error, only support argument \"init-db\" or no argument"
	exit
fi
flask run --host=0.0.0.0

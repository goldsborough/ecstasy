echo;

for ((i=0;i<3;++i)); do

    x=1;

    for j in {40..47} {100..107}; do

	if [ $i -eq 1 ]; then

	    if [ $x -eq 1 ] || [ $x -eq 5 ] || [ $x -eq 13 ]; then

		c=97;

	    else

		c=30;

	    fi;

	else

	    c=8;

	fi;

	echo -en "\033[${j}m  \033[${c}m$x  \033[0m";

	let x+=1;

    done;

    echo;

done;

echo;
echo

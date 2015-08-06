echo
x=1

for i in {30..37} {90..97}; do

    if [ $x -eq 1 ];then

	b=107

    else

	b=40

   fi
	
    
    echo -en "\033[${i};${b}m  $x  \033[0m"

    let ++x

done

echo
echo

#########################################################################
# File Name: do.pdf.sh
# Author: Iydon
# mail: 11711217@mail.sustc.edu.cn
# Created Time: Thu 24 May 2018 06:15:18 PM CST
#########################################################################
#!/bin/bash

if [ "$1" -eq "1" ]; then
    echo "\documentclass{article}" > main.tex
    echo "\usepackage{amsmath,amssymb,amsfonts,mathrsfs,amsthm}"   >> main.tex
    echo "\pagestyle{empty}"      >> main.tex
    echo "\begin{document}"       >> main.tex
    echo "\["                     >> main.tex
elif [ "$1" -eq "2" ]; then
    echo "\]"                     >> main.tex
    echo "\end{document}"         >> main.tex
    pdflatex -halt-on-error main.tex
    rm main.log main.aux
    pdfcrop main.pdf out.pdf
    rm main.pdf
elif [ "$1" -eq "3" ]; then
    curl -F"smfile=@out.png" "https://sm.ms/api/upload" > result.log
    rm out.pdf out.png
elif [ "$1" -eq "4" ]; then
    rm result.log
fi

# curl -F"smfile=@out.png" "https://sm.ms/api/upload"
#pdflatex $file.tex
#rm $file.aux $file.log

#pdfcrop $file.pdf image.pdf
#python3 Form2.py

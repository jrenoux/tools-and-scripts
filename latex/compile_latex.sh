#!/bin/bash
#format: latex_compile [biblioProgram] filename

#config
master_bib="path/to/master/bib/file.bib"
path_to_current_folder="/path/to/current/folder"


#get the name without the extension
biblioProgram=biber
errorMessage=""
if [ "$#" -eq 0 ]; then	
	echo "USAGE: ./compile_latex.sh [*biber*/bibtex] filename"
	exit
fi

if [ "$#" -eq 2 ]; then
    biblioProgram=$1
    #filename=$(echo $2 | cut -f 1 -d '.')
    basename=$2
else
    #filename=$(echo $1 | cut -f 1 -d '.')
    basename=$1
fi

filename="${basename##*/}"
# get the master filename (if there is "TeX-master" property in the document)
masterfilename=`python3 $path_to_current_folder/get-master-filename.py $filename` # Remember to change the path
masterfilename="${masterfilename%.*}"



#create build folder
buildDir=$masterfilename.build
TEXMFOUTPUT=$buildDir

rm $buildDir/*
rmdir $buildDir
mkdir $buildDir


target_bib=$masterfilename".bib"

python3 $path_to_current_folder/fetch-references.py $master_bib $target_bib

mainDirectory=$(pwd)

echo "cp "$mainDirectory"/*.bib" $buildDir
cp "$mainDirectory"/*.bib "$buildDir"

echo "==============================================================="
echo "Compiling file " $masterfilename " (basename : " $basename")"
echo "Using " $biblioProgram " as bibliography manager"
echo "==============================================================="

pdflatex -output-directory $buildDir $masterfilename.tex
echo "==============================================================="
echo "==============================================================="
if [ "$biblioProgram" = "biber" ]; then
   biber $buildDir/$masterfilename
elif [ "$biblioProgram" = "bibtex" ]; then
   bibtex $buildDir/$masterfilename.aux
else 
   echo "bibliography manager " $biblioProgram " not recognized"
   errorMessage=$(echo "Bibliography manager " $biblioProgram " not recognized")
fi
echo "==============================================================="
echo "==============================================================="
pdflatex -output-directory $buildDir $masterfilename.tex
echo "==============================================================="
echo "==============================================================="
pdflatex -output-directory $buildDir $masterfilename.tex

echo "==============================================================="
echo "File " $masterfilename " compiled with " $biblioProgram " as bibliography manager"
echo "==============================================================="
echo $errorMessage
echo "==============================================================="
echo " Last run (showing only warnings)"
echo "==============================================================="
pdflatex -output-directory $buildDir $masterfilename.tex | grep "LaTeX Warning" > warnings.txt
python3 /home/jennifer/scripts/latex/process-warnings.py
rm warnings.txt

cp "$buildDir/$masterfilename.pdf" "$mainDirectory"


echo "==============================================================="
echo " TODOs left in *.tex files"
echo "==============================================================="
grep -n 'TODO' *.tex


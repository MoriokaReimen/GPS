#! /bin/bash
for f in $(find ./data/ -name "motor*.txt" -type f);
do
  #set path variables
  fname=${f##*/}
  dir=${f%/*}

  echo
  echo
  echo 'processing'${f}

  cp -f ${f} .
  python motor.py ${fname} |tee distance.txt
  mv -f ./distance.txt ${dir}

  #Clean up process
  rm -f ./motor*.txt
done

for f in $(find ./data/ -name "*.000" -type f);
do
  #set path variables
  fname=${f##*/}
  dir=${f%/*}

  echo
  echo
  echo 'processing'${f}

  cp -f ${f} .
  python gps.py ${fname} |tee distance.txt
  mv -f ./distance.txt ${dir}

  #Clean up process
  rm -f ./*.000
done

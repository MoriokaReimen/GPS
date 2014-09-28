#! /bin/bash
for f in $(find ./data/ -name "motor*.txt" -type f);
do
  #set path variables
  fname=${f##*/}
  name=${fname##.*}
  dir=${f%/*}

  echo
  echo
  echo 'processing'${f}

  cp -f ${f} .
  python motor.py ${fname} |tee ${name}_distance.txt
  mv -f ./${name}_distance.txt ${dir}

  #Clean up process
  rm -f ./${fname}
done

for f in $(find ./data/ -name "*.000" -type f);
do
  #set path variables
  fname=${f##*/}
  name=${fname##.*}
  dir=${f%/*}

  echo
  echo
  echo 'processing'${f}

  cp -f ${f} .
  python gps.py ${fname} |tee ${name}_distance.txt
  mv -f ./${name}_distance.txt ${dir}

  #Clean up process
  rm -f ./*.000
done

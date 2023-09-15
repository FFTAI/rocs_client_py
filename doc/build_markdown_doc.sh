FILE_FULL_PATH=$0
FILE_NAME=${FILE_FULL_PATH##*/}
FILE_PATH=$(find -name "$FILE_NAME" | awk '{print $1}')
cd $(dirname "$FILE_PATH")

cd ../src
touch __init__.py

cd -
rm -rf source
rm -rf build

mkdir build
mkdir source

cp conf.py ./source/
cp index.rst ./source/


sphinx-apidoc -o source ../src
make markdown

cd ../src
rm -rf __init__.py
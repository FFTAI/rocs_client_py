FILE_FULL_PATH=$0
FILE_NAME=${FILE_FULL_PATH##*/}
FILE_PATH=$(find -name "$FILE_NAME" | awk '{print $1}')
cd $(dirname "$FILE_PATH")

rm -rf source
rm -rf build

mkdir -p source/_static
mkdir -p source/_template
mkdir build

# git版本中直接忽略了source和build两个目录
cp -r conf.py ./source
cp -r index.rst ./source

sphinx-apidoc -o source ../src
make html


mv build/html/* ../docs

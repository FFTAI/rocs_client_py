rm -rf dist

python -m build

python -m twine upload dist/*

rm -rf ./dist
rm -rf ./rocs_client.egg-info

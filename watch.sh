export brownfield_land_index=http://localhost:8000/brownfield-land-collection/collection/index.json

make

while inotifywait -e close_write ../brownfield-land-collection/collection/index.json 
do
  make
done

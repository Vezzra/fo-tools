cd build
rm -R *
cmake ..
cmake --build . --config RelWithDebInfo
cd ..
echo "Press any key..."
read

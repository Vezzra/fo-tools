cd build
del *.*
cmake -G "Visual Studio 14 2015" -T v140_xp ..
cmake --build . --config RelWithDebInfo
cd ..
pause

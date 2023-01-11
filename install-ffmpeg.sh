cd /usr/local/bin
mkdir ffmpeg
cd ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz
rm ffmpeg-release-amd64-static.tar.xz
ln -s /usr/local/bin/ffmpeg/ffmpeg-5.1.1-amd64-static/ffmpeg /usr/bin/ffmpeg

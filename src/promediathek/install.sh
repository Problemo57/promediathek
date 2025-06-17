#! /bin/bash

set -e
sudo apt-get update -qq && sudo apt-get -y install \
  build-essential \
  yasm \
  libass-dev \
  ninja-build \
  doxygen \
  xxd \
  nasm \
  cmake \
  curl \
  libreadline-dev \
  libgdbm-compat-dev \
  libopus-dev \
  libdav1d-dev \
  libsndfile1-dev \
  libssl-dev \
  libsqlite3-dev \
  openssl \
  libssl-dev \
  llvm \
  tk-dev \
  pkg-config \
  git \
  zlib1g-dev


sudo rm -rf Python*

curl -s "https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tar.xz" -o "python.tar.xz"
tar -xf "python.tar.xz"
rm -r "python.tar.xz"
cd Python*
./configure --enable-optimizations
make -j "$(nproc)"
sudo make install
cd ..

rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#rm -rf ~/.zshenv ~/.bash_completion
#activate-global-python-argcomplete
#eval "$(register-python-argcomplete crunchyroll_downloader)"

sudo rm -rf Python*

CLANG_VERSION="19"
SVT_AV1_VERSION="3.0.2"

sudo rm -rf SVT-AV1
wget -O svt-av1.tar.gz "https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/v${SVT_AV1_VERSION}/SVT-AV1-${SVT_AV1_VERSION}.tar.gz"
tar xvf svt-av1.tar.gz
rm svt-av1.tar.gz
mv SVT-AV1-v${SVT_AV1_VERSION}* "SVT-AV1"

cd SVT-AV1
sed -i "s/llvm-profdata/llvm-profdata-$CLANG_VERSION/g" CMakeLists.txt
cd Build/linux
sudo CC="clang-$CLANG_VERSION" CXX="clang++-$CLANG_VERSION" ./build.sh release "-j$(nproc)" --install --enable-pgo
cd ../../..

rm -rf ffmpeg
wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjvf ffmpeg-snapshot.tar.bz2
rm -f ffmpeg-snapshot.tar.bz2

rm -rf ffmpeg_source
mv ffmpeg ffmpeg_source
cd ffmpeg_source || (echo "Error, no ffmpeg dir" && exit)

./configure \
  --pkg-config-flags="--static" \
  --extra-libs="-lpthread -lm" \
  --extra-ldflags="-Wl,-rpath,/usr/local/lib" \
  --ld="g++" \
  --enable-gpl \
  --enable-libass \
  --enable-libsvtav1 \
  --enable-libdav1d \
  --enable-libopus \
  --enable-openssl \
  --enable-version3

make -j "$(nproc)"
cp ffmpeg ffprobe ../venv/bin/
cd ..
sudo rm -rf ffmpeg_source SVT-AV1


# Install mount-zip for fast zip file access.
wget "https://github.com/google/mount-zip/archive/refs/tags/v1.8.zip" -O mount-zip.zip
unzip mount-zip.zip
rm mount-zip.zip
mv mount-zip* mount-zip
cd mount-zip
sudo apt-get -y install libboost-container-dev libicu-dev libfuse3-dev libzip-dev g++ pkg-config make pandoc
make -j "$(nproc)"
sudo make install
cd ..
rm -rf mount-zip


# Install Bento4 for drm decryption
curl -s "https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip" -o "bento4.zip"
unzip "bento4.zip"
rm -rf "bento4"; mv Bento4-SDK* "bento4"
mv bento4/bin/* "venv/bin"

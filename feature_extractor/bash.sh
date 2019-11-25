# OBS Config
wget https://obs-community.obs.cn-north-1.myhuaweicloud.com/obsutil/current/obsutil_linux_amd64.tar.gz
tar -xzvf obsutil_linux_amd64.tar.gz
cd obsutil_linux_amd64_5.1.10
chmod 755 obsutil
./obsutil config -i=DT4AOTZSAYYL3AWVX5CV -k=WYddcYRUK8KIjKcBh7KWi8aZ9G6TUvWg0CVfF7NZ -e=http://obs.cn-north-1.myhuaweicloud.com

# Ubuntu source
echo 'deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse' > /etc/apt/source.list
apt update

# PYTHON config
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
apt install python3-pip
pip3 install pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
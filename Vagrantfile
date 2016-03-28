# -*- mode: ruby -*-
# vi: set ft=ruby :

# Ref. https://www.vagrantup.com/docs/virtualbox/networking.html
# Ref. http://qiita.com/sho7650/items/cf5a586713f0aec86dc0
Vagrant.configure(2) do |config|
  config.vm.box = "debian/jessie64"

  config.vm.define 'dockerhost' do |dockerhost|
    dockerhost.vm.network 'private_network', ip: '192.168.50.2',
    virtualbox__intnet: '_inner'

    dockerhost.vm.provision 'shell', inline: <<-SCRIPT
      curl -fsSL https://get.docker.com/ | sh
      gpasswd -a vagrant docker
      curl -L https://github.com/docker/compose/releases/download/1.6.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
      chmod +x /usr/local/bin/docker-compose
      curl -fsSL https://bootstrap.pypa.io/get-pip.py | python
      pip install -r /vagrant/requirements.txt
    SCRIPT
  end

  config.vm.define 'client' do |client|
    client.vm.network 'private_network', ip: '192.168.50.3',
    virtualbox__intnet: '_inner'
  end
end

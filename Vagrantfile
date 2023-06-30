# -*- mode: ruby -*-
# vi: set ft=ruby :

vmPath = `VBoxManage list systemproperties | grep 'Default machine folder' | cut -b 34-`
vmPath = vmPath.gsub("\n","")

Vagrant.configure("2") do |config|
  boxes = [
    { :name => "master-1", :box => "ubuntu/focal64", :ip_address => "192.168.56.11"},
    { :name => "master-2", :box => "ubuntu/focal64", :ip_address => "192.168.56.12"},
    { :name => "node-1", :box => "ubuntu/focal64", :ip_address => "192.168.56.13"},
    { :name => "node-2", :box => "ubuntu/focal64", :ip_address => "192.168.56.14"},
    { :name => "node-3", :box => "ubuntu/focal64", :ip_address => "192.168.56.15"},
  ]
  boxes.each do |opts|
    config.vm.define opts[:name] do |config|
      config.vm.hostname = opts[:name]
      config.vm.network "private_network", ip: opts[:ip_address]
      config.vm.box = opts[:box]
      config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 3
        if (File.file?("#{vmPath}/#{opts[:name]}_additional_disk.vdi"))
          
        else
          v.customize ['createhd', '--filename', "#{vmPath}/#{opts[:name]}_additional_disk.vdi",'--variant', 'Fixed', '--size', 20 * 1024]
        end      
        v.customize ['storageattach', :id,  '--storagectl', 'SCSI', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', "#{vmPath}/#{opts[:name]}_additional_disk.vdi"]
      end
      
      if opts[:name] == boxes.last[:name]
        config.vm.provision "ansible" do |ansible|
          ansible.playbook = "main.yml"
          ansible.limit = "all"
          ansible.groups = {
            "master" => ["master-1", "master-2"],
            "node" => ["node-1", "node-2", "node-3"]
          }
          ansible.extra_vars = {
            master_ip: "192.168.56.11",
            extra_cluster_init_master_args: "--advertise-address=192.168.56.11 --tls-san=192.168.56.11 --node-ip=192.168.56.11 --node-external-ip=192.168.56.11 --flannel-iface=enp0s8",
            extra_server_args: "--disable servicelb --flannel-iface=enp0s8",
            extra_agent_args: "--flannel-iface=enp0s8",
            metallb_ip_range: "192.168.56.240-192.168.56.250"
          }          
        end
      end
    end
  end
end

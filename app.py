import docker
client = docker.from_env()

def readHosts():
    f = open("/etc/hosts", "r")
    hosts_file = f.read().strip()
    f.close()
    return hosts_file

def writeHosts(hosts_file):
    f = open("/etc/hosts", "w")
    f.write(hosts_file)
    f.close()

def getHostname():
    docker_ip_list = []
    for container in client.containers.list():
        for network in container.attrs['NetworkSettings']['Networks']:
            container_ip = container.attrs['NetworkSettings']['Networks'][network]['IPAddress']
            container_name = container.name
            hostname = container.attrs['Config']['Hostname']

            if container_ip and hostname.find('.') != -1:
                docker_ip_list.append(f'{container_ip} {hostname}')

    return '\n'.join(map(str, docker_ip_list))

hosts_file = readHosts()

if hosts_file.find('# DOCKER SECTION') == -1:
    hosts_file = hosts_file + '\n' + '# DOCKER SECTION' + '\n' + getHostname()
    writeHosts(hosts_file)
    print(hosts_file)
else:
    docker_index = hosts_file.split('\n').index('# DOCKER SECTION')
    hosts_file = '\n'.join(map(str, hosts_file.split('\n')[:docker_index])) + '# DOCKER SECTION' + '\n' + getHostname()
    writeHosts(hosts_file)
    print(hosts_file)
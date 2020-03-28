import paramiko

if __name__ == '__main__':
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('127.0.0.1', username='cat', password='cat', port=2222)

    stdin, stdout, stderr = client.exec_command('ls -la prog')
    for line in stdout:
        print('... ' + line.strip('\n'))
    client.close()

import argparse
import json
import os

import requests

parser = argparse.ArgumentParser(description='ssh-key generator')
parser.add_argument('--passphrase', '-N', required=True,
                    help='desired passphrase for ssh-key (required)')
parser.add_argument('--pc-name', '-n', required=True,
                    help='current PC name (could be any, required)')
parser.add_argument('--destination', '-t', default='.',
                    help='destination folder')
parser.add_argument('--write-access', action='store_true',
                    help='if specified the deploy key will have the'
                         ' write access to the repository')
parser.add_argument('--no-github', action='store_true',
                    help='generate key only without adding it to github')
args = parser.parse_args()


script_dir = os.path.dirname(os.path.realpath(__file__))
if not args.no_github:
    with open(os.path.join(script_dir, 'secret.txt'), 'r') as secret_file:
        github_secret = secret_file.readline().strip()
json_config_file = os.path.join(script_dir, 'deploy-key-config.json')
with open(json_config_file, 'r') as json_file:
    config_dict = json.load(json_file)


if args.write_access:
    print('WARNING: every keys will be written with write-access')


def add_deploy_key(repo_name, public_key):
    print(f'Adding key {public_key} to {repo_name}')
    header = {'Authorization': f'token {github_secret}',
              'Content-Type': 'application/json'}
    url = f'https://api.github.com/repos/' \
          f'{config_dict["owner"]}/{repo_name}/keys'
    request_data = json.dumps({
        'title': args.pc_name,
        'key': public_key,
        'read_only': not args.write_access,
        })
    response = requests.post(url,
                             data=request_data,
                             headers=header,
                             )
    if int(response.status_code) != 201:
        print(f'Error adding {repo_name}: {response.content}')
        return False
    print(f'Successfully added the public key to {repo_name}')
    return True


print_buffer = ''
ssh_config = ''
for repository_name in config_dict['repository']:
    file_name = f'id_rsa.{args.pc_name}.{repository_name}'
    path = os.path.join(args.destination, file_name)
    shell_cmd = f'ssh-keygen -t ed25519 -N {args.passphrase}' \
                f' -f {path}'
    os.system(shell_cmd)
    print_buffer += f'{repository_name}: \n'
    with open(f'{path}.pub', 'r') as public_key_file:
        public_key = public_key_file.readline()
        if not args.no_github:
            add_deploy_key(repository_name, public_key)
        print_buffer += public_key
    print_buffer += '\n'
    ssh_config += f'Host github-{repository_name}\n' \
                  f'HostName github.com\n' \
                  f'User git\n' \
                  f'IdentityFile ~/.ssh/{file_name}\n\n'

print('========================================')
print('All public keys.')
print('Repository: public-key')
print('========================================')
print(print_buffer)

path = os.path.join(args.destination, 'public-keys.txt')
with open(path, 'w') as public_keys_file:
    public_keys_file.write(print_buffer)

path = os.path.join(args.destination, 'ssh-config.txt')
with open(path, 'w') as ssh_config_file:
    ssh_config_file.write(ssh_config)

print("""
========================================
.----.-----.---.-.--|  |.--------.-----.
|   _|  -__|  _  |  _  ||        |  -__|
|__| |_____|___._|_____||__|__|__|_____|
========================================
""")
if args.no_github:
    print('* Add the printed public keys (or in public-keys.txt) to the')
    print('  appropriate repositories (Repsitory/Setting/Deploy Keys)')
print('* Move the generated keys to ~/.ssh (both private and public)')
print('* Append ~/.ssh/config with the content in ssh-config.txt')
print('* When use, Set the remote url to github-[repository_name].')
print('  e.g. github-myrepo:zynaxsoft/myrepo')

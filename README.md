# Problem
I want to create and register deploy keys for doing `git pull` or `git clone`. What do I do?

# Solution
1. Clone this repository.
1. `cd tools`
1. if there is no *deploy-key-gen.py try* `checkout develop`
1. add/remove target repository name in *deploy-key-config.json*.
1. `python3 deploy-key-gen.py -N [passphrase] -n [pc_name] -t [target_folder]`
  * ex. `python3 deploy-key-gen.py -N password1234 -n my_laptop -t ssh_keys`
  * passphrase is a password that you have to enter when doing `git` remote related commands
1. Follow the appeared readme in the terminal.

> * Add the printed public keys (or in public-keys.txt) to the
>   appropriate repositories (Repository/Setting/Deploy Keys)
> * Move the generated keys to ~/.ssh (both private and public)
> * Append ~/.ssh/config with the content in ssh-config.txt
> * When used, Set the remote url to github-[repository_name]. e.g. github-myrepo:zynaxsoft/myrepo

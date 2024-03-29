# Problem
I want to create and register deploy keys for doing `git pull` or `git clone`. What do I do?

# Solution (with github automation)
1. Clone this repository.
1. Create personal access tokens on https://github.com/settings/tokens
1. Click `Generate new token`
1. Add some note for yourself and tick `repo` (Full control of private repositories)
1. `Generate token`
1. Copy the token and paste in on a new file in `secret.txt` that is at the same location with the script.
1. add/remove target repository name in *deploy-key-config.json*.
1. edit `owner` field to your username/organization, i.e. `zynaxsoft`.
1. `python3 deploy-key-gen.py -N [passphrase] -n [pc_name] -t [target_folder]`
  * ex. `python3 deploy-key-gen.py -N password1234 -n my_laptop -t ssh_keys`
  * passphrase is a password that you have to enter when doing `git` remote related commands
1. Follow the instructions on appeared readme in the terminal.

**Removing the created personal access token after the keys will also remove the generated/added deploy keys.**

If you want to be sure that this key will cause no harm, you can
 * Change the scope of the key by unchecking the checked `repo` option.
   * This will make the key has access to only public repository only and wii have only *read* access. [(reference)](https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/)
 * Update token.
 * Regenerate the token.


# Solution (no github automation)
1. Clone this repository.
1. add/remove target repository name in *deploy-key-config.json*.
1. `python3 deploy-key-gen.py -N [passphrase] -n [pc_name] -t [target_folder] --no-github`
  * ex. `python3 deploy-key-gen.py -N password1234 -n my_laptop -t ssh_keys --no-github`
  * passphrase is a password that you have to enter when doing `git` remote related commands
1. Follow the instructions on appeared readme in the terminal.

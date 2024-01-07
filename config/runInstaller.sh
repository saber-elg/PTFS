#!/bin/bash
# This script installs ptfs in the user's home directory and configure the .bashrc file with environnement variables and alias

read -p "Please enter PTFS local path \"ex: /home/user/Dowloads/PTFS\": " path

# Request new entry while the path is invalid
while [ ! -e "$path" ]
do
  echo "Invalid path, retry."
  read -p "Please enter PTFS local path: " path
done
 
# File Sytem Directories creation
mkdir ~/ptfs
cp -r $path/src/bin ~/ptfs
cp -r $path/src/sbin ~/ptfs
cd ~/ptfs
mkdir etc home log root sys usr

# etc folder initialisation
cd ~/ptfs/etc
touch root_file.json sudoers_file.json users_file.json
echo -e "{\n}" >> sudoers_file.json

# Root configuration
read -s -p "Enter a password for root: " password # -s hides the input
hash=$(python3 -c "import hashlib; print(hashlib.sha256(b'$password').hexdigest())")
echo -e "{\n    \"root\": {\n        \"password\": \"$hash\"\n    }\n}" >> root_file.json

# Creating an initial user
echo -e "\nEnter your username : "
read username 
echo -e "Enter a password for $username : "
read -s user_pass
user_hash=$(python3 -c "import hashlib; print(hashlib.sha256(b'$user_pass').hexdigest())")
echo -e "{\n    \"$username\": {\n        \"password\": \"$user_hash\"\n    }\n}" >> users_file.json
mkdir ~/ptfs/home/$username
# sys folder initialisation
cd ~/ptfs/sys
touch sys.json
cp -r $path/sys/icons ~/ptfs/sys
cp -r $path/sys/images ~/ptfs/sys
# Creating an initial system status
echo -e "{\n    \"status\": \"on\",\n    \"connected_user\": \"$username\"\n}" >> sys.json
~/ptfs/sbin/ptfs_mkdir --comment user_Documents ~/ptfs/home/$username/Documents
~/ptfs/sbin/ptfs_mkdir --comment user_Downloads ~/ptfs/home/$username/Downloads
~/ptfs/sbin/ptfs_mkdir --comment user_Desktop ~/ptfs/home/$username/Desktop
echo -e "{\n    \"status\": \"off\",\n    \"connected_user\": null\n}" > sys.json

# Ajoute les répertoires ptfs au PATH
echo "export PATH=\$PATH:~/ptfs/sbin" >> ~/.bashrc
echo "export PATH=\$PATH:~/ptfs/bin" >> ~/.bashrc

# Définit le prompt avec le nom d'utilisateur ptfs
echo "PS1="\'\$\(ptfs_whoami\) \'"" >> ~/.bashrc

# Crée un alias pour changer de répertoire avec ptfs
echo "alias ptfs_cd='source ptfs_chdir' " >> ~/.bashrc

# Change directory to home and remove the installation repository
cd ~/ptfs
rm -rf $path

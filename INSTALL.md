
# Librarian Installation Guide #

## Download Librarian Sources: ##
Before getting started, please make sure Docker is installed and running. You can type ```systemctl status docker``` to check the running status of Docker daemon.

Next, run the following command to clone Librarian:
```
# Using SSH
git clone https://github.com/salmanee/Librarian.git

# Using HTTPS
git clone git@github.com:salmanee/Librarian.git
```
In the same directory where Librarian resides, run the following command to start docker (whicch contains a working enviroment with all requierments installed):
```
docker run -it -v $PWD/Librarian:/home/Librarian --rm yhuai/librarian
```

If successful,  you will see the following messages at the bottom of your screen:
```
[root@44c29e2ea5d4 home]# ls
Librarian
```

## Using Librarian: ##

You can 

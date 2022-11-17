import subprocess

subprocess.run("docker-compose exec db bash -c 'mysql -uroot -proot -D ml_test '", shell=True)


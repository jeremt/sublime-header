/*
** test.c for test in /home/schoch_h/Projets/Python/sublime-header
** 
** Made by SCHOCH Hugo
** Login   <schoch_h@epitech.net>
** 
** Started on  Tue Jan  13 23:30:06 2015 SCHOCH Hugo
** Last update Tue Jan  13 23:30:06 2015 SCHOCH Hugo
*/




int main()
{






proc = subprocess.Popen("cat /etc/passwd | grep " + os.environ['USER'] + " | cut -d: -f5 | cut -d, -f1", stdout=subprocess.PIPE)



proc = os.popen("cat /etc/passwd | grep " + os.environ['USER'] + " | cut -d: -f5 | cut -d, -f1").read()



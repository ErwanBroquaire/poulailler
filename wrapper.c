#include <stdio.h>
#include <string.h>

int main(int argc, char**argv){
setuid(0);
char chaine1[100] = "/home/pi/poulailler/publier.py  ", espace[] = " ";


strcat(chaine1, argv[1]); // On concatene le permier argument dans chaine1
strcat(chaine1, espace); // On concatene un espace dans chaine1
strcat(chaine1, argv[2]); // On concatene le second argument dans chaine1
//printf(chaine1);
system(chaine1);
return 0;
}

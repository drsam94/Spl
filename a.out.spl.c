// e12.spl
// compiled with splc.py (c) Sam Donow 2013-2015
#include <stdio.h>
#include <math.h>
#include "include/mathhelpers.h"
int condition = 0;
char inputbuffer[BUFSIZ];
int main() {

int Juliet = 2;
int Ophelia = 2;
int Octavia = 0;
int Macbeth = 4;
int Romeo = 1;
int Julia = 2;
act1: {
goto act_1_scene1;
}
act_1_scene1: {
;
Octavia = 512 ;
Octavia = (Octavia - (16 + -4)) ;
Juliet = 2 ;

goto act2;

}
act2: {
goto act_2_scene1;
}
act_2_scene1: {
Romeo = (Romeo + 1) ;
Juliet = ((Romeo * (Romeo + 1)) / 2) ;
Macbeth = (int)sqrt(Juliet) ;

goto act_2_scene2;

}
act_2_scene2: {
Ophelia = 0 ;
condition = (square(Macbeth)) == (Juliet);
if (condition) {
 Ophelia = 1 ;
 }
Julia = 1 ;

goto act_2_scene3;

}
act_2_scene3: {
condition = ((Juliet % Julia)) > (0);
if (!condition) {
 Ophelia = (Ophelia + 2) ;
 }
Julia = (Julia + 1) ;
condition = (Julia) > (Macbeth);
if (condition) {
 goto act_2_scene4;
 }
if (!condition) {
 goto act_2_scene3;
 }

goto act_2_scene4;

}
act_2_scene4: {
;
condition = (Ophelia) > (Octavia);
if (condition) {
 goto act_2_scene5;
 }
goto act_2_scene1;

goto act_2_scene5;

}
act_2_scene5: {
;
fprintf(stdout, "%d", Juliet);
Ophelia = (2 * (1 + 4)) ;
fprintf(stdout, "%c", (char)Ophelia);

}
}

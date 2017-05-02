#include <string.h>
#define MAXSIZE 1130250
#define MAXNAMELENGTH 100


struct character
{
   int* stk;
   long top;
   int value;
   char name[MAXNAMELENGTH];
};
typedef struct character CHARACTER;
void push(CHARACTER *s, int num);
void pop(CHARACTER *s);

void push(CHARACTER *s, int num)
{
   if ((*s).top >= (MAXSIZE - 1))
   {
       char errormessage[MAXNAMELENGTH+500];
       strcpy(errormessage, "Error: ");
       strlcat(errormessage, (*s).name, MAXNAMELENGTH);
       strcat(errormessage, " knows too much!\n");
       printf (errormessage);
       printf("Length: ");
       printf("%i\n",(*s).top);
       return;
   }
   else
   {
     (*s).top = (*s).top + 1;
     (*s).stk[(*s).top] = num;
   }
   return;
}

void pop(CHARACTER *s)
{
    if ((*s).top <= -1)
    {
       char errormessage[MAXNAMELENGTH+50];
       strcpy(errormessage, "Error: ");
       strlcat(errormessage, (*s).name, MAXNAMELENGTH);
       strcat(errormessage, " knows nothing!\n");
       printf (errormessage);
       printf("Length: ");
       printf("%i\n",(*s).top);
       return;
    }
    else
    {
       (*s).value = (*s).stk[(*s).top];
       (*s).top = (*s).top - 1;
    }
    return;
}
                 
CHARACTER InitializeCharacter(int startingvalue, char* name)
{
    CHARACTER MyChar;
    MyChar.stk = malloc(MAXSIZE);
    MyChar.top = -1;
    MyChar.value = startingvalue;
    strncpy(MyChar.name,name,MAXNAMELENGTH);
    return MyChar;
}
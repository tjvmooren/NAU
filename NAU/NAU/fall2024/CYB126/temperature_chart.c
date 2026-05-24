#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
  if (argc <3 || argc>4) {
    printf("Please provide 2 or 3 numbers, the first two are the start and stop temperature,\n");
    printf("the third is the step increase,if a third isn't provided it will step by 1\n");
    return EXIT_SUCCESS;
  }
  int step = 1;
  int newstep = atoi(argv[3]);
  //check to see if there is a third arguement, assign step to third arguement if exists
  if(newstep != 0){
    step = newstep;
  }
  int start = atoi(argv[1]);
  int stop = atoi(argv[2]);
  printf("_F______->_______C__\n");
  //increase start by number step = default 1, or by third arguement
  for (start = start; start <= stop; start += step){
    //convert fahrenheit to celsius store in tocelsius
    //(Fahrenheit - 32) * 5/9 or 0.55555555555;
    double tocelsius = (start - 32)*0.55555555555;
    printf("|%i     ->     %.2f|\n", start, tocelsius);
  }
  return EXIT_SUCCESS;
}

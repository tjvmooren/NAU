#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
  if (argc !=2) {
    printf("Please provide the single integer number for the fibonacci sequence.\n ");
    return EXIT_SUCCESS;
  }
  //n resprents the nth term to calculate
  //using the golden ratio to calculate fibonacci numbers, g = golden ratio
  // xn = (g^n - (1-g)^n) / sqrt(5)
  float g = 1.618034;
  int n = atoi(argv[1]);
  int fibonacci = ((pow(g,n) - pow(1-g,n))/sqrt(5));
  printf("The nth term %i is %i in the fibonacci sequence\n", n,
        fibonacci);
  return EXIT_SUCCESS;
}

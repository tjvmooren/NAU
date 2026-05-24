#include <stdio.h>
#include <math.h>
#include <stdlib.h>


float to_fahrenheit(float celsius){
// Celsius to Fahrenheit formula
// (9.0 / 5.0) * celsius + 32
  float fahrenheit = ((9.0 / 5.0) * celsius) + 32.0;
  return fahrenheit;
}


int main(int argc, char *argv[]){
  if (argc > 2){
    printf("please provide only one integer to convert from celsius to fahrenheit\n");
    return EXIT_SUCCESS;
  }

  float celsius = to_fahrenheit(atof(argv[1]));
  printf("%i celsius converted to fahrenheit is %.2f\n", atoi(argv[1]), celsius);
  return EXIT_SUCCESS;
}

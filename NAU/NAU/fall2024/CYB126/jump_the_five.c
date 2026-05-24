#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
  //check to to see if argc = 8 or 11, do nothing. if it doesnt send error message
  if (argc == 8 || argc == 11) {}
  else{
    printf("Please provide either 7 or 10 digits(1-9) to encrypt.\n ");
    return EXIT_SUCCESS;
  }
  //minus one off argc to get stop number
  int stop = argc - 1;
  //print the original numbers
  for(int start = 1; start <= stop; start++){
    int digit = atoi(argv[start]);
    //check through argv[] to make sure no digits are greater than 9
    if(digit >= 10){
      printf("\nYou provided a digit greater than 9, only provide 1-9 digits.\n");
      return EXIT_SUCCESS;
    }
    printf("%i", digit);
  }
  //for clarity
  printf("\n----------\n");
  //using if,elif statments to swap digits iterting through argc[]
  //jump the five encryption for 7 or 10 digit numbers
  for(int start = 1; start <= stop; start++){
    int digit = atoi(argv[start]);
    if(digit == 0){
      digit = 5;
    }
    else if(digit == 5){
      digit = 0;
    }
    if(digit == 1){
      digit = 9;
    }
    else if(digit == 9){
      digit = 1;
    }
    if(digit == 2){
      digit = 8;
    }
    else if(digit == 8){
      digit = 2;
    }
    if(digit == 3){
      digit = 7;
    }
    else if(digit == 7){
      digit = 3;
    }
    if(digit == 4){
      digit = 6;
    }
    else if(digit == 6){
      digit = 4;
    }
    //print the new encrypted numbers
    printf("%i", digit);
  }
  return EXIT_SUCCESS;
}

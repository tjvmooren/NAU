# include <stdio.h>
# include <math.h>
int main(){
//initalize start stop and step
int start = 10;
int stop = 30;
int step = 4;
{
  for (start = start; start <= stop; start++)
  {
    //iterates through start->stop
    //uses modulo on start and step and stores in multiple
    int multiple = start % step;
    //if multiple does have a remainder = 0 then print the start number
    if (multiple == 0)
    {
      printf("%i\n", start);
    }
  }
  return 0;
}
}

# include <stdio.h>

int main()
{
  //Finding Resistance using Ohm's Law
  //R = Resistance, V = Voltage, I = Current
  //R = V / I. Resistance = Voltage / Current
  //For Homework: Voltage is 120, Current is 15
  double res = 0;
  int volt = 120;
  int current = 15;

  //Get the Voltage and Current from the user
  //printf("Enter the Voltage: \n");
  //scanf("%d", &volt);
  //printf("Enter the Current: \n");
  //scanf("%d", &current);

  // Divide voltage by current to get the resistance then print the result
  res = (double)volt / (double)current;
  printf("\n%d amps of current at %d volts requires %.2f ohms of resistance. \n", current, volt, res);

	return 0;
}

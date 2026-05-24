# include <stdio.h>
# include <math.h>
int main()
{
  //Finding roots using quadratic formula
  //Quadratic formula = ax^2 = bx + c = 0
  //Find roots by x = (-b +/- sqrt(b^2 -4ac)) / 2a
  //For Homework: Find's the roots for 2x^2 - 4x - 3
  double a = 2;
  double b = -4;
  double c = -3;
  double root1 = 0;
  double root2 = 0;
  //Get the values of a, b, c from user
  //printf("Enter the value of A: \n");
  //scanf("%lf", &a);
  //printf("Enter the value of B: \n");
  //scanf("%lf", &b);
  //printf("Enter the value of c: \n");
  //scanf("%lf", &c);
  // Use the quadratic formula to get the two roots.
  root1 = ((-b + (sqrt(pow(b, 2) - (4 * a * c))))/(2*a));
  root2 = ((-b - (sqrt(pow(b, 2) - (4 * a * c))))/(2*a));
  printf("Using the quadratic formula this program finds the roots of 2x^2 - 4x - 3\n");
  printf("x = %lf\n", root1);
  printf("x = %lf\n", root2);
  //Only functions if there are two real roots.
	return 0;
}

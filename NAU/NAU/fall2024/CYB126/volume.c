# include <stdio.h>
# include <math.h>
int main()
{
  //Finding the volume of a icosahedron
  //Volume = ((5(3 + sqrt(5))) / 12) * a^3 == 2.18169499062 * a^3 where a is the edge length
  //For Homework: The Length of Side is 5cm
  double volume = 0;
  double edge = 5;

  //Get the length of edges of icosahedron(in cm)
  //printf("Enter the edge length(in CM): \n");
  //scanf("%lf", &edge);

  //Do the forumla and print result
  volume = 2.18169499062 * pow(edge,3);
  printf("\nA icosahedron with edge length of %.2f cm has a volume of %.2f \n", edge, volume);

	return 0;
}

# include <stdio.h>
# include <math.h>
int main()
{
  //Calculates how many days,hours,minutes,seconds are in seconds given
  //For Homework: convert 8675309 seconds into days, hours, minutes, seconds
  //
  //
  int totalseconds = 8675309;
  int days = 0;
  int hours = 0;
  int minutes = 0;
  int seconds = 0;
  //Get the value of seconds from user
  //printf("Enter the amount of seconds to convert: \n");
  //scanf("%d", &totalseconds);
  int finalseconds = totalseconds;

  // for seconds in a day    = 86400 * days
  // for seconds in a hour   = 3600 * hours
  // for seconds in a minute = 60 * minutes
  // divide seconds by amount of seconds in a day and round down
  days = totalseconds / 86400;
  days = floor(days);
  //update totalseconds by minusing the amount of days calculated
  totalseconds = totalseconds - (days * 86400);
  //divide seconds by amount of seconds in hours and round down
  hours = totalseconds / 3600;
  hours = floor(hours);
  //update totalseconds by minusing the amount of hours calculated
  totalseconds = totalseconds - (hours * 3600);
  //divide seconds by amount of seconds in a minute and round down
  minutes = totalseconds / 60;
  minutes = floor(minutes);
  //find seconds by minusing totalseconds from amount of seconds in minutes
  seconds = totalseconds - (minutes * 60);

  printf("%d seconds is equivalent to %d days, %d hours, %d minutes, and %d seconds\n",finalseconds,days,hours,minutes,seconds);
	return 0;
}

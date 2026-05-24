# include <stdio.h>
# include <math.h>
int main()
{
  //Calculates how many total seconds by converting years,weeks,days,hours,minutes
  //For Homework: Convert 3 years, 6 weeks, 5 days, 2 hours, 5 minutes to seconds
  //
  //
  int years = 3;
  int weeks = 6;
  int days = 5;
  int hours = 2;
  int minutes = 5;
  int totalsec = 0;
  //Get the values of years, weeks, days, hours, minutes from user
  //printf("Enter the amount of years: \n");
  //scanf("%d", &years);
  //printf("Enter the amount of weeks: \n");
  //scanf("%d", &weeks);
  //printf("Enter the amount of days: \n");
  //scanf("%d", &days);
  //printf("Enter the amount of hours: \n");
  //scanf("%d", &hours);
  //printf("Enter the amount of minutes: \n");
  //scanf("%d", &minutes);
  // for seconds in a year   = 31536000 * years
  int secyears = 31536000 * years;
  // for seconds in a week   = 604800 * weeks
  int secweeks = 604800 * weeks;
  // for seconds in a day    = 86400 * days
  int secdays = 86400 * days;
  // for seconds in a hour   = 3600 * hours
  int sechours = 3600 * hours;
  // for seconds in a minute = 60 * minutes
  int secminutes = 60 * minutes;
  // add years + weeks + days + hours + minutes to get total seconds
  totalsec = secyears + secweeks + secdays + sechours + secminutes;
  printf("The amount of seconds in %d years, %d weeks, %d days, %d hours, %d minutes is %d seconds\n",years,weeks,days,hours,minutes,totalsec);
	return 0;
}

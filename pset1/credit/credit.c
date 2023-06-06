#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long card, first_digits, heMast;
    int lastdigit, second_to_last=0, h1, not_multi_by2=0, sum, lengh=0;
    /*printf("Number: ");
    scanf("%ld", &card);*/
    card = get_long("Number: ");
    first_digits=card;
    heMast = card;
// calculat the lengh of the num
    lengh = log10(card)+1;

// a loop gose into every digit in the num of card
    for(int i=1; log10(card)+1 >=1; i++)
    {
        // to find the last digit in each position
        lastdigit = card % 10;
        /*printf("%d: %d\n",i,  lastdigit);*/
        // to remove the last digit
        card = card/10;
        // for count the  second to last digit by ( # * 2)
        if (i % 2 == 0)
        {
            // if we have the case of (# *2)= ## =>> #+#
            h1 =lastdigit*2;
            if (h1>9)
            {
                h1=1 + (h1%10);
            }
            second_to_last = second_to_last + h1;
        }
        // for count the digit who are not multiplied by 2
        else
        {
            not_multi_by2 = not_multi_by2 + lastdigit;
        }

    }
    // the last sum that's to have an 0 in the last digit
    sum= second_to_last+not_multi_by2;

    if(sum % 10 == 0)
    {
        // check the first digits if they go with whish card
        if( lengh == 16 || lengh == 13)
        {
            // find the first digit
            while(first_digits >= 10)
            {
                first_digits = first_digits /10;
            }
            if (first_digits == 4)
            {
                printf("VISA\n");
                return 0;
            }
        }
        // get back the value of card number for the case of a mastercard
        first_digits = heMast;
        if (lengh == 16 || lengh == 15)
        {
            while(first_digits >= 100)
            {
                first_digits = first_digits /10;
            }
            if(lengh == 16 && (first_digits == 51 || first_digits == 52 ||first_digits == 53 ||first_digits == 54 ||first_digits == 55))
            {
                printf("MASTERCARD\n");
                return 0;
            }
            if (lengh == 15 && (first_digits == 34 || first_digits == 37))
            {
                printf("AMEX\n");
                return 0;
            }
            else
                printf("INVALID\n");
        }
        else
            printf("INVALID\n");
    }
    else
        printf("INVALID\n");
}
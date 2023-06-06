#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        printf("Height: ");
        scanf("%d", &n);
    }
    while (n > 8 || n <= 0);

    for (int i = 1 ; i <= n; i++)  // colums
    {
        for (int p = n; p > i; p--) // dots
        {
            printf(" ");
        }
        for (int j = 1; j <= i; j++) // 1st rows
        {
            printf("#");
        }
        printf("  ");
        for (int a = 1; a <= i; a++) // 2ed rows
        {
            printf("#");
        }
        printf("\n");
    }
}
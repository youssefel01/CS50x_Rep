#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    do
    {
        h = get_int("height: ");
    }
    while (h < 1 || h > 8);

    for (int r = 0; r < h; r++)
    {
//spaces
        for (int s = 0; s < h - r - 1; s++)
        {
            printf(" ");
        }
//hashes
        for (int c = 0; c <= r; c++)
        {
            printf("#");
        }
//lines
        printf("\n");
    }
}
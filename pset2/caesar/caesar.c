#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool only_digits(string s);
char rotate(char p, int k);

int main(int argc, string argv[])
{
// make sure there is one command-line argument
// make sure is it a decimal digit
// make sure the that is not negative
// make sure there is a command line AKA a key
    // convert argv[1] from "string" to "int"
    // prompt user for plaintext
    // for each character in the plaintext:
    // rotate the character if it's a letter
    int K;
    if (argc != 2 || !only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    K = atoi(argv[1]);

    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        char ciphertext = rotate(plaintext[i], K);
        printf("%c", ciphertext);
    }
    printf("\n");
}

bool only_digits(string s)
{
    for (int i = 0, len = strlen(s); i < len; i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

char rotate(char p, int k)
{
    char c;
    if (isupper(p))
    {
        p = p - 'A';
        c = (p + k) % 26;
        return c + 'A';
    }
    else if (islower(p))
    {
        p = p - 'a';
        c = (p + k) % 26;
        return c + 'a';
    }
    else
    {
        return p;
    }
}
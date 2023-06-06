
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string Text);
int count_words(string Text);
int count_sentences(string Text);

int main(void)
{
    string Text = get_string("Text: ");
    //letters
    float l = count_letters(Text);
    //words
    float w = count_words(Text);
    //sentences
    float s = count_sentences(Text);
    //Putting it All Together
    double L = (l * 100) / (w + 1);
    double S = (s * 100) / (w + 1);
    double Grade = 0.0588 * L - 0.296 * S - 15.8;

    //If the Grade number is less than 1
    if (Grade < 1)
    {
        printf("Before Grade 1\n");
    }
    //If the resulting Grade number is 16 or higher
    else if (Grade >= 16)
    {
        printf("Grade 16+\n");
    }
    //if the resulting is between 1 and 16, round the resulting Grade number to the nearest int!
    else
    {
        printf("Grade %i\n", (int) round(Grade));
    }
}


//count letters
int count_letters(string Text)
{

    int letters = 0;
    for (int i = 0; i < strlen(Text); i++)
    {
        if ((isupper(Text[i])) || (islower(Text[i])))
        {
            letters++;
        }
    }
    return letters;
}

//count words
int count_words(string Text)
{
    int words = 0;
    for (int i = 0; i < strlen(Text); i++)
    {
        if (Text[i] == ' ')
        {
            words++;
        }
    }
    return words;
}

//count sentences
int count_sentences(string Text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(Text); i++)
    {
        if (Text[i] == '.' || Text[i] == '!' || Text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}
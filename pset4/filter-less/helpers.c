#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // to float
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float Blue = image[i][j].rgbtBlue;
            //round average
            int average = round((red + green + Blue) / 3);
            //updat pixel value
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // to float
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float Blue = image[i][j].rgbtBlue;
            //round value
            int sepiaRed = round(.393 * red + .769 * green + .189 * Blue);
            int sepiaGreen = round(.349 * red + .686 * green + .168 * Blue);
            int sepiaBlue = round(.272 * red + .534 * green + .131 * Blue);

            // >255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            //updat pixel value
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            //swap values
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp [height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            // cope image
            temp [i][j] = image[i][j];
        }
    }

    for (int i = 0 ; i < height; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            int average_red = 0;
            int average_green = 0;
            int average_blue = 0;

            float counter = 0.00;

            for (int a = -1; a < 2; a++)
            {
                for (int b = -1; b < 2; b++)
                {
                    int ca = i + a;
                    int cb = j + b;

                    if (ca < 0 || ca > (height - 1) || cb < 0 || cb > (width - 1))
                    {
                        continue;
                    }

                    average_red += image[ca][cb].rgbtRed;
                    average_green += image[ca][cb].rgbtGreen;
                    average_blue += image[ca][cb].rgbtBlue;

                    counter++;
                }
                //count and round
                temp [i][j].rgbtRed = round(average_red / counter);
                temp [i][j].rgbtGreen = round(average_green / counter);
                temp [i][j].rgbtBlue = round(average_blue / counter);
            }
        }
    }

    for (int i = 0 ; i < height; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            //updat pixel value
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }

    return;
}

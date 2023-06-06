#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define BLOCK_SIZE 512
typedef uint8_t BYTE;


int main(int argc, char *argv[])
{
    // Check command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    //open memory card
    FILE *file = fopen(argv[1], "r");

    //If the forensic image cannot be opened for reading
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 2;
    }
    // variables

    BYTE buffer[BLOCK_SIZE];
    int count_image = 0;

    //file pointer for recover images
    FILE *output_file = NULL;

    //char filename
    char *filename = malloc(8 * sizeof(char));

    while (fread(buffer, sizeof(char), 512, file) == BLOCK_SIZE)
    {
        // check first three bytes
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //file name
            sprintf(filename, "%03i.jpg", count_image);

            //open output file for writing
            output_file = fopen(filename, "w");

            count_image++;
        }
        //check output
        if (output_file != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output_file);
        }
    }
    free(filename);
    fclose(output_file);
    fclose(file);
}



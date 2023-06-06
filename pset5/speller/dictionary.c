// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 17576; //=17576; 26 × 26 × 26 × 26= 456976

// Hash table
node *table[N];

//variables
int countword;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //hash word to obtain a hash value

    int index = hash(word);
    //access linked list au that index in the hash table

    node *cursor = table[index];
    //trabers licked list, looking for the word (strcasecmp)

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function

    unsigned long total = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // OPEN dictionary

    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open\n");
        return false;
    }
    //read strings form file one at time

    char word[LENGTH + 1];

    while ((fscanf(file, "%s", word)) != EOF)
    {
        //creat a new node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        //cope word into node
        strcpy(n->word, word);
        //insert node into the hash table
        n->next = NULL;
        unsigned int index = hash(word);


        n->next = table[index];
        table[index] = n;
        countword++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    //return number of words in dictionary
    if (countword > 0)
    {
        return countword;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <vector>

// Variables used to allocate array width and height
int height, width;

// Struct with RGB colors
typedef struct {
    int r;
    int g;
    int b;
} color;
typedef color Pixel;

/*
 * Generates a new .ppm file with the appropriate data allocations.
 */
void create_img (std::vector<std::vector<Pixel>> image, char output[]){

    strcat(output, ".ppm");
    FILE * image_file;
    
    image_file = fopen(output, "w");

    fprintf(image_file, "P3\n");
    fprintf(image_file, "%i %i\n%i\n",width, height, 255);

    int i, j;
    for(i = 0; i < height; i++){
        for(j = 0; j < width; j++){
            fprintf(image_file, "%i %i %i\n", image[i][j].r, image[i][j].g, image[i][j].b);
        }
    }    
    fclose(image_file);
}

/*
 * Performs binarization of the last image based on the threshold informed
 */
std::vector<std::vector<Pixel>> binarization(std::vector<std::vector<Pixel>> image, int thr){
    std::vector<std::vector<Pixel>> copy(height);
    for ( int i = 0 ; i < height ; i++ )
        copy[i].resize(width);

    copy = image;
    int bin = 0;
    int i, j;

    for(i=0; i < height; i++){
        for(j=0;j < width;j++){
            
            bin  = (copy[i][j].r + copy[i][j].g + copy[i][j].b)/3;

            if (bin > thr){
                copy[i][j].r = 255;
                copy[i][j].g = 255;
                copy[i][j].b = 255;
            }else{
                copy[i][j].r = 0;
                copy[i][j].g = 0;
                copy[i][j].b = 0;
            }
        }
    }

    return copy;
}

/*
 * Method main where the file is loaded, sent to binarize and saved in an output .ppm file
 */
int main(int argc, char** argv) {   
    
    FILE *file;

    // Read the file
    file = fopen(argv[1], "r");
    
    // Read the header data
    fscanf(file, "P3 %i %i 255",&width, &height);
    
    // Creates a matrix of Pixels
    std::vector<std::vector<Pixel>> image(height);
    for ( int i = 0 ; i < height ; i++ )
        image[i].resize(width);

    // Read each pixel by allocating in the variable referring to the struct
    for (int i = 0; i < height; i++)
        for(int j = 0; j < width; j++)
            fscanf(file, "%i %i %i", &image[i][j].r, &image[i][j].g, &image[i][j].b);

    // Close the file
    fclose(file);
 
    // Calls the binarization filter
    image = binarization(image, atoi(argv[2]));
    create_img(image, argv[3]);

    //printf("%s\n", "image binarized successfully!");     
    
    // Finish the program
    return (EXIT_SUCCESS);
}
